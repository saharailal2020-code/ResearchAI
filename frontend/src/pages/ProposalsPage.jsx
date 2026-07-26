import { useCallback, useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import { getClients } from '../services/clients'
import { getProposals } from '../services/proposals'

const statusOptions = [
  { label: 'Semua Status', value: '' },
  { label: 'Draft', value: 'Draft' },
  { label: 'Dikirim ke Client', value: 'Sent' },
  { label: 'Revisi', value: 'Revised' },
  { label: 'Disetujui', value: 'Approved' },
  { label: 'Ditolak', value: 'Rejected' },
]

const sortOptions = [
  { label: 'Tanggal dibuat terbaru', value: 'created_desc' },
  { label: 'Tanggal dibuat terlama', value: 'created_asc' },
  { label: 'Budget terbesar', value: 'budget_desc' },
  { label: 'Budget terkecil', value: 'budget_asc' },
  { label: 'Status A-Z', value: 'status_asc' },
]

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

function formatCurrency(value) {
  const amount = Number(value || 0)
  return new Intl.NumberFormat('id-ID', {
    currency: 'IDR',
    maximumFractionDigits: 0,
    style: 'currency',
  }).format(amount)
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

function sortProposals(proposals, sortBy) {
  return [...proposals].sort((first, second) => {
    if (sortBy === 'created_asc') {
      return new Date(first.created_at) - new Date(second.created_at)
    }
    if (sortBy === 'budget_desc') {
      return Number(second.estimated_budget || 0) - Number(first.estimated_budget || 0)
    }
    if (sortBy === 'budget_asc') {
      return Number(first.estimated_budget || 0) - Number(second.estimated_budget || 0)
    }
    if (sortBy === 'status_asc') {
      return statusLabel(first.status).localeCompare(statusLabel(second.status), 'id-ID')
    }

    return new Date(second.created_at) - new Date(first.created_at)
  })
}

function ProposalsPage() {
  const [proposals, setProposals] = useState([])
  const [clients, setClients] = useState([])
  const [search, setSearch] = useState('')
  const [status, setStatus] = useState('')
  const [clientId, setClientId] = useState('')
  const [researchType, setResearchType] = useState('')
  const [sortBy, setSortBy] = useState('created_desc')
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(true)

  const query = useMemo(
    () => ({
      client_id: clientId || undefined,
      research_type: researchType.trim() || undefined,
      search: search.trim() || undefined,
      status: status || undefined,
    }),
    [clientId, researchType, search, status],
  )

  const loadData = useCallback(async () => {
    setIsLoading(true)
    setError('')

    try {
      const [proposalData, clientData] = await Promise.all([getProposals(query), getClients()])
      setProposals(proposalData)
      setClients(clientData)
    } catch {
      setError('Data proposal belum bisa dimuat. Pastikan backend sedang berjalan.')
    } finally {
      setIsLoading(false)
    }
  }, [query])

  useEffect(() => {
    loadData()
  }, [loadData])

  const sortedProposals = useMemo(() => sortProposals(proposals, sortBy), [proposals, sortBy])

  return (
    <div className="mx-auto max-w-7xl">
      <section className="rounded-lg border border-slate-200 bg-white">
        <div className="border-b border-slate-200 px-5 py-4">
          <div className="space-y-4">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
              <div>
                <p className="text-sm font-medium text-slate-500">Manajemen Proposal</p>
                <h2 className="mt-1 text-lg font-semibold text-slate-950">Daftar Proposal</h2>
              </div>
              <button
                className="h-10 shrink-0 whitespace-nowrap rounded-md bg-slate-950 px-4 text-sm font-semibold text-white hover:bg-slate-800"
                type="button"
              >
                + Proposal Baru
              </button>
            </div>

            <div className="grid gap-2 md:grid-cols-2 xl:grid-cols-[minmax(220px,1fr)_160px_minmax(220px,1fr)_180px_220px]">
              <input
                className="h-10 rounded-md border border-slate-300 px-3 text-sm outline-none focus:border-slate-950"
                onChange={(event) => setSearch(event.target.value)}
                placeholder="Cari proposal"
                type="search"
                value={search}
              />
              <select
                className="h-10 rounded-md border border-slate-300 px-3 text-sm outline-none focus:border-slate-950"
                onChange={(event) => setStatus(event.target.value)}
                value={status}
              >
                {statusOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
              <select
                className="h-10 rounded-md border border-slate-300 px-3 text-sm outline-none focus:border-slate-950"
                onChange={(event) => setClientId(event.target.value)}
                value={clientId}
              >
                <option value="">Semua Client</option>
                {clients.map((client) => (
                  <option key={client.id} value={client.id}>
                    {client.client_name}
                  </option>
                ))}
              </select>
              <input
                className="h-10 rounded-md border border-slate-300 px-3 text-sm outline-none focus:border-slate-950"
                onChange={(event) => setResearchType(event.target.value)}
                placeholder="Filter jenis riset"
                value={researchType}
              />
              <select
                className="h-10 rounded-md border border-slate-300 px-3 text-sm outline-none focus:border-slate-950"
                onChange={(event) => setSortBy(event.target.value)}
                value={sortBy}
              >
                {sortOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {error && (
          <div className="mx-5 mt-4 rounded-md bg-red-50 px-3 py-2 text-sm font-medium text-red-700">
            {error}
          </div>
        )}

        {isLoading ? (
          <div className="px-5 py-8 text-sm font-medium text-slate-500">Memuat data proposal...</div>
        ) : sortedProposals.length === 0 ? (
          <div className="px-5 py-12 text-center">
            <p className="text-base font-semibold text-slate-950">Belum ada proposal</p>
            <p className="mt-2 text-sm text-slate-500">
              Proposal yang dibuat dari backend akan tampil di sini sebagai entry point Proposal Management.
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-[1240px] w-full border-collapse text-left">
              <thead>
                <tr className="border-b border-slate-200 bg-slate-50 text-xs font-semibold uppercase text-slate-400">
                  <th className="px-5 py-3">Nomor</th>
                  <th className="px-5 py-3">Judul Proposal</th>
                  <th className="px-5 py-3">Client</th>
                  <th className="px-5 py-3">Jenis Riset</th>
                  <th className="px-5 py-3">Estimasi Budget</th>
                  <th className="px-5 py-3">Owner</th>
                  <th className="px-5 py-3">Status</th>
                  <th className="px-5 py-3">Tanggal Dibuat</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200">
                {sortedProposals.map((proposal) => (
                  <tr className="hover:bg-slate-50" key={proposal.id}>
                    <td className="whitespace-nowrap px-5 py-4 text-sm font-semibold text-slate-800">
                      {proposal.proposal_number}
                    </td>
                    <td className="px-5 py-4">
                      <Link className="text-sm font-semibold text-slate-950 hover:text-slate-700" to={`/proposals/${proposal.id}`}>
                        {proposal.proposal_title}
                      </Link>
                    </td>
                    <td className="px-5 py-4 text-sm font-medium text-slate-700">{proposal.client_name}</td>
                    <td className="px-5 py-4 text-sm text-slate-600">{proposal.research_type || '-'}</td>
                    <td className="px-5 py-4 text-sm font-medium text-slate-800">{formatCurrency(proposal.estimated_budget)}</td>
                    <td className="px-5 py-4 text-sm text-slate-600">
                      {proposal.proposal_owner?.full_name || proposal.proposal_owner?.email || '-'}
                    </td>
                    <td className="px-5 py-4">
                      <span className={`inline-flex rounded-full px-2.5 py-1 text-xs font-semibold ring-1 ${statusStyles[proposal.status] || statusStyles.Draft}`}>
                        {statusLabel(proposal.status)}
                      </span>
                    </td>
                    <td className="px-5 py-4 text-sm text-slate-600">{formatDate(proposal.created_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  )
}

export default ProposalsPage
