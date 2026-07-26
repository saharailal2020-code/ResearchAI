import { useCallback, useEffect, useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import { getClient } from '../services/clients'
import { getProposal } from '../services/proposals'

const statusStyles = {
  Draft: 'bg-slate-100 text-slate-700 ring-slate-200',
  Sent: 'bg-sky-50 text-sky-700 ring-sky-200',
  Revised: 'bg-amber-50 text-amber-700 ring-amber-200',
  Approved: 'bg-emerald-50 text-emerald-700 ring-emerald-200',
  Rejected: 'bg-red-50 text-red-700 ring-red-200',
}

function statusLabel(status) {
  const labels = {
    Draft: 'Draft',
    Sent: 'Dikirim',
    Revised: 'Revisi',
    Approved: 'Disetujui',
    Rejected: 'Ditolak',
  }

  return labels[status] || status || '-'
}

function statusDescription(status) {
  const descriptions = {
    Draft: 'Proposal masih dalam tahap penyusunan internal.',
    Sent: 'Proposal sudah dikirim ke client dan menunggu keputusan.',
    Revised: 'Proposal membutuhkan revisi berdasarkan masukan client.',
    Approved: 'Proposal sudah disetujui dan siap untuk Project Setup.',
    Rejected: 'Proposal tidak dilanjutkan oleh client.',
  }

  return descriptions[status] || 'Status proposal belum dikenali.'
}

function formatCurrency(value) {
  if (value === null || value === undefined || value === '') {
    return '-'
  }

  return new Intl.NumberFormat('id-ID', {
    currency: 'IDR',
    maximumFractionDigits: 0,
    style: 'currency',
  }).format(Number(value))
}

function formatDate(value) {
  if (!value) {
    return '-'
  }

  return new Intl.DateTimeFormat('id-ID', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  }).format(new Date(value))
}

function displayValue(value) {
  return value || '-'
}

function primaryContact(client) {
  return client?.contacts?.find((contact) => contact.is_primary) || client?.contacts?.[0] || null
}

function DetailItem({ label, value, strong = false }) {
  return (
    <div>
      <p className="text-xs font-semibold uppercase text-slate-400">{label}</p>
      <p className={`mt-1 text-sm ${strong ? 'font-semibold text-slate-950' : 'font-medium text-slate-700'}`}>
        {value}
      </p>
    </div>
  )
}

function TextSection({ label, value }) {
  return (
    <div>
      <p className="text-sm font-semibold text-slate-950">{label}</p>
      <p className="mt-2 rounded-md bg-slate-50 px-4 py-3 text-sm leading-6 text-slate-700">
        {value || 'Belum diisi'}
      </p>
    </div>
  )
}

function ProposalDetailSkeleton() {
  return (
    <div className="mx-auto max-w-7xl animate-pulse space-y-4">
      <p className="text-sm font-medium text-slate-500">Memuat detail proposal...</p>
      <div className="h-4 w-56 rounded bg-slate-200" />
      <section className="rounded-lg border border-slate-200 bg-white p-6">
        <div className="h-5 w-48 rounded bg-slate-200" />
        <div className="mt-4 h-10 w-80 rounded bg-slate-200" />
        <div className="mt-5 grid gap-4 md:grid-cols-3">
          <div className="h-16 rounded bg-slate-100" />
          <div className="h-16 rounded bg-slate-100" />
          <div className="h-16 rounded bg-slate-100" />
        </div>
      </section>
      <div className="grid gap-4 lg:grid-cols-[minmax(0,1.3fr)_minmax(320px,0.7fr)]">
        <div className="h-72 rounded-lg border border-slate-200 bg-white" />
        <div className="h-72 rounded-lg border border-slate-200 bg-white" />
      </div>
    </div>
  )
}

function ProposalDetailPage() {
  const { proposalId } = useParams()
  const [proposal, setProposal] = useState(null)
  const [client, setClient] = useState(null)
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(true)

  const contact = useMemo(() => primaryContact(client), [client])

  const loadProposal = useCallback(async () => {
    setIsLoading(true)
    setError('')

    try {
      const proposalData = await getProposal(proposalId)
      setProposal(proposalData)

      try {
        const clientData = await getClient(proposalData.client_id)
        setClient(clientData)
      } catch {
        setClient(null)
      }
    } catch (requestError) {
      if (requestError?.response?.status === 404) {
        setError('Proposal tidak ditemukan. Proposal mungkin sudah dihapus atau ID tidak valid.')
      } else {
        setError('Tidak dapat mengambil detail proposal. Periksa koneksi server lalu coba lagi.')
      }
    } finally {
      setIsLoading(false)
    }
  }, [proposalId])

  useEffect(() => {
    loadProposal()
  }, [loadProposal])

  if (isLoading) {
    return <ProposalDetailSkeleton />
  }

  if (error) {
    return (
      <div className="mx-auto max-w-7xl">
        <div className="mb-4 flex items-center gap-2 text-sm font-medium text-slate-500">
          <Link className="hover:text-slate-950" to="/proposals">
            Proposal
          </Link>
          <span>/</span>
          <span className="text-slate-950">Proposal Detail</span>
        </div>

        <section className="rounded-lg border border-red-200 bg-white p-6">
          <p className="text-sm font-semibold text-red-700">Detail proposal belum bisa ditampilkan</p>
          <h2 className="mt-2 text-xl font-semibold text-slate-950">{error}</h2>
          <div className="mt-5 flex flex-wrap gap-3">
            <button
              className="rounded-md border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50"
              onClick={loadProposal}
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
          </div>
        </section>
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
        <span className="text-slate-950">Proposal Detail</span>
      </div>

      <section className="rounded-lg border border-slate-200 bg-white">
        <div className="flex flex-col gap-5 border-b border-slate-200 px-6 py-5 lg:flex-row lg:items-start lg:justify-between">
          <div>
            <Link className="text-sm font-medium text-slate-500 hover:text-slate-950" to="/proposals">
              Kembali ke Proposal
            </Link>
            <p className="mt-5 text-sm font-semibold uppercase text-slate-400">Nomor Proposal</p>
            <h1 className="mt-1 text-3xl font-bold tracking-normal text-slate-950 md:text-4xl">
              {proposal.proposal_number}
            </h1>
            <p className="mt-3 text-xl font-semibold text-slate-900">{proposal.proposal_title}</p>
            <p className="mt-2 text-sm text-slate-500">
              Client: {client?.client_name || proposal.client_id} | Owner:{' '}
              {proposal.proposal_owner?.full_name || proposal.proposal_owner?.email || '-'}
            </p>
          </div>
          <span
            className={`inline-flex w-fit rounded-full px-3 py-1 text-sm font-semibold ring-1 ${statusStyles[proposal.status] || statusStyles.Draft}`}
          >
            {statusLabel(proposal.status)}
          </span>
        </div>

        <div className="grid gap-4 p-6 lg:grid-cols-[minmax(0,1.25fr)_minmax(320px,0.75fr)]">
          <div className="space-y-4">
            <section className="rounded-lg border border-slate-200 bg-white p-5">
              <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
                <DetailItem label="Jenis Riset" value={displayValue(proposal.research_type)} strong />
                <DetailItem label="Estimasi Budget" value={formatCurrency(proposal.estimated_budget)} strong />
                <DetailItem label="Owner Proposal" value={proposal.proposal_owner?.full_name || proposal.proposal_owner?.email || '-'} />
                <DetailItem label="Tanggal Dibuat" value={formatDate(proposal.created_at)} />
                <DetailItem label="Terakhir Diperbarui" value={formatDate(proposal.updated_at)} />
                <DetailItem label="Tanggal Disetujui" value={formatDate(proposal.approved_at)} />
              </div>
            </section>

            <section className="space-y-4 rounded-lg border border-slate-200 bg-white p-5">
              <div>
                <p className="text-base font-semibold text-slate-950">Detail Riset</p>
                <p className="mt-1 text-sm text-slate-500">
                  Informasi ini dapat dilengkapi setelah draft proposal dibuat.
                </p>
              </div>
              <TextSection label="Objective Riset" value={proposal.research_objective} />
              <TextSection label="Ringkasan Metodologi" value={proposal.methodology_summary} />
              <TextSection label="Estimasi Timeline" value={proposal.estimated_timeline} />
            </section>

            <section className="rounded-lg border border-slate-200 bg-white p-5">
              <p className="text-base font-semibold text-slate-950">Status & Next Step</p>
              <p className="mt-2 text-sm leading-6 text-slate-600">{statusDescription(proposal.status)}</p>
              {proposal.status === 'Approved' && (
                <div className="mt-4 rounded-md bg-emerald-50 px-4 py-3 text-sm font-semibold text-emerald-700">
                  Siap untuk Project Setup. Project belum dibuat pada sprint ini.
                </div>
              )}
            </section>
          </div>

          <aside className="rounded-lg border border-slate-200 bg-white p-5">
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="text-sm font-semibold text-slate-500">Relasi Client</p>
                <h2 className="mt-1 text-lg font-semibold text-slate-950">{client?.client_name || '-'}</h2>
              </div>
              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-md bg-slate-100 text-base font-semibold text-slate-500">
                {(client?.client_name || 'C').slice(0, 1).toUpperCase()}
              </div>
            </div>

            <div className="mt-6 space-y-4">
              <DetailItem label="Kota" value={displayValue(client?.city)} />
              <DetailItem label="Industry" value={displayValue(client?.industry)} />
              <DetailItem label="PIC Utama" value={displayValue(contact?.contact_name)} />
              <DetailItem label="Email" value={displayValue(contact?.email)} />
              <DetailItem label="Telepon" value={displayValue(contact?.mobile_phone || contact?.phone || contact?.whatsapp_number)} />
            </div>

            {client?.id ? (
              <Link
                className="mt-6 inline-flex w-full justify-center rounded-md bg-slate-950 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800"
                to={`/clients/${client.id}`}
              >
                Lihat Client 360
              </Link>
            ) : (
              <p className="mt-6 rounded-md bg-slate-50 px-4 py-3 text-sm text-slate-500">
                Data client belum dapat dimuat.
              </p>
            )}
          </aside>
        </div>
      </section>
    </div>
  )
}

export default ProposalDetailPage
