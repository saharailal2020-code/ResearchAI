import { useCallback, useEffect, useState } from 'react'
import { Link, useNavigate, useOutletContext } from 'react-router-dom'

import { getClients } from '../services/clients'
import { createProposal } from '../services/proposals'

const researchTypeOptions = [
  'Quantitative',
  'Qualitative',
  'Mystery Shopping',
  'FGD',
  'IDI',
  'Desk Research',
  'Market Assessment',
  'Customer Satisfaction',
  'Brand Health',
  'Tracking',
  'Social Research',
  'Other',
]

function SystemInfoItem({ label, value }) {
  return (
    <div>
      <p className="text-xs font-semibold uppercase text-slate-400">{label}</p>
      <p className="mt-1 text-sm font-medium text-slate-700">{value}</p>
    </div>
  )
}

function formatCurrencyPreview(value) {
  const numericValue = Number(value || 0)

  return new Intl.NumberFormat('id-ID', {
    currency: 'IDR',
    maximumFractionDigits: 0,
    style: 'currency',
  }).format(numericValue)
}

function validateForm(form) {
  const errors = {}
  const title = form.proposalTitle.trim()
  const budgetValue = form.estimatedBudget.trim()

  if (!form.clientId) {
    errors.clientId = 'Client wajib dipilih.'
  }

  if (!title) {
    errors.proposalTitle = 'Judul proposal wajib diisi.'
  } else if (title.length < 3) {
    errors.proposalTitle = 'Judul proposal minimal 3 karakter.'
  } else if (title.length > 150) {
    errors.proposalTitle = 'Judul proposal maksimal 150 karakter.'
  }

  if (budgetValue) {
    const amount = Number(budgetValue)
    if (Number.isNaN(amount) || amount < 0) {
      errors.estimatedBudget = 'Estimasi nilai proposal harus berupa angka dan tidak boleh negatif.'
    }
  }

  return errors
}

function ProposalCreatePage() {
  const navigate = useNavigate()
  const { user } = useOutletContext()
  const [clients, setClients] = useState([])
  const [form, setForm] = useState({
    clientId: '',
    estimatedBudget: '',
    proposalTitle: '',
    researchType: '',
  })
  const [fieldErrors, setFieldErrors] = useState({})
  const [loadError, setLoadError] = useState('')
  const [submitError, setSubmitError] = useState('')
  const [isLoadingClients, setIsLoadingClients] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const loadClients = useCallback(async () => {
    setIsLoadingClients(true)
    setLoadError('')

    try {
      const clientData = await getClients()
      setClients(clientData)
    } catch {
      setLoadError('Daftar client belum bisa dimuat. Pastikan backend sedang berjalan.')
    } finally {
      setIsLoadingClients(false)
    }
  }, [])

  useEffect(() => {
    loadClients()
  }, [loadClients])

  function updateField(fieldName, value) {
    setForm((currentForm) => ({ ...currentForm, [fieldName]: value }))
    setFieldErrors((currentErrors) => ({ ...currentErrors, [fieldName]: '' }))
    setSubmitError('')
  }

  async function handleSubmit(event) {
    event.preventDefault()
    const validationErrors = validateForm(form)
    setFieldErrors(validationErrors)
    setSubmitError('')

    if (Object.keys(validationErrors).length > 0) {
      return
    }

    setIsSubmitting(true)

    try {
      const payload = {
        client_id: form.clientId,
        estimated_budget: form.estimatedBudget.trim() ? Number(form.estimatedBudget) : null,
        proposal_title: form.proposalTitle.trim(),
        research_type: form.researchType || null,
      }
      const proposal = await createProposal(payload)
      navigate(`/proposals/${proposal.id}`)
    } catch {
      setSubmitError('Proposal belum bisa disimpan. Silakan coba lagi.')
    } finally {
      setIsSubmitting(false)
    }
  }

  const isEmpty = !isLoadingClients && !loadError && clients.length === 0

  return (
    <div className="mx-auto max-w-7xl">
      <div className="mb-4 flex items-center gap-2 text-sm font-medium text-slate-500">
        <Link className="hover:text-slate-950" to="/proposals">
          Proposal
        </Link>
        <span>/</span>
        <span className="text-slate-950">Proposal Baru</span>
      </div>

      <section className="mb-4 rounded-lg border border-slate-200 bg-white p-5">
        <p className="text-sm font-medium text-slate-500">Manajemen Proposal</p>
        <h2 className="mt-1 text-xl font-semibold text-slate-950">Proposal Baru</h2>
        <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-600">
          Buat draft proposal baru untuk client. Proposal belum dikirim ke client sampai Anda menjalankan Status
          Action dari halaman detail.
        </p>
      </section>

      {isLoadingClients ? (
        <section className="rounded-lg border border-slate-200 bg-white p-6">
          <p className="text-sm font-medium text-slate-500">Memuat daftar client...</p>
          <div className="mt-5 grid gap-4 lg:grid-cols-[minmax(0,1fr)_320px]">
            <div className="h-80 animate-pulse rounded-md bg-slate-100" />
            <div className="h-80 animate-pulse rounded-md bg-slate-100" />
          </div>
        </section>
      ) : loadError ? (
        <section className="rounded-lg border border-red-200 bg-white p-6">
          <p className="text-sm font-semibold text-red-700">{loadError}</p>
          <div className="mt-5 flex flex-wrap gap-3">
            <button
              className="rounded-md border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50"
              onClick={loadClients}
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
      ) : isEmpty ? (
        <section className="rounded-lg border border-slate-200 bg-white p-10 text-center">
          <p className="text-base font-semibold text-slate-950">Belum ada client</p>
          <p className="mt-2 text-sm text-slate-500">Buat client terlebih dahulu sebelum membuat proposal.</p>
          <Link
            className="mt-5 inline-flex rounded-md bg-slate-950 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800"
            to="/clients"
          >
            Kembali ke Client
          </Link>
        </section>
      ) : (
        <form className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_340px]" onSubmit={handleSubmit}>
          <section className="rounded-lg border border-slate-200 bg-white">
            <div className="border-b border-slate-200 px-5 py-4">
              <h3 className="text-base font-semibold text-slate-950">Informasi Proposal</h3>
              <p className="mt-1 text-sm text-slate-500">Isi informasi minimum untuk menyimpan draft proposal.</p>
            </div>

            <div className="space-y-5 p-5">
              {submitError && (
                <div className="rounded-md bg-red-50 px-4 py-3 text-sm font-semibold text-red-700">
                  {submitError}
                </div>
              )}

              <label className="block">
                <span className="text-sm font-semibold text-slate-700">Client *</span>
                <select
                  className={`mt-1 h-11 w-full rounded-md border px-3 text-sm outline-none focus:border-slate-950 ${
                    fieldErrors.clientId ? 'border-red-300' : 'border-slate-300'
                  }`}
                  onChange={(event) => updateField('clientId', event.target.value)}
                  value={form.clientId}
                >
                  <option value="">Pilih Client</option>
                  {clients.map((client) => (
                    <option key={client.id} value={client.id}>
                      {client.client_name}
                    </option>
                  ))}
                </select>
                {fieldErrors.clientId && <p className="mt-1 text-sm font-medium text-red-600">{fieldErrors.clientId}</p>}
              </label>

              <label className="block">
                <span className="text-sm font-semibold text-slate-700">Proposal Title *</span>
                <input
                  className={`mt-1 h-11 w-full rounded-md border px-3 text-sm outline-none focus:border-slate-950 ${
                    fieldErrors.proposalTitle ? 'border-red-300' : 'border-slate-300'
                  }`}
                  maxLength={150}
                  onChange={(event) => updateField('proposalTitle', event.target.value)}
                  placeholder="Masukkan judul proposal"
                  value={form.proposalTitle}
                />
                {fieldErrors.proposalTitle && (
                  <p className="mt-1 text-sm font-medium text-red-600">{fieldErrors.proposalTitle}</p>
                )}
              </label>

              <div className="grid gap-5 md:grid-cols-2">
                <label className="block">
                  <span className="text-sm font-semibold text-slate-700">Research Type</span>
                  <select
                    className="mt-1 h-11 w-full rounded-md border border-slate-300 px-3 text-sm outline-none focus:border-slate-950"
                    onChange={(event) => updateField('researchType', event.target.value)}
                    value={form.researchType}
                  >
                    <option value="">Pilih jenis riset</option>
                    {researchTypeOptions.map((option) => (
                      <option key={option} value={option}>
                        {option}
                      </option>
                    ))}
                  </select>
                </label>

                <label className="block">
                  <span className="text-sm font-semibold text-slate-700">Estimasi Nilai Proposal (Rp)</span>
                  <input
                    className={`mt-1 h-11 w-full rounded-md border px-3 text-sm outline-none focus:border-slate-950 ${
                      fieldErrors.estimatedBudget ? 'border-red-300' : 'border-slate-300'
                    }`}
                    min="0"
                    onChange={(event) => updateField('estimatedBudget', event.target.value)}
                    placeholder="25000000"
                    type="number"
                    value={form.estimatedBudget}
                  />
                  {form.estimatedBudget && !fieldErrors.estimatedBudget && (
                    <p className="mt-1 text-xs font-medium text-slate-500">
                      Preview: {formatCurrencyPreview(form.estimatedBudget)}
                    </p>
                  )}
                  {fieldErrors.estimatedBudget && (
                    <p className="mt-1 text-sm font-medium text-red-600">{fieldErrors.estimatedBudget}</p>
                  )}
                </label>
              </div>

              <div className="flex flex-col-reverse gap-3 border-t border-slate-200 pt-5 sm:flex-row sm:justify-end">
                <Link
                  className="inline-flex h-10 items-center justify-center rounded-md border border-slate-300 px-4 text-sm font-semibold text-slate-700 hover:bg-slate-50"
                  to="/proposals"
                >
                  Batal
                </Link>
                <button
                  className="inline-flex h-10 items-center justify-center rounded-md bg-slate-950 px-4 text-sm font-semibold text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-300 disabled:text-slate-500"
                  disabled={isSubmitting}
                  type="submit"
                >
                  {isSubmitting ? 'Menyimpan...' : 'Simpan Draft'}
                </button>
              </div>
            </div>
          </section>

          <aside className="rounded-lg border border-slate-200 bg-white p-5">
            <h3 className="text-base font-semibold text-slate-950">Informasi Sistem</h3>
            <p className="mt-1 text-sm leading-6 text-slate-500">
              Informasi ini dibuat otomatis setelah proposal disimpan sebagai draft.
            </p>

            <div className="mt-6 space-y-4">
              <SystemInfoItem label="Proposal Number" value="Dibuat otomatis" />
              <SystemInfoItem label="Proposal Owner" value={user?.full_name || user?.email || '-'} />
              <SystemInfoItem label="Status" value="Draft" />
              <SystemInfoItem label="Created Date" value="Setelah disimpan" />
              <SystemInfoItem label="Updated Date" value="Setelah disimpan" />
            </div>
          </aside>
        </form>
      )}
    </div>
  )
}

export default ProposalCreatePage
