import { useEffect, useMemo, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'

import { DetailItem, ErrorState, InfoCard, StatusBadge } from '../components/ui.jsx'
import { getClient } from '../services/clients'
import { getProposal } from '../services/proposals'
import { setupProjectFromProposal } from '../services/projects'
import { displayValue, formatCurrency, formatDate } from '../utils/formatters'
import { proposalStatusStyles } from '../utils/statusStyles'

function primaryContact(client) {
  return client?.contacts?.find((contact) => contact.is_primary) || client?.contacts?.[0] || null
}

function ProjectSetupSkeleton() {
  return (
    <div className="mx-auto max-w-7xl animate-pulse space-y-4">
      <p className="text-sm font-medium text-slate-500">Memuat data setup project...</p>
      <section className="rounded-lg border border-slate-200 bg-white p-6">
        <div className="h-5 w-40 rounded bg-slate-200" />
        <div className="mt-4 h-10 w-96 rounded bg-slate-200" />
      </section>
      <div className="grid gap-4 lg:grid-cols-[minmax(0,1.25fr)_minmax(320px,0.75fr)]">
        <div className="h-96 rounded-lg border border-slate-200 bg-white" />
        <div className="h-96 rounded-lg border border-slate-200 bg-white" />
      </div>
    </div>
  )
}

function ProjectSetupReviewPage() {
  const navigate = useNavigate()
  const { proposalId } = useParams()
  const [proposal, setProposal] = useState(null)
  const [client, setClient] = useState(null)
  const [projectName, setProjectName] = useState('')
  const [error, setError] = useState('')
  const [validationError, setValidationError] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const contact = useMemo(() => primaryContact(client), [client])

  useEffect(() => {
    let isMounted = true

    async function loadData() {
      setIsLoading(true)
      setError('')

      try {
        const proposalData = await getProposal(proposalId)
        if (proposalData.status !== 'Approved') {
          setError('Project hanya dapat dibuat dari Proposal yang sudah disetujui.')
          return
        }
        if (proposalData.project_id) {
          navigate(`/projects/${proposalData.project_id}`, { replace: true })
          return
        }

        const clientData = await getClient(proposalData.client_id)
        if (isMounted) {
          setProposal(proposalData)
          setClient(clientData)
          setProjectName(proposalData.proposal_title || '')
        }
      } catch (requestError) {
        if (requestError?.response?.status === 404) {
          setError('Proposal tidak ditemukan.')
        } else {
          setError('Tidak dapat memuat data setup project. Periksa koneksi server lalu coba lagi.')
        }
      } finally {
        if (isMounted) {
          setIsLoading(false)
        }
      }
    }

    loadData()

    return () => {
      isMounted = false
    }
  }, [navigate, proposalId])

  async function handleSubmit(event) {
    event.preventDefault()
    const trimmedName = projectName.trim()
    setValidationError('')

    if (trimmedName.length < 3) {
      setValidationError('Nama project wajib diisi minimal 3 karakter.')
      return
    }
    if (trimmedName.length > 150) {
      setValidationError('Nama project maksimal 150 karakter.')
      return
    }

    setIsSubmitting(true)
    try {
      const project = await setupProjectFromProposal(proposalId, { project_name: trimmedName })
      navigate(`/projects/${project.id}`)
    } catch (requestError) {
      if (requestError?.response?.status === 400) {
        setError(requestError.response.data?.detail || 'Project belum bisa dibuat dari proposal ini.')
      } else {
        setError('Project belum bisa dibuat. Silakan coba lagi.')
      }
    } finally {
      setIsSubmitting(false)
    }
  }

  if (isLoading) {
    return <ProjectSetupSkeleton />
  }

  if (error && !proposal) {
    return (
      <div className="mx-auto max-w-7xl">
        <div className="mb-4 flex items-center gap-2 text-sm font-medium text-slate-500">
          <Link className="hover:text-slate-950" to="/proposals">
            Proposal
          </Link>
          <span>/</span>
          <span className="text-slate-950">Setup Project</span>
        </div>
        <ErrorState
          actions={
            <>
              <Link
                className="rounded-md border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50"
                to={`/proposals/${proposalId}`}
              >
                Kembali ke Proposal
              </Link>
              <Link
                className="rounded-md bg-slate-950 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800"
                to="/proposals"
              >
                Daftar Proposal
              </Link>
            </>
          }
          message={error}
          title="Setup project belum bisa dilanjutkan"
        />
      </div>
    )
  }

  return (
    <div className="mx-auto max-w-7xl">
      <div className="mb-4 flex items-center gap-2 text-sm font-medium text-slate-500">
        <Link className="hover:text-slate-950" to="/proposals">
          Proposal
        </Link>
        <span>/</span>
        <Link className="hover:text-slate-950" to={`/proposals/${proposal.id}`}>
          Proposal Detail
        </Link>
        <span>/</span>
        <span className="text-slate-950">Setup Project</span>
      </div>

      <section className="rounded-lg border border-slate-200 bg-white">
        <div className="flex flex-col gap-4 border-b border-slate-200 px-6 py-5 lg:flex-row lg:items-start lg:justify-between">
          <div>
            <p className="text-sm font-semibold text-slate-500">Setup Project</p>
            <h1 className="mt-1 text-3xl font-bold text-slate-950">Review Setup Project</h1>
            <p className="mt-2 text-sm text-slate-500">Review data proposal sebelum membuat project operasional.</p>
          </div>
          <div className="flex flex-wrap gap-2">
            <StatusBadge label="Disetujui" status="Approved" styles={proposalStatusStyles} />
            <StatusBadge label="Status Project: Setup" status="Draft" styles={proposalStatusStyles} />
          </div>
        </div>

        <form className="grid gap-4 p-6 lg:grid-cols-[minmax(0,1.25fr)_minmax(320px,0.75fr)]" onSubmit={handleSubmit}>
          <div className="space-y-4">
            <InfoCard title="Ringkasan Proposal">
              <div className="grid gap-5 md:grid-cols-2">
                <DetailItem label="Nomor Proposal" value={proposal.proposal_number} strong />
                <DetailItem label="Judul Proposal" value={proposal.proposal_title} strong />
                <DetailItem label="Jenis Riset" value={displayValue(proposal.research_type)} />
                <DetailItem label="Estimasi Nilai" value={formatCurrency(proposal.estimated_budget)} />
                <DetailItem label="Owner Proposal" value={proposal.proposal_owner?.full_name || '-'} />
                <DetailItem label="Tanggal Disetujui" value={formatDate(proposal.approved_at)} />
              </div>
            </InfoCard>

            <InfoCard title="Ringkasan Client">
              <div className="grid gap-5 md:grid-cols-2">
                <DetailItem label="Nama Client" value={client.client_name} strong />
                <DetailItem label="Industry" value={displayValue(client.industry)} />
                <DetailItem label="Kota" value={displayValue(client.city)} />
                <DetailItem label="Status Client" value={displayValue(client.status)} />
                <DetailItem label="PIC Utama" value={displayValue(contact?.contact_name)} />
                <DetailItem label="Email PIC" value={displayValue(contact?.email)} />
                <DetailItem label="Nomor HP" value={displayValue(contact?.mobile_phone || contact?.phone)} />
              </div>
            </InfoCard>

            <InfoCard title="Project Information" description="Nama project dapat disesuaikan sebelum Project dibuat.">
              <label className="block">
                <span className="text-sm font-semibold text-slate-700">Project Name *</span>
                <input
                  className={`mt-2 h-10 w-full rounded-md border px-3 text-sm outline-none focus:border-slate-950 ${
                    validationError ? 'border-red-300' : 'border-slate-300'
                  }`}
                  onChange={(event) => setProjectName(event.target.value)}
                  value={projectName}
                />
              </label>
              {validationError && <p className="mt-2 text-sm font-medium text-red-700">{validationError}</p>}
              <div className="mt-5 grid gap-5 md:grid-cols-2">
                <DetailItem label="Project Manager" value="Belum ditentukan" />
                <DetailItem label="Contract" value="Tidak wajib pada MVP" />
              </div>
            </InfoCard>
          </div>

          <aside className="space-y-4">
            <InfoCard title="Informasi Sistem">
              <div className="space-y-4">
                <DetailItem label="Project Number" value="Dibuat otomatis" />
                <DetailItem label="Status Awal" value="Setup" strong />
                <DetailItem label="Proposal Reference" value={proposal.proposal_number} />
                <DetailItem label="Created Date" value="Setelah Project dibuat" />
              </div>
            </InfoCard>

            <InfoCard title="Checklist Data">
              <ul className="space-y-3 text-sm font-medium text-slate-700">
                {[
                  'Client dibawa ke Project.',
                  'Proposal Reference disimpan.',
                  'Project Name dapat diubah sebelum simpan.',
                  'Research Type dibawa ke Project.',
                  'Estimasi nilai menjadi Project Value awal.',
                  'Proposal Owner menjadi referensi Business Development.',
                  'Status awal Project adalah Setup.',
                  'Contract tidak wajib pada MVP.',
                  'Project Manager optional.',
                ].map((item) => (
                  <li className="flex gap-2" key={item}>
                    <span className="text-emerald-600">✓</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </InfoCard>

            {error && (
              <div className="rounded-md bg-red-50 px-4 py-3 text-sm font-semibold text-red-700">{error}</div>
            )}

            <div className="rounded-lg border border-slate-200 bg-white p-5">
              <div className="flex flex-col gap-3">
                <Link
                  className="inline-flex h-10 items-center justify-center rounded-md border border-slate-300 px-4 text-sm font-semibold text-slate-700 hover:bg-slate-50"
                  to={`/proposals/${proposal.id}`}
                >
                  Batal
                </Link>
                <button
                  className="inline-flex h-10 items-center justify-center rounded-md bg-slate-950 px-4 text-sm font-semibold text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-300 disabled:text-slate-500"
                  disabled={isSubmitting}
                  type="submit"
                >
                  {isSubmitting ? 'Membuat Project...' : 'Buat Project'}
                </button>
              </div>
            </div>
          </aside>
        </form>
      </section>
    </div>
  )
}

export default ProjectSetupReviewPage
