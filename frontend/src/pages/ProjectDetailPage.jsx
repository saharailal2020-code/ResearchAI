import { useCallback, useEffect, useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import {
  DetailItem,
  ErrorState,
  InfoCard,
  PlaceholderCard,
  StatusBadge,
  SummaryCard,
} from '../components/ui.jsx'
import { getProject, updateProjectStatus } from '../services/projects'
import { displayValue, formatCurrency, formatDate } from '../utils/formatters'
import { projectStatusStyles, questionnaireStatusStyles } from '../utils/statusStyles'

const projectStatusLabels = {
  Setup: 'Setup',
  Ready: 'Ready',
  Fieldwork: 'Fieldwork',
  QC: 'QC',
  Analysis: 'Analysis',
  Reporting: 'Reporting',
  Completed: 'Completed',
  Cancelled: 'Cancelled',
}

const projectSteps = ['Setup', 'Ready', 'Fieldwork', 'QC', 'Analysis', 'Reporting', 'Completed']

function ProjectDetailSkeleton() {
  return (
    <div className="mx-auto max-w-7xl animate-pulse space-y-4">
      <p className="text-sm font-medium text-slate-500">Memuat detail project...</p>
      <section className="rounded-lg border border-slate-200 bg-white p-6">
        <div className="h-5 w-52 rounded bg-slate-200" />
        <div className="mt-4 h-10 w-96 rounded bg-slate-200" />
      </section>
      <div className="grid gap-4 lg:grid-cols-4">
        <div className="h-24 rounded-lg border border-slate-200 bg-white" />
        <div className="h-24 rounded-lg border border-slate-200 bg-white" />
        <div className="h-24 rounded-lg border border-slate-200 bg-white" />
        <div className="h-24 rounded-lg border border-slate-200 bg-white" />
      </div>
      <div className="h-96 rounded-lg border border-slate-200 bg-white" />
    </div>
  )
}

function ProjectTimeline({ status }) {
  const currentIndex = projectSteps.indexOf(status)

  return (
    <InfoCard title="Timeline Project">
      <div className="overflow-x-auto">
        <div className="flex min-w-[760px] items-center">
          {projectSteps.map((step, index) => {
            const isCompleted = currentIndex > index
            const isActive = currentIndex === index
            return (
              <div className="flex flex-1 items-center" key={step}>
                <div
                  className={`flex h-10 w-10 items-center justify-center rounded-full text-sm font-bold ring-1 ${
                    isActive
                      ? 'bg-slate-950 text-white ring-slate-950'
                      : isCompleted
                        ? 'bg-emerald-50 text-emerald-700 ring-emerald-200'
                        : 'bg-slate-50 text-slate-400 ring-slate-200'
                  }`}
                >
                  {index + 1}
                </div>
                <div className="ml-3 min-w-0">
                  <p className={`text-sm font-semibold ${isActive ? 'text-slate-950' : 'text-slate-500'}`}>
                    {step}
                  </p>
                  <p className="text-xs text-slate-400">
                    {isActive ? 'Aktif' : isCompleted ? 'Selesai' : 'Berikutnya'}
                  </p>
                </div>
                {index < projectSteps.length - 1 && <div className="mx-4 h-px flex-1 bg-slate-200" />}
              </div>
            )
          })}
        </div>
      </div>
    </InfoCard>
  )
}

function ProjectDetailPage() {
  const { projectId } = useParams()
  const [project, setProject] = useState(null)
  const [error, setError] = useState('')
  const [actionError, setActionError] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  const [isActionLoading, setIsActionLoading] = useState(false)

  const nextAction = useMemo(() => (project?.status === 'Setup' ? 'Ready' : ''), [project?.status])

  const loadProject = useCallback(async () => {
    setIsLoading(true)
    setError('')

    try {
      const projectData = await getProject(projectId)
      setProject(projectData)
    } catch (requestError) {
      if (requestError?.response?.status === 404) {
        setError('Project tidak ditemukan.')
      } else {
        setError('Tidak dapat mengambil detail project. Periksa koneksi server lalu coba lagi.')
      }
    } finally {
      setIsLoading(false)
    }
  }, [projectId])

  useEffect(() => {
    loadProject()
  }, [loadProject])

  async function handleReadyAction() {
    setActionError('')
    setIsActionLoading(true)

    try {
      const updatedProject = await updateProjectStatus(projectId, 'Ready')
      setProject(updatedProject)
    } catch {
      setActionError('Status project belum bisa diperbarui. Silakan coba lagi.')
    } finally {
      setIsActionLoading(false)
    }
  }

  if (isLoading) {
    return <ProjectDetailSkeleton />
  }

  if (error) {
    return (
      <div className="mx-auto max-w-7xl">
        <div className="mb-4 flex items-center gap-2 text-sm font-medium text-slate-500">
          <Link className="hover:text-slate-950" to="/projects">
            Project
          </Link>
          <span>/</span>
          <span className="text-slate-950">Project Detail</span>
        </div>
        <ErrorState
          actions={
            <>
              <button
                className="rounded-md border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50"
                onClick={loadProject}
                type="button"
              >
                Coba Lagi
              </button>
              <Link
                className="rounded-md bg-slate-950 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800"
                to="/proposals"
              >
                Kembali ke Proposal
              </Link>
            </>
          }
          message={error}
          title="Detail project belum bisa ditampilkan"
        />
      </div>
    )
  }

  return (
    <div className="mx-auto max-w-7xl">
      <div className="mb-4 flex items-center gap-2 text-sm font-medium text-slate-500">
        <Link className="hover:text-slate-950" to="/projects">
          Project
        </Link>
        <span>/</span>
        <span className="text-slate-950">Project Detail</span>
      </div>

      <section className="rounded-lg border border-slate-200 bg-white">
        <div className="flex flex-col gap-5 border-b border-slate-200 px-6 py-5 lg:flex-row lg:items-start lg:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase text-slate-400">Project Number</p>
            <h1 className="mt-1 text-3xl font-bold tracking-normal text-slate-950 md:text-4xl">
              {project.project_number}
            </h1>
            <p className="mt-3 text-xl font-semibold text-slate-900">{project.project_name}</p>
            <p className="mt-2 text-sm text-slate-500">
              Client: {project.client.client_name} | Research Type: {displayValue(project.research_type)} | Value:{' '}
              {formatCurrency(project.project_value)}
            </p>
            <p className="mt-1 text-sm text-slate-500">Proposal: {project.proposal.proposal_number}</p>
          </div>
          <StatusBadge
            label={projectStatusLabels[project.status] || project.status}
            status={project.status}
            styles={projectStatusStyles}
          />
        </div>
      </section>

      <div className="mt-4 grid gap-4 lg:grid-cols-4">
        <SummaryCard label="Project Value" value={formatCurrency(project.project_value)} />
        <SummaryCard label="Status" value={projectStatusLabels[project.status] || project.status} />
        <SummaryCard label="Research Type" value={displayValue(project.research_type)} />
        <SummaryCard label="Project Manager" value={project.project_manager?.full_name || 'Belum ditentukan'} />
      </div>

      <div className="mt-4 grid gap-4 lg:grid-cols-[minmax(0,1.2fr)_minmax(320px,0.8fr)]">
        <div className="space-y-4">
          <InfoCard title="Informasi Project">
            <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
              <DetailItem label="Project Number" value={project.project_number} strong />
              <DetailItem label="Project Name" value={project.project_name} strong />
              <DetailItem label="Research Type" value={displayValue(project.research_type)} />
              <DetailItem label="Project Value" value={formatCurrency(project.project_value)} />
              <DetailItem label="Project Manager" value={project.project_manager?.full_name || 'Belum ditentukan'} />
              <DetailItem label="Business Development" value={project.business_development_owner?.full_name || '-'} />
              <DetailItem label="Tanggal Dibuat" value={formatDate(project.created_at)} />
              <DetailItem label="Terakhir Diperbarui" value={formatDate(project.updated_at)} />
              <DetailItem label="Ready Date" value={formatDate(project.ready_at)} />
            </div>
          </InfoCard>

          <ProjectTimeline status={project.status} />

          <section>
            <div className="mb-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <p className="text-base font-semibold text-slate-950">Questionnaire</p>
                <p className="mt-1 text-sm text-slate-500">Instrumen survey kuantitatif berdasarkan target respondent.</p>
              </div>
              <Link
                className="inline-flex h-10 items-center justify-center rounded-md bg-slate-950 px-4 text-sm font-semibold text-white hover:bg-slate-800"
                to={`/projects/${project.id}/questionnaire/new`}
              >
                + Tambah Questionnaire
              </Link>
            </div>
            <div className="rounded-lg border border-slate-200 bg-white">
              {project.questionnaires?.length > 0 ? (
                <div className="overflow-x-auto">
                  <table className="min-w-[920px] w-full border-collapse text-left">
                    <thead>
                      <tr className="border-b border-slate-200 bg-slate-50 text-xs font-semibold uppercase text-slate-400">
                        <th className="px-5 py-3">Questionnaire</th>
                        <th className="px-5 py-3">Target Respondent</th>
                        <th className="px-5 py-3">Instrument Type</th>
                        <th className="px-5 py-3">Version</th>
                        <th className="px-5 py-3">Status</th>
                        <th className="px-5 py-3">Last Updated</th>
                        <th className="px-5 py-3">Action</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-200">
                      {project.questionnaires.map((questionnaire) => (
                        <tr className="hover:bg-slate-50" key={questionnaire.id}>
                          <td className="px-5 py-4 text-sm font-semibold text-slate-950">
                            {questionnaire.questionnaire_name}
                          </td>
                          <td className="px-5 py-4 text-sm text-slate-700">{questionnaire.target_respondent}</td>
                          <td className="px-5 py-4 text-sm text-slate-700">{questionnaire.instrument_type}</td>
                          <td className="px-5 py-4 text-sm text-slate-700">{questionnaire.version_number}</td>
                          <td className="px-5 py-4">
                            <StatusBadge
                              label={questionnaire.status}
                              status={questionnaire.status}
                              styles={questionnaireStatusStyles}
                            />
                          </td>
                          <td className="px-5 py-4 text-sm text-slate-600">{formatDate(questionnaire.updated_at)}</td>
                          <td className="px-5 py-4">
                            <Link
                              className="text-sm font-semibold text-slate-950 hover:text-slate-700"
                              to={`/questionnaires/${questionnaire.id}`}
                            >
                              Buka
                            </Link>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="px-5 py-10 text-center">
                  <p className="text-base font-semibold text-slate-950">Belum ada questionnaire</p>
                  <p className="mt-2 text-sm text-slate-500">
                    Tambahkan instrumen survey kuantitatif berdasarkan target respondent project ini.
                  </p>
                </div>
              )}
            </div>

            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
              <PlaceholderCard description="Target sample, quota, dan segment project akan dikelola di sini." title="Sample" />
              <PlaceholderCard description="Pelaksanaan pengumpulan data akan dimonitor di sini." title="Fieldwork" />
              <PlaceholderCard description="Pemeriksaan kualitas data project akan dikelola di sini." title="QC" />
              <PlaceholderCard description="Dataset hasil project akan dikelola pada modul ini." title="Dataset" />
              <PlaceholderCard description="Dashboard project akan tersedia pada phase berikutnya." label="Coming Soon" title="Dashboard" />
              <PlaceholderCard description="Report final dan deliverable client akan dikelola di sini." label="Coming Soon" title="Report" />
            </div>
          </section>
        </div>

        <aside className="space-y-4">
          <InfoCard title="Next Business Action">
            {nextAction ? (
              <>
                <p className="text-sm leading-6 text-slate-600">
                  Project masih dalam tahap Setup. Tandai Ready setelah data awal project sudah siap dijalankan.
                </p>
                <button
                  className="mt-5 inline-flex h-10 w-full items-center justify-center rounded-md bg-slate-950 px-4 text-sm font-semibold text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-300 disabled:text-slate-500"
                  disabled={isActionLoading}
                  onClick={handleReadyAction}
                  type="button"
                >
                  {isActionLoading ? 'Memperbarui Status...' : 'Tandai Ready'}
                </button>
              </>
            ) : (
              <div className="rounded-md bg-slate-50 px-4 py-3 text-sm font-medium text-slate-600">
                Tidak ada aksi lanjutan untuk status ini pada sprint ini.
              </div>
            )}
            {actionError && (
              <div className="mt-4 rounded-md bg-red-50 px-4 py-3 text-sm font-semibold text-red-700">
                {actionError}
              </div>
            )}
          </InfoCard>

          <InfoCard title="Informasi Client">
            <div className="space-y-4">
              <DetailItem label="Nama Client" value={project.client.client_name} strong />
              <DetailItem label="Industry" value={displayValue(project.client.industry)} />
              <DetailItem label="Kota" value={displayValue(project.client.city)} />
              <DetailItem label="Status Client" value={displayValue(project.client.status)} />
            </div>
            <Link
              className="mt-5 inline-flex w-full justify-center rounded-md border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50"
              to={`/clients/${project.client_id}`}
            >
              Buka Client
            </Link>
          </InfoCard>

          <InfoCard title="Proposal Asal">
            <div className="space-y-4">
              <DetailItem label="Nomor Proposal" value={project.proposal.proposal_number} strong />
              <DetailItem label="Judul Proposal" value={project.proposal.proposal_title} />
              <DetailItem label="Status Proposal" value={project.proposal.status} />
              <DetailItem label="Owner Proposal" value={project.proposal.proposal_owner?.full_name || '-'} />
              <DetailItem label="Tanggal Disetujui" value={formatDate(project.proposal.approved_at)} />
            </div>
            <Link
              className="mt-5 inline-flex w-full justify-center rounded-md border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50"
              to={`/proposals/${project.proposal_id}`}
            >
              Buka Proposal
            </Link>
          </InfoCard>
        </aside>
      </div>
    </div>
  )
}

export default ProjectDetailPage
