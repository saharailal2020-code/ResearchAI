import { proposalStatusStyles } from '../utils/statusStyles'

export function StatusBadge({ label, status, styles = proposalStatusStyles }) {
  return (
    <span
      className={`inline-flex w-fit rounded-full px-3 py-1 text-sm font-semibold ring-1 ${styles[status] || styles.Draft || styles.Setup}`}
    >
      {label}
    </span>
  )
}

export function InfoCard({ children, title, description }) {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-5">
      {title && (
        <div className="mb-5">
          <p className="text-base font-semibold text-slate-950">{title}</p>
          {description && <p className="mt-1 text-sm text-slate-500">{description}</p>}
        </div>
      )}
      {children}
    </section>
  )
}

export function DetailItem({ label, value, strong = false }) {
  return (
    <div>
      <p className="text-xs font-semibold uppercase text-slate-400">{label}</p>
      <p className={`mt-1 text-sm ${strong ? 'font-semibold text-slate-950' : 'font-medium text-slate-700'}`}>
        {value}
      </p>
    </div>
  )
}

export function SummaryCard({ label, value }) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-5">
      <p className="text-sm font-semibold text-slate-500">{label}</p>
      <p className="mt-3 text-2xl font-bold text-slate-950">{value}</p>
    </div>
  )
}

export function PlaceholderCard({ description, label = 'Belum dimulai', title }) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-5">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-base font-semibold text-slate-950">{title}</p>
          <p className="mt-2 text-sm leading-6 text-slate-500">{description}</p>
        </div>
        <span className="shrink-0 rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-500">
          {label}
        </span>
      </div>
    </div>
  )
}

export function ErrorState({ actions, message, title = 'Data belum bisa ditampilkan' }) {
  return (
    <section className="rounded-lg border border-red-200 bg-white p-6">
      <p className="text-sm font-semibold text-red-700">{title}</p>
      <h2 className="mt-2 text-xl font-semibold text-slate-950">{message}</h2>
      {actions && <div className="mt-5 flex flex-wrap gap-3">{actions}</div>}
    </section>
  )
}
