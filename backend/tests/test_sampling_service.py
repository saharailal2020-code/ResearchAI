import sys
import unittest
import uuid
from decimal import Decimal
from pathlib import Path

from fastapi import HTTPException
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.db.base import Base
from app.models import Client, ClientActivity, Project, Proposal, Questionnaire, User
from app.models.sampling import SamplingTarget
from app.schemas.sampling import (
    SampleGroupCreate,
    SampleGroupStatusUpdate,
    SampleGroupUpdate,
    SamplingTargetCreate,
)
from app.services.sampling import create_sample_group, update_sample_group, update_sample_group_status


class SamplingServiceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine("sqlite+pysqlite:///:memory:")
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)
        self.db = self.SessionLocal()

        self.user = User(
            full_name="ResearchAI Admin",
            email=f"admin-{uuid.uuid4()}@researchai.local",
            password_hash="hash",
            status="active",
            is_active=True,
        )
        self.client = Client(client_name="Beerka Test Client", status="Active")
        self.db.add_all([self.user, self.client])
        self.db.flush()

        self.proposal = Proposal(
            proposal_number="PROP-TEST-0001",
            client_id=self.client.id,
            proposal_owner_id=self.user.id,
            proposal_title="Sampling Plan Test Proposal",
            research_type="Quantitative",
            estimated_budget=Decimal("10000000"),
            status="Approved",
            created_by=self.user.id,
        )
        self.db.add(self.proposal)
        self.db.flush()

        self.project = Project(
            project_number="PRJ-TEST-0001",
            client_id=self.client.id,
            proposal_id=self.proposal.id,
            project_name="Sampling Plan Test Project",
            research_type="Quantitative",
            project_value=Decimal("10000000"),
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
            status="Draft",
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

    def tearDown(self) -> None:
        self.db.close()
        self.engine.dispose()

    def build_payload(self, name: str, questionnaire_id: uuid.UUID | None = None) -> SampleGroupCreate:
        return SampleGroupCreate(
            sample_group_name=name,
            questionnaire_id=questionnaire_id,
            target_respondent=name,
            notes="Target sampling sesuai proposal.",
            targets=[
                SamplingTargetCreate(region_type="Provinsi", region_name="Jawa Barat", target_sample=100),
                SamplingTargetCreate(region_type="Provinsi", region_name="Jawa Tengah", target_sample=80),
            ],
        )

    def test_pattern_b_allows_one_questionnaire_for_many_sample_groups(self) -> None:
        first = create_sample_group(
            self.db,
            self.project.id,
            self.build_payload("Mitra", self.questionnaire.id),
            self.user,
        )
        second = create_sample_group(
            self.db,
            self.project.id,
            self.build_payload("Non Mitra", self.questionnaire.id),
            self.user,
        )

        self.assertEqual(first.questionnaire_id, self.questionnaire.id)
        self.assertEqual(second.questionnaire_id, self.questionnaire.id)
        self.assertEqual(first.total_target_sample, 180)
        self.assertEqual(second.total_target_sample, 180)

    def test_pattern_a_allows_many_questionnaires_for_many_sample_groups(self) -> None:
        mitra = create_sample_group(
            self.db,
            self.project.id,
            self.build_payload("Mitra", self.questionnaire.id),
            self.user,
        )
        umkm = create_sample_group(
            self.db,
            self.project.id,
            self.build_payload("UMKM", self.questionnaire_umkm.id),
            self.user,
        )

        self.assertNotEqual(mitra.questionnaire_id, umkm.questionnaire_id)
        self.assertEqual(mitra.targets[0].target_sample, 100)
        self.assertEqual(umkm.targets[1].region_name, "Jawa Tengah")

    def test_rejects_questionnaire_from_another_project(self) -> None:
        other_proposal = Proposal(
            proposal_number="PROP-TEST-0002",
            client_id=self.client.id,
            proposal_owner_id=self.user.id,
            proposal_title="Other Proposal",
            status="Approved",
            created_by=self.user.id,
        )
        self.db.add(other_proposal)
        self.db.flush()
        other_project = Project(
            project_number="PRJ-TEST-0002",
            client_id=self.client.id,
            proposal_id=other_proposal.id,
            project_name="Other Project",
            status="Setup",
            created_by=self.user.id,
        )
        self.db.add(other_project)
        self.db.flush()
        other_questionnaire = Questionnaire(
            project_id=other_project.id,
            questionnaire_name="Other Questionnaire",
            target_respondent="Other",
            instrument_type="Quantitative Survey",
            version_number=1,
            status="Draft",
            sort_order=1,
            created_by=self.user.id,
        )
        self.db.add(other_questionnaire)
        self.db.commit()

        with self.assertRaises(HTTPException):
            create_sample_group(
                self.db,
                self.project.id,
                self.build_payload("Invalid", other_questionnaire.id),
                self.user,
            )

    def test_mark_ready_and_reject_ready_edit(self) -> None:
        sample_group = create_sample_group(
            self.db,
            self.project.id,
            self.build_payload("Rumah Tangga", self.questionnaire.id),
            self.user,
        )

        ready = update_sample_group_status(
            self.db,
            sample_group.id,
            SampleGroupStatusUpdate(status="Ready"),
            self.user,
        )

        self.assertEqual(ready.status, "Ready")
        self.assertIsNotNone(ready.ready_at)

        with self.assertRaises(HTTPException):
            update_sample_group(
                self.db,
                sample_group.id,
                SampleGroupUpdate(notes="Should not edit ready sample group"),
                self.user,
            )

    def test_activity_logging_for_create_update_ready(self) -> None:
        sample_group = create_sample_group(
            self.db,
            self.project.id,
            self.build_payload("Rumah Tangga", self.questionnaire.id),
            self.user,
        )
        update_sample_group(
            self.db,
            sample_group.id,
            SampleGroupUpdate(notes="Updated target sampling notes"),
            self.user,
        )
        update_sample_group_status(
            self.db,
            sample_group.id,
            SampleGroupStatusUpdate(status="Ready"),
            self.user,
        )

        activities = self.db.execute(
            select(ClientActivity.activity_title).where(ClientActivity.source_type == "SamplingPlan")
        ).scalars().all()

        self.assertIn("Sampling Plan dibuat", activities)
        self.assertIn("Sampling Plan diperbarui", activities)
        self.assertIn("Sampling Plan ditandai Ready", activities)

    def test_update_replaces_sampling_targets_without_orphans(self) -> None:
        sample_group = create_sample_group(
            self.db,
            self.project.id,
            self.build_payload("Rumah Tangga", self.questionnaire.id),
            self.user,
        )
        old_target_ids = {target.id for target in sample_group.targets}

        updated = update_sample_group(
            self.db,
            sample_group.id,
            SampleGroupUpdate(
                targets=[
                    SamplingTargetCreate(region_type="Provinsi", region_name="Jawa Timur", target_sample=90),
                    SamplingTargetCreate(region_type="Provinsi", region_name="Bali", target_sample=40),
                ],
            ),
            self.user,
        )

        new_targets = self.db.execute(
            select(SamplingTarget).where(SamplingTarget.sample_group_id == sample_group.id)
        ).scalars().all()
        new_target_ids = {target.id for target in new_targets}
        new_region_names = {target.region_name for target in new_targets}

        orphaned_old_targets = self.db.execute(
            select(SamplingTarget).where(SamplingTarget.id.in_(old_target_ids))
        ).scalars().all()

        self.assertEqual(updated.total_target_sample, 130)
        self.assertEqual(len(new_targets), 2)
        self.assertEqual(new_region_names, {"Jawa Timur", "Bali"})
        self.assertTrue(old_target_ids.isdisjoint(new_target_ids))
        self.assertEqual(orphaned_old_targets, [])


if __name__ == "__main__":
    unittest.main()
