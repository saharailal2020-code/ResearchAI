import { Link, useParams } from 'react-router-dom'

function ProposalDetailPage() {
  const { proposalId } = useParams()

  return (
    <div className="mx-auto max-w-7xl">
      <div className="mb-4">
        <Link className="text-sm font-medium text-slate-600 hover:text-slate-950" to="/proposals">
          Kembali ke Proposal
        </Link>
      </div>

      <section className="rounded-lg border border-slate-200 bg-white p-6">
        <p className="text-sm font-medium text-slate-500">Detail Proposal</p>
        <h2 className="mt-1 text-xl font-semibold text-slate-950">Segera tersedia</h2>
        <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-600">
          Halaman detail proposal akan dibangun pada sprint berikutnya. Untuk saat ini, klik dari Proposal List sudah
          diarahkan ke halaman placeholder ini agar alur navigasi dasar siap.
        </p>
        <p className="mt-5 text-xs font-medium uppercase text-slate-400">Proposal ID</p>
        <p className="mt-1 break-all text-sm font-medium text-slate-700">{proposalId}</p>
      </section>
    </div>
  )
}

export default ProposalDetailPage
