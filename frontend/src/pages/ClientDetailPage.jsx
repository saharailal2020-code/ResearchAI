import { useCallback, useEffect, useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import {
  createClientContact,
  deleteClientContact,
  getClient,
  getClientActivities,
  setPrimaryClientContact,
  updateClientContact,
} from '../services/clients'
import { getProposals } from '../services/proposals'

const tabs = [
  { key: 'Overview', label: 'Ringkasan' },
  { key: 'Contacts', label: 'Kontak' },
  { key: 'Activities', label: 'Aktivitas' },
  { key: 'Proposals', label: 'Proposal' },
  { key: 'Projects', label: 'Project' },
  { key: 'Documents', label: 'Dokumen' },
]

const emptyContactForm = {
  contact_name: '',
  position: '',
  email: '',
  phone: '',
  mobile_phone: '',
  whatsapp_number: '',
  contact_type: '',
  is_primary: false,
  is_decision_maker: false,
  notes: '',
}

const statusStyles = {
  active: 'bg-emerald-50 text-emerald-700 ring-emerald-200',
  prospect: 'bg-amber-50 text-amber-700 ring-amber-200',
  negotiation: 'bg-sky-50 text-sky-700 ring-sky-200',
  dormant: 'bg-orange-50 text-orange-700 ring-orange-200',
  inactive: 'bg-red-50 text-red-700 ring-red-200',
}

function normalizeStatus(status) {
  return String(status || 'Prospect').toLowerCase().replace('_', ' ')
}

function statusLabel(status) {
  const normalized = normalizeStatus(status)
  const labels = {
    active: 'Aktif',
    prospect: 'Prospek',
    negotiation: 'Negosiasi',
    dormant: 'Dormant',
    inactive: 'Tidak Aktif',
    draft: 'Draft',
    sent: 'Dikirim',
    revised: 'Revisi',
    approved: 'Disetujui',
    rejected: 'Ditolak',
  }

  return (
    labels[normalized] ||
    normalized
      .split(' ')
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ')
  )
}

function clientTypeLabel(type) {
  const normalized = String(type || '').toLowerCase()
  const labels = {
    prospect: 'Prospek',
    active_client: 'Client Aktif',
    partner: 'Partner',
    enterprise: 'Enterprise',
  }

  return labels[normalized] || type || null
}

function translateActivityTitle(title) {
  const labels = {
    'Proposal approved': 'Proposal disetujui',
    'Proposal marked for revision': 'Proposal perlu revisi',
    'Proposal sent to client': 'Proposal dikirim ke client',
    'Proposal updated': 'Proposal diperbarui',
    'Proposal created': 'Proposal dibuat',
    'Proposal rejected': 'Proposal ditolak',
    'Contact person added': 'Contact person ditambahkan',
    'Contact person updated': 'Contact person diperbarui',
    'Contact person deleted': 'Contact person dihapus',
  }

  return labels[title] || title
}

function translateActivityDescription(description) {
  if (!description) {
    return description
  }

  return description
    .replace(/^(.+) was approved\.$/, 'Proposal $1 telah disetujui.')
    .replace(/^(.+) requires revision\.$/, 'Proposal $1 perlu direvisi.')
    .replace(/^(.+) was sent to client\.$/, 'Proposal $1 telah dikirim ke client.')
    .replace(/^(.+) details were updated\.$/, 'Detail proposal $1 telah diperbarui.')
    .replace(/^(.+) was created\.$/, 'Proposal $1 telah dibuat.')
    .replace(/^(.+) was rejected\.$/, 'Proposal $1 telah ditolak.')
    .replace(/^(.+) was added as a client contact\.$/, '$1 ditambahkan sebagai contact person client.')
    .replace(/^(.+) contact details were updated\.$/, 'Detail contact person $1 telah diperbarui.')
    .replace(/^(.+) was removed from client contacts\.$/, '$1 dihapus dari daftar contact person client.')
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

function formatCurrency(value) {
  const amount = Number(value || 0)
  return new Intl.NumberFormat('id-ID', {
    currency: 'IDR',
    maximumFractionDigits: 0,
    style: 'currency',
  }).format(amount)
}

function isValidPhone(value) {
  if (!value) {
    return true
  }

  return /^\+?[0-9][0-9\s().-]{6,24}$/.test(value)
}

function InfoItem({ label, value }) {
  const displayValue = value === null || value === undefined || value === '' ? '-' : value

  return (
    <div>
      <p className="text-xs font-medium uppercase text-slate-400">{label}</p>
      <p className="mt-1 text-sm font-semibold text-slate-900">{displayValue}</p>
    </div>
  )
}

function ClientLogo({ client }) {
  const [hasImageError, setHasImageError] = useState(false)
  const shouldShowImage = client.logo_url && !hasImageError

  return (
    <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-lg bg-slate-100 text-lg font-semibold text-slate-500">
      {shouldShowImage ? (
        <img
          alt=""
          className="h-full w-full rounded-lg object-cover"
          onError={() => setHasImageError(true)}
          src={client.logo_url}
        />
      ) : (
        client.client_name.charAt(0).toUpperCase()
      )}
    </div>
  )
}

function EmptyState({ children }) {
  return (
    <div className="rounded-lg border border-dashed border-slate-300 bg-slate-50 px-5 py-8 text-center text-sm font-medium text-slate-500">
      {children}
    </div>
  )
}

function ClientDetailPage() {
  const { clientId } = useParams()
  const [activeTab, setActiveTab] = useState('Overview')
  const [client, setClient] = useState(null)
  const [proposals, setProposals] = useState([])
  const [activities, setActivities] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [contactForm, setContactForm] = useState(emptyContactForm)
  const [editingContactId, setEditingContactId] = useState(null)
  const [contactError, setContactError] = useState('')
  const [contactSuccess, setContactSuccess] = useState('')
  const [isSavingContact, setIsSavingContact] = useState(false)

  const loadClientDetail = useCallback(async ({ showLoading = true } = {}) => {
    if (showLoading) {
      setIsLoading(true)
    }
    setError('')

    try {
      const [clientData, proposalData, activityData] = await Promise.all([
        getClient(clientId),
        getProposals({ client_id: clientId }),
        getClientActivities(clientId),
      ])

      setClient(clientData)
      setProposals(proposalData)
      setActivities(activityData)
    } catch {
      setError('Client detail belum bisa dimuat. Pastikan backend sedang berjalan.')
    } finally {
      setIsLoading(false)
    }
  }, [clientId])

  useEffect(() => {
    loadClientDetail()
  }, [loadClientDetail])

  function updateContactForm(field, value) {
    setContactForm((current) => ({ ...current, [field]: value }))
  }

  function resetContactForm() {
    setContactForm(emptyContactForm)
    setEditingContactId(null)
  }

  function startEditContact(contact) {
    setContactError('')
    setContactSuccess('')
    setEditingContactId(contact.id)
    setContactForm({
      contact_name: contact.contact_name || '',
      position: contact.position || '',
      email: contact.email || '',
      phone: contact.phone || '',
      mobile_phone: contact.mobile_phone || '',
      whatsapp_number: contact.whatsapp_number || '',
      contact_type: contact.contact_type || '',
      is_primary: Boolean(contact.is_primary),
      is_decision_maker: Boolean(contact.is_decision_maker),
      notes: contact.notes || '',
    })
  }

  function buildContactPayload() {
    return {
      contact_name: contactForm.contact_name.trim(),
      position: contactForm.position.trim() || null,
      email: contactForm.email.trim() || null,
      phone: contactForm.phone.trim() || null,
      mobile_phone: contactForm.mobile_phone.trim() || null,
      whatsapp_number: contactForm.whatsapp_number.trim() || null,
      contact_type: contactForm.contact_type.trim() || null,
      is_primary: contactForm.is_primary,
      is_decision_maker: contactForm.is_decision_maker,
      notes: contactForm.notes.trim() || null,
    }
  }

  async function handleContactSubmit(event) {
    event.preventDefault()
    setContactError('')
    setContactSuccess('')

    if (!contactForm.contact_name.trim()) {
      setContactError('Nama contact wajib diisi.')
      return
    }

    if (![contactForm.phone, contactForm.mobile_phone, contactForm.whatsapp_number].every(isValidPhone)) {
      setContactError('Nomor telepon/HP belum sesuai format.')
      return
    }

    setIsSavingContact(true)

    try {
      const payload = buildContactPayload()
      if (editingContactId) {
        await updateClientContact(clientId, editingContactId, payload)
        setContactSuccess('Contact person berhasil diperbarui.')
      } else {
        await createClientContact(clientId, payload)
        setContactSuccess('Contact person berhasil ditambahkan.')
      }
      resetContactForm()
      await loadClientDetail({ showLoading: false })
    } catch {
      setContactError('Contact person belum berhasil disimpan. Cek email, nomor HP, atau koneksi backend.')
    } finally {
      setIsSavingContact(false)
    }
  }

  async function handleSetPrimary(contactId) {
    setContactError('')
    setContactSuccess('')

    try {
      await setPrimaryClientContact(clientId, contactId)
      setContactSuccess('Contact person utama berhasil diperbarui.')
      await loadClientDetail({ showLoading: false })
    } catch {
      setContactError('Contact person utama belum berhasil diperbarui.')
    }
  }

  async function handleDeleteContact(contactId) {
    setContactError('')
    setContactSuccess('')

    try {
      await deleteClientContact(clientId, contactId)
      if (editingContactId === contactId) {
        resetContactForm()
      }
      setContactSuccess('Contact person berhasil dihapus.')
      await loadClientDetail({ showLoading: false })
    } catch {
      setContactError('Contact person belum berhasil dihapus.')
    }
  }

  const primaryContact = useMemo(() => {
    if (!client?.contacts?.length) {
      return null
    }

    return client.contacts.find((contact) => contact.is_primary) || client.contacts[0]
  }, [client])

  const totalContractValue = useMemo(
    () =>
      proposals
        .filter((proposal) => normalizeStatus(proposal.status) === 'approved')
        .reduce((total, proposal) => total + Number(proposal.estimated_budget || 0), 0),
    [proposals],
  )

  if (isLoading) {
    return (
      <div className="mx-auto max-w-7xl rounded-lg border border-slate-200 bg-white px-5 py-8 text-sm font-medium text-slate-500">
        Memuat detail client...
      </div>
    )
  }

  if (error || !client) {
    return (
      <div className="mx-auto max-w-7xl">
        <Link className="text-sm font-medium text-slate-600 hover:text-slate-950" to="/clients">
          Kembali ke Client
        </Link>
        <div className="mt-4 rounded-lg border border-red-200 bg-red-50 px-5 py-4 text-sm font-medium text-red-700">
          {error || 'Client tidak ditemukan.'}
        </div>
      </div>
    )
  }

  const normalizedStatus = normalizeStatus(client.status)
  const badgeClass = statusStyles[normalizedStatus] || statusStyles.prospect
  const primaryPhone = primaryContact?.mobile_phone || primaryContact?.phone || primaryContact?.whatsapp_number

  return (
    <div className="mx-auto max-w-7xl">
      <div className="mb-4">
        <Link className="text-sm font-medium text-slate-600 hover:text-slate-950" to="/clients">
          Kembali ke Client
        </Link>
      </div>

      <section className="rounded-lg border border-slate-200 bg-white">
        <div className="border-b border-slate-200 px-5 py-5">
          <div className="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">
            <div className="flex gap-4">
              <ClientLogo client={client} />
              <div>
                <div className="flex flex-wrap items-center gap-2">
                  <h2 className="text-2xl font-semibold text-slate-950">{client.client_name}</h2>
                  <span className={`rounded-full px-2.5 py-1 text-xs font-semibold ring-1 ${badgeClass}`}>
                    {statusLabel(client.status)}
                  </span>
                </div>
                <p className="mt-2 text-sm text-slate-500">
                  {[client.industry || 'Industri belum diisi', client.city || 'Kota belum diisi', clientTypeLabel(client.client_type)]
                    .filter(Boolean)
                    .join(' / ')}
                </p>
              </div>
            </div>

            <div className="grid gap-4 sm:grid-cols-3 lg:min-w-[520px]">
              <InfoItem label="Total Proposal" value={proposals.length} />
              <InfoItem label="Total Project" value="0" />
              <InfoItem label="Nilai Kontrak" value={formatCurrency(totalContractValue)} />
            </div>
          </div>
        </div>

        <div className="overflow-x-auto border-b border-slate-200 px-5">
          <div className="flex min-w-max gap-1">
            {tabs.map((tab) => (
              <button
                className={`border-b-2 px-3 py-3 text-sm font-semibold ${
                  activeTab === tab.key
                    ? 'border-slate-950 text-slate-950'
                    : 'border-transparent text-slate-500 hover:text-slate-900'
                }`}
                key={tab.key}
                onClick={() => setActiveTab(tab.key)}
                type="button"
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        <div className="p-5">
          {activeTab === 'Overview' && (
            <div className="grid gap-6 xl:grid-cols-[1fr_360px]">
              <div className="rounded-lg border border-slate-200 p-5">
                <h3 className="text-base font-semibold text-slate-950">Ringkasan Client</h3>
                <div className="mt-5 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
                  <InfoItem label="Industri" value={client.industry} />
                  <InfoItem label="Kota" value={client.city} />
                  <InfoItem label="Status" value={statusLabel(client.status)} />
                  <InfoItem label="Menjadi Client Sejak" value={formatDate(client.customer_since)} />
                  <InfoItem label="Aktivitas Terakhir" value={formatDate(client.last_activity_at)} />
                  <InfoItem label="Follow Up Berikutnya" value={formatDate(client.next_follow_up_at)} />
                  <InfoItem label="Total Proposal" value={proposals.length} />
                  <InfoItem label="Total Project" value="0" />
                  <InfoItem label="Total Nilai Kontrak" value={formatCurrency(totalContractValue)} />
                </div>
              </div>

              <div className="rounded-lg border border-slate-200 p-5">
                <h3 className="text-base font-semibold text-slate-950">Contact Person Utama</h3>
                {primaryContact ? (
                  <div className="mt-5 space-y-4">
                    <InfoItem label="PIC Utama" value={primaryContact.contact_name} />
                    <InfoItem label="Jabatan" value={primaryContact.position} />
                    <InfoItem label="Nomor HP" value={primaryPhone} />
                    <InfoItem label="Email" value={primaryContact.email} />
                  </div>
                ) : (
                  <EmptyState>Belum ada contact person utama.</EmptyState>
                )}
              </div>
            </div>
          )}

          {activeTab === 'Contacts' && (
            <div className="grid gap-6 xl:grid-cols-[minmax(0,1fr)_420px]">
              <div className="rounded-lg border border-slate-200">
                <div className="border-b border-slate-200 px-5 py-4">
                  <h3 className="text-base font-semibold text-slate-950">Contact Person</h3>
                </div>
                {client.contacts.length === 0 ? (
                  <div className="p-5">
                    <EmptyState>Belum ada contact person.</EmptyState>
                  </div>
                ) : (
                  <div className="divide-y divide-slate-200">
                    {client.contacts.map((contact) => (
                      <div className="px-5 py-4" key={contact.id}>
                        <div className="flex flex-col gap-3 lg:flex-row lg:items-start lg:justify-between">
                          <div>
                            <div className="flex flex-wrap items-center gap-2">
                              <p className="font-semibold text-slate-950">{contact.contact_name}</p>
                              {contact.is_primary && (
                                <span className="rounded-full bg-slate-950 px-2.5 py-1 text-xs font-semibold text-white">
                                  Utama
                                </span>
                              )}
                              {contact.is_decision_maker && (
                                <span className="rounded-full bg-sky-50 px-2.5 py-1 text-xs font-semibold text-sky-700">
                                  Pengambil Keputusan
                                </span>
                              )}
                            </div>
                            <p className="mt-1 text-sm text-slate-500">{contact.position || contact.contact_type || '-'}</p>
                          </div>

                          <div className="flex flex-wrap items-center gap-2">
                            {!contact.is_primary && (
                              <button
                                className="rounded-md border border-slate-300 px-3 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50"
                                onClick={() => handleSetPrimary(contact.id)}
                                type="button"
                              >
                                Jadikan Utama
                              </button>
                            )}
                            <button
                              className="rounded-md border border-slate-300 px-3 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50"
                              onClick={() => startEditContact(contact)}
                              type="button"
                            >
                              Ubah
                            </button>
                            <button
                              className="rounded-md border border-red-200 px-3 py-2 text-xs font-semibold text-red-700 hover:bg-red-50"
                              onClick={() => handleDeleteContact(contact.id)}
                              type="button"
                            >
                              Hapus
                            </button>
                          </div>
                        </div>

                        <div className="mt-4 grid gap-4 sm:grid-cols-3">
                          <InfoItem label="Nomor HP" value={contact.mobile_phone || contact.phone || contact.whatsapp_number} />
                          <InfoItem label="Email" value={contact.email} />
                          <InfoItem label="Tipe" value={contact.contact_type} />
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div className="rounded-lg border border-slate-200 p-5">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <p className="text-sm font-medium text-slate-500">
                      {editingContactId ? 'Ubah Contact' : 'Contact Baru'}
                    </p>
                    <h3 className="mt-1 text-base font-semibold text-slate-950">
                      {editingContactId ? 'Perbarui Contact Person' : 'Tambah Contact Person'}
                    </h3>
                  </div>
                  {editingContactId && (
                    <button
                      className="rounded-md border border-slate-300 px-3 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50"
                      onClick={resetContactForm}
                      type="button"
                    >
                      Batal
                    </button>
                  )}
                </div>

                {contactError && (
                  <div className="mt-4 rounded-md bg-red-50 px-3 py-2 text-sm font-medium text-red-700">
                    {contactError}
                  </div>
                )}

                {contactSuccess && (
                  <div className="mt-4 rounded-md bg-emerald-50 px-3 py-2 text-sm font-medium text-emerald-700">
                    {contactSuccess}
                  </div>
                )}

                <form className="mt-5 space-y-4" onSubmit={handleContactSubmit}>
                  <label className="block">
                    <span className="text-sm font-medium text-slate-700">Nama Contact</span>
                    <input
                      className="mt-1 h-10 w-full rounded-md border border-slate-300 px-3 text-sm outline-none focus:border-slate-950"
                      onChange={(event) => updateContactForm('contact_name', event.target.value)}
                      value={contactForm.contact_name}
                    />
                  </label>

                  <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-1">
                    <label className="block">
                      <span className="text-sm font-medium text-slate-700">Jabatan</span>
                      <input
                        className="mt-1 h-10 w-full rounded-md border border-slate-300 px-3 text-sm outline-none focus:border-slate-950"
                        onChange={(event) => updateContactForm('position', event.target.value)}
                        value={contactForm.position}
                      />
                    </label>
                    <label className="block">
                      <span className="text-sm font-medium text-slate-700">Tipe Contact</span>
                      <input
                        className="mt-1 h-10 w-full rounded-md border border-slate-300 px-3 text-sm outline-none focus:border-slate-950"
                        onChange={(event) => updateContactForm('contact_type', event.target.value)}
                        placeholder="PIC utama, Finance, Procurement"
                        value={contactForm.contact_type}
                      />
                    </label>
                  </div>

                  <label className="block">
                    <span className="text-sm font-medium text-slate-700">Email</span>
                    <input
                      className="mt-1 h-10 w-full rounded-md border border-slate-300 px-3 text-sm outline-none focus:border-slate-950"
                      onChange={(event) => updateContactForm('email', event.target.value)}
                      type="email"
                      value={contactForm.email}
                    />
                  </label>

                  <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-1">
                    <label className="block">
                      <span className="text-sm font-medium text-slate-700">Telepon</span>
                      <input
                        className="mt-1 h-10 w-full rounded-md border border-slate-300 px-3 text-sm outline-none focus:border-slate-950"
                        onChange={(event) => updateContactForm('phone', event.target.value)}
                        value={contactForm.phone}
                      />
                    </label>
                    <label className="block">
                      <span className="text-sm font-medium text-slate-700">Nomor HP</span>
                      <input
                        className="mt-1 h-10 w-full rounded-md border border-slate-300 px-3 text-sm outline-none focus:border-slate-950"
                        onChange={(event) => updateContactForm('mobile_phone', event.target.value)}
                        value={contactForm.mobile_phone}
                      />
                    </label>
                  </div>

                  <label className="block">
                    <span className="text-sm font-medium text-slate-700">Nomor WhatsApp</span>
                    <input
                      className="mt-1 h-10 w-full rounded-md border border-slate-300 px-3 text-sm outline-none focus:border-slate-950"
                      onChange={(event) => updateContactForm('whatsapp_number', event.target.value)}
                      value={contactForm.whatsapp_number}
                    />
                  </label>

                  <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-1">
                    <label className="flex items-center gap-2 text-sm font-medium text-slate-700">
                      <input
                        checked={contactForm.is_primary}
                        className="h-4 w-4 rounded border-slate-300"
                        onChange={(event) => updateContactForm('is_primary', event.target.checked)}
                        type="checkbox"
                      />
                      Contact Person Utama
                    </label>
                    <label className="flex items-center gap-2 text-sm font-medium text-slate-700">
                      <input
                        checked={contactForm.is_decision_maker}
                        className="h-4 w-4 rounded border-slate-300"
                        onChange={(event) => updateContactForm('is_decision_maker', event.target.checked)}
                        type="checkbox"
                      />
                      Pengambil Keputusan
                    </label>
                  </div>

                  <label className="block">
                    <span className="text-sm font-medium text-slate-700">Catatan</span>
                    <textarea
                      className="mt-1 min-h-20 w-full resize-y rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-slate-950"
                      onChange={(event) => updateContactForm('notes', event.target.value)}
                      value={contactForm.notes}
                    />
                  </label>

                  <button
                    className="h-11 w-full rounded-md bg-slate-950 text-sm font-semibold text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-400"
                    disabled={isSavingContact}
                    type="submit"
                  >
                    {isSavingContact ? 'Menyimpan contact...' : editingContactId ? 'Perbarui Contact' : 'Simpan Contact'}
                  </button>
                </form>
              </div>
            </div>
          )}

          {activeTab === 'Activities' && (
            <div className="rounded-lg border border-slate-200 p-5">
              <h3 className="text-base font-semibold text-slate-950">Riwayat Aktivitas</h3>
              {activities.length === 0 ? (
                <div className="mt-5">
                  <EmptyState>Belum ada aktivitas</EmptyState>
                </div>
              ) : (
                <div className="mt-5 space-y-4">
                  {activities.map((activity) => (
                    <div className="border-l-2 border-slate-200 pl-4" key={activity.id}>
                      <p className="text-sm font-semibold text-slate-950">{translateActivityTitle(activity.activity_title)}</p>
                      <p className="mt-1 text-xs font-medium text-slate-400">{formatDate(activity.activity_at)}</p>
                      {activity.activity_description && (
                        <p className="mt-2 text-sm leading-6 text-slate-600">
                          {translateActivityDescription(activity.activity_description)}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {activeTab === 'Proposals' && (
            <div className="rounded-lg border border-slate-200">
              <div className="border-b border-slate-200 px-5 py-4">
                <h3 className="text-base font-semibold text-slate-950">Proposal Client</h3>
              </div>
              {proposals.length === 0 ? (
                <div className="p-5">
                  <EmptyState>Belum ada proposal untuk client ini.</EmptyState>
                </div>
              ) : (
                <div className="divide-y divide-slate-200">
                  {proposals.map((proposal) => (
                    <div className="grid gap-4 px-5 py-4 lg:grid-cols-[minmax(0,1fr)_180px_180px]" key={proposal.id}>
                      <div>
                        <p className="font-semibold text-slate-950">{proposal.proposal_title}</p>
                        <p className="mt-1 text-sm text-slate-500">{proposal.research_type || 'Jenis riset belum diisi'}</p>
                      </div>
                      <div>
                        <p className="text-xs font-medium uppercase text-slate-400">Status</p>
                        <p className="mt-1 text-sm font-medium text-slate-800">{statusLabel(proposal.status)}</p>
                      </div>
                      <div>
                        <p className="text-xs font-medium uppercase text-slate-400">Estimasi Budget</p>
                        <p className="mt-1 text-sm font-medium text-slate-800">{formatCurrency(proposal.estimated_budget)}</p>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {activeTab === 'Projects' && <EmptyState>Segera tersedia</EmptyState>}

          {activeTab === 'Documents' && <EmptyState>Segera tersedia</EmptyState>}
        </div>
      </section>
    </div>
  )
}

export default ClientDetailPage
