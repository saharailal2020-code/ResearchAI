import { useCallback, useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import { createClient, getClients } from '../services/clients'

const statusOptions = [
  { label: 'All Status', value: '' },
  { label: 'Active', value: 'active' },
  { label: 'Archived', value: 'archived' },
]

const emptyForm = {
  client_name: '',
  industry: '',
  client_type: 'prospect',
  contact_name: '',
  position: '',
  email: '',
  phone: '',
  notes: '',
}

function ClientsPage() {
  const [clients, setClients] = useState([])
  const [search, setSearch] = useState('')
  const [status, setStatus] = useState('')
  const [form, setForm] = useState(emptyForm)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)

  const query = useMemo(
    () => ({
      search: search.trim() || undefined,
      status: status || undefined,
    }),
    [search, status],
  )

  const loadClients = useCallback(async () => {
    setIsLoading(true)
    setError('')

    try {
      const data = await getClients(query)
      setClients(data)
    } catch {
      setError('Data client belum bisa dimuat. Pastikan backend sedang berjalan.')
    } finally {
      setIsLoading(false)
    }
  }, [query])

  useEffect(() => {
    loadClients()
  }, [loadClients])

  function updateForm(field, value) {
    setForm((current) => ({ ...current, [field]: value }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    setSuccess('')

    if (!form.client_name.trim()) {
      setError('Nama client wajib diisi.')
      return
    }

    setIsSaving(true)

    const payload = {
      client_name: form.client_name.trim(),
      industry: form.industry.trim() || null,
      client_type: form.client_type,
      notes: form.notes.trim() || null,
      primary_contact: form.contact_name.trim()
        ? {
            contact_name: form.contact_name.trim(),
            position: form.position.trim() || null,
            email: form.email.trim() || null,
            phone: form.phone.trim() || null,
            notes: null,
          }
        : null,
    }

    try {
      await createClient(payload)
      setForm(emptyForm)
      setSuccess('Client baru berhasil disimpan.')
      await loadClients()
    } catch {
      setError('Client belum berhasil disimpan. Cek nama, email contact, atau koneksi backend.')
    } finally {
      setIsSaving(false)
    }
  }

  return (
    <div className="mx-auto grid max-w-7xl gap-6 xl:grid-cols-[minmax(0,1fr)_420px]">
      <section className="rounded-lg border border-slate-200 bg-white">
        <div className="border-b border-slate-200 px-5 py-4">
          <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <p className="text-sm font-medium text-slate-500">Client Management</p>
              <h2 className="mt-1 text-lg font-semibold text-slate-950">Client List</h2>
            </div>
            <div className="flex flex-col gap-2 sm:flex-row">
              <input
                className="h-10 rounded-md border border-slate-300 px-3 text-sm outline-none focus:border-slate-950"
                onChange={(event) => setSearch(event.target.value)}
                placeholder="Search clients"
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
            </div>
          </div>
        </div>

        {error && (
          <div className="mx-5 mt-4 rounded-md bg-red-50 px-3 py-2 text-sm font-medium text-red-700">
            {error}
          </div>
        )}

        {success && (
          <div className="mx-5 mt-4 rounded-md bg-emerald-50 px-3 py-2 text-sm font-medium text-emerald-700">
            {success}
          </div>
        )}

        <div className="divide-y divide-slate-200">
          {isLoading ? (
            <div className="px-5 py-8 text-sm font-medium text-slate-500">Loading clients...</div>
          ) : clients.length === 0 ? (
            <div className="px-5 py-8 text-sm text-slate-500">
              Belum ada client. Tambahkan client pertama dari form di sebelah kanan.
            </div>
          ) : (
            clients.map((client) => (
              <div
                className="grid gap-3 px-5 py-4 hover:bg-slate-50 lg:grid-cols-[minmax(0,1fr)_160px_120px]"
                key={client.id}
              >
                <div>
                  <Link className="font-semibold text-slate-950 hover:text-slate-700" to={`/clients/${client.id}`}>
                    {client.client_name}
                  </Link>
                  <p className="mt-1 text-sm text-slate-500">
                    {[client.industry || 'Industry not set', client.city].filter(Boolean).join(' • ')}
                  </p>
                </div>
                <div>
                  <p className="text-xs font-medium uppercase text-slate-400">Type</p>
                  <p className="mt-1 text-sm font-medium capitalize text-slate-700">{client.client_type}</p>
                </div>
                <div>
                  <p className="text-xs font-medium uppercase text-slate-400">Status</p>
                  <span className="mt-1 inline-flex rounded-full bg-emerald-50 px-2.5 py-1 text-xs font-semibold capitalize text-emerald-700">
                    {client.status}
                  </span>
                </div>
              </div>
            ))
          )}
        </div>
      </section>

      <section className="rounded-lg border border-slate-200 bg-white p-5">
        <div>
          <p className="text-sm font-medium text-slate-500">New Client</p>
          <h2 className="mt-1 text-lg font-semibold text-slate-950">Add Client</h2>
        </div>

        <form className="mt-5 space-y-4" onSubmit={handleSubmit}>
          <label className="block">
            <span className="text-sm font-medium text-slate-700">Client Name</span>
            <input
              className="mt-1 h-10 w-full rounded-md border border-slate-300 px-3 text-sm outline-none focus:border-slate-950"
              onChange={(event) => updateForm('client_name', event.target.value)}
              value={form.client_name}
            />
          </label>

          <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-1">
            <label className="block">
              <span className="text-sm font-medium text-slate-700">Industry</span>
              <input
                className="mt-1 h-10 w-full rounded-md border border-slate-300 px-3 text-sm outline-none focus:border-slate-950"
                onChange={(event) => updateForm('industry', event.target.value)}
                value={form.industry}
              />
            </label>

            <label className="block">
              <span className="text-sm font-medium text-slate-700">Client Type</span>
              <select
                className="mt-1 h-10 w-full rounded-md border border-slate-300 px-3 text-sm outline-none focus:border-slate-950"
                onChange={(event) => updateForm('client_type', event.target.value)}
                value={form.client_type}
              >
                <option value="prospect">Prospect</option>
                <option value="active_client">Active Client</option>
                <option value="partner">Partner</option>
              </select>
            </label>
          </div>

          <div className="border-t border-slate-200 pt-4">
            <p className="text-sm font-semibold text-slate-950">Primary Contact</p>
            <div className="mt-3 space-y-4">
              <input
                className="h-10 w-full rounded-md border border-slate-300 px-3 text-sm outline-none focus:border-slate-950"
                onChange={(event) => updateForm('contact_name', event.target.value)}
                placeholder="Contact name"
                value={form.contact_name}
              />
              <input
                className="h-10 w-full rounded-md border border-slate-300 px-3 text-sm outline-none focus:border-slate-950"
                onChange={(event) => updateForm('position', event.target.value)}
                placeholder="Position"
                value={form.position}
              />
              <input
                className="h-10 w-full rounded-md border border-slate-300 px-3 text-sm outline-none focus:border-slate-950"
                onChange={(event) => updateForm('email', event.target.value)}
                placeholder="Email"
                type="email"
                value={form.email}
              />
              <input
                className="h-10 w-full rounded-md border border-slate-300 px-3 text-sm outline-none focus:border-slate-950"
                onChange={(event) => updateForm('phone', event.target.value)}
                placeholder="Phone"
                value={form.phone}
              />
            </div>
          </div>

          <label className="block">
            <span className="text-sm font-medium text-slate-700">Notes</span>
            <textarea
              className="mt-1 min-h-24 w-full resize-y rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-slate-950"
              onChange={(event) => updateForm('notes', event.target.value)}
              value={form.notes}
            />
          </label>

          <button
            className="h-11 w-full rounded-md bg-slate-950 text-sm font-semibold text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-400"
            disabled={isSaving}
            type="submit"
          >
            {isSaving ? 'Saving client...' : 'Save Client'}
          </button>
        </form>
      </section>
    </div>
  )
}

export default ClientsPage
