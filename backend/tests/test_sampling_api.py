import sys
import unittest
import uuid
from decimal import Decimal
from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.api.deps import get_current_user
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models import Client, ClientActivity, Project, Proposal, Questionnaire, User
from app.models.sampling import SampleGroup, SamplingTarget


class SamplingApiTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine(
            "sqlite+pysqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)
        self.db = self.SessionLocal()

        self.user = User(
            full_name="ResearchAI Admin",
            email=f"api-admin-{uuid.uuid4()}@researchai.local",
            password_hash="hash",
            status="active",
            is_active=True,
        )
        self.client_record = Client(client_name="Beerka API Client", status="Active")
        self.db.add_all([self.user, self.client_record])
        self.db.flush()

        self.proposal = Proposal(
            proposal_number="PROP-API-0001",
            client_id=self.client_record.id,
            proposal_owner_id=self.user.id,
            proposal_title="Sampling API Proposal",
            research_type="Quantitative",
            estimated_budget=Decimal("15000000"),
            status="Approved",
            created_by=self.user.id,
        )
        self.db.add(self.proposal)
        self.db.flush()

        self.project = Project(
            project_number="PRJ-API-0001",
            client_id=self.client_record.id,
            proposal_id=self.proposal.id,
            project_name="Sampling API Project",
            research_type="Quantitative",
            project_value=Decimal("15000000"),
            status="Setup",
            created_by=self.user.id,
        )
        self.db.add(self.project)
        self.db.flush()

        self.questionnaire = Questionnaire(
            project_id=self.project.id,
            questionnaire_name="Questionnaire Kepuasan",
            target_respondent="Mitra",
            instrument_type="Quantitative Survey",
            version_number=1,
            status="Ready",
            sort_order=1,
            created_by=self.user.id,
        )
        self.questionnaire_umkm = Questionnaire(
            project_id=self.project.id,
            questionnaire_name="Questionnaire UMKM",
            target_respondent="UMKM",
            instrument_type="Quantitative Survey",
            version_number=1,
            status="Draft",
            sort_order=2,
            created_by=self.user.id,
        )
        self.db.add_all([self.questionnaire, self.questionnaire_umkm])
        self.db.commit()

        def override_get_db():
            db = self.SessionLocal()
            try:
                yield db
            finally:
                db.close()

        def override_get_current_user():
            return self.user

        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_current_user] = override_get_current_user
        self.api = TestClient(app)

    def tearDown(self) -> None:
        app.dependency_overrides.clear()
        self.db.close()
        self.engine.dispose()

    def sample_group_payload(
        self,
        name: str = "Rumah Tangga",
        questionnaire_id: uuid.UUID | None = None,
    ) -> dict[str, object]:
        return {
            "questionnaire_id": str(questionnaire_id) if questionnaire_id else None,
            "sample_group_name": name,
            "target_respondent": name,
            "notes": "Target sampling sesuai proposal.",
            "targets": [
                {"region_type": "Provinsi", "region_name": "Jawa Barat", "target_sample": 100},
                {"region_type": "Provinsi", "region_name": "Jawa Tengah", "target_sample": 80},
            ],
        }

    def create_sample_group(self, name: str = "Rumah Tangga") -> dict[str, object]:
        response = self.api.post(
            f"/api/v1/projects/{self.project.id}/sample-groups",
            json=self.sample_group_payload(name, self.questionnaire.id),
        )
        self.assertEqual(response.status_code, 201)
        return response.json()

    def test_sample_group_crud_status_and_activity_logging(self) -> None:
        created = self.create_sample_group()

        self.assertEqual(created["sample_group_name"], "Rumah Tangga")
        self.assertEqual(created["status"], "Draft")
        self.assertEqual(created["total_target_sample"], 180)
        self.assertEqual(len(created["targets"]), 2)

        list_response = self.api.get(f"/api/v1/projects/{self.project.id}/sample-groups")
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(len(list_response.json()), 1)

        detail_response = self.api.get(f"/api/v1/sample-groups/{created['id']}")
        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(detail_response.json()["id"], created["id"])

        update_response = self.api.patch(
            f"/api/v1/sample-groups/{created['id']}",
            json={
                "notes": "Updated API notes",
                "targets": [
                    {"region_type": "Provinsi", "region_name": "Jawa Timur", "target_sample": 120},
                    {"region_type": "Provinsi", "region_name": "Bali", "target_sample": 40},
                ],
            },
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json()["total_target_sample"], 160)
        self.assertEqual({target["region_name"] for target in update_response.json()["targets"]}, {"Jawa Timur", "Bali"})

        ready_response = self.api.patch(
            f"/api/v1/sample-groups/{created['id']}/status",
            json={"status": "Ready"},
        )
        self.assertEqual(ready_response.status_code, 200)
        self.assertEqual(ready_response.json()["status"], "Ready")

        ready_delete_response = self.api.delete(f"/api/v1/sample-groups/{created['id']}")
        self.assertEqual(ready_delete_response.status_code, 400)

        activities = self.db.execute(
            select(ClientActivity.activity_title).where(ClientActivity.source_type == "SamplingPlan")
        ).scalars().all()
        self.assertIn("Sampling Plan dibuat", activities)
        self.assertIn("Sampling Plan diperbarui", activities)
        self.assertIn("Sampling Plan ditandai Ready", activities)

    def test_delete_draft_sample_group_removes_targets(self) -> None:
        created = self.create_sample_group("UMKM")
        target_ids = {target["id"] for target in created["targets"]}

        response = self.api.delete(f"/api/v1/sample-groups/{created['id']}")

        self.assertEqual(response.status_code, 204)
        self.assertIsNone(self.db.get(SampleGroup, uuid.UUID(created["id"])))
        remaining_targets = self.db.execute(
            select(SamplingTarget).where(SamplingTarget.id.in_([uuid.UUID(target_id) for target_id in target_ids]))
        ).scalars().all()
        self.assertEqual(remaining_targets, [])

    def test_sampling_target_crud_and_last_target_validation(self) -> None:
        created = self.create_sample_group("Bank Peserta")
        first_target_id = created["targets"][0]["id"]
        second_target_id = created["targets"][1]["id"]

        list_response = self.api.get(f"/api/v1/sample-groups/{created['id']}/targets")
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(len(list_response.json()), 2)

        detail_response = self.api.get(f"/api/v1/sampling-targets/{first_target_id}")
        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(detail_response.json()["region_name"], "Jawa Barat")

        add_response = self.api.post(
            f"/api/v1/sample-groups/{created['id']}/targets",
            json={"region_type": "Provinsi", "region_name": "Jawa Timur", "target_sample": 90},
        )
        self.assertEqual(add_response.status_code, 201)
        self.assertEqual(add_response.json()["total_target_sample"], 270)

        update_response = self.api.patch(
            f"/api/v1/sampling-targets/{first_target_id}",
            json={"region_name": "DKI Jakarta", "target_sample": 70},
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json()["total_target_sample"], 240)

        delete_response = self.api.delete(f"/api/v1/sampling-targets/{second_target_id}")
        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(len(delete_response.json()["targets"]), 2)

        remaining_target_ids = [target["id"] for target in delete_response.json()["targets"]]
        self.api.delete(f"/api/v1/sampling-targets/{remaining_target_ids[0]}")
        last_delete_response = self.api.delete(f"/api/v1/sampling-targets/{remaining_target_ids[1]}")
        self.assertEqual(last_delete_response.status_code, 400)

    def test_pattern_a_and_pattern_b_are_supported_by_api(self) -> None:
        pattern_b_first = self.api.post(
            f"/api/v1/projects/{self.project.id}/sample-groups",
            json=self.sample_group_payload("Mitra", self.questionnaire.id),
        )
        pattern_b_second = self.api.post(
            f"/api/v1/projects/{self.project.id}/sample-groups",
            json=self.sample_group_payload("Non Mitra", self.questionnaire.id),
        )
        pattern_a_third = self.api.post(
            f"/api/v1/projects/{self.project.id}/sample-groups",
            json=self.sample_group_payload("UMKM", self.questionnaire_umkm.id),
        )

        self.assertEqual(pattern_b_first.status_code, 201)
        self.assertEqual(pattern_b_second.status_code, 201)
        self.assertEqual(pattern_a_third.status_code, 201)
        self.assertEqual(pattern_b_first.json()["questionnaire_id"], str(self.questionnaire.id))
        self.assertEqual(pattern_b_second.json()["questionnaire_id"], str(self.questionnaire.id))
        self.assertEqual(pattern_a_third.json()["questionnaire_id"], str(self.questionnaire_umkm.id))

    def test_validation_and_not_found_errors(self) -> None:
        missing_project_response = self.api.get(f"/api/v1/projects/{uuid.uuid4()}/sample-groups")
        self.assertEqual(missing_project_response.status_code, 404)

        invalid_create_response = self.api.post(
            f"/api/v1/projects/{self.project.id}/sample-groups",
            json={
                "sample_group_name": "A",
                "targets": [{"region_type": "Provinsi", "region_name": "Jawa Barat", "target_sample": 0}],
            },
        )
        self.assertEqual(invalid_create_response.status_code, 422)

        missing_target_response = self.api.get(f"/api/v1/sampling-targets/{uuid.uuid4()}")
        self.assertEqual(missing_target_response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
