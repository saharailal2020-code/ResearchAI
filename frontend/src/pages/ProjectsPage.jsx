import { Link } from 'react-router-dom'

function ProjectsPage() {
  return (
    <div className="mx-auto max-w-7xl">
      <section className="rounded-lg border border-slate-200 bg-white p-6">
        <p className="text-sm font-semibold text-slate-500">Project Management</p>
        <h1 className="mt-1 text-2xl font-bold text-slate-950">Project</h1>
        <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-600">
          Project List lengkap belum masuk scope Sprint 6. Project baru dibuat dari Proposal yang sudah disetujui
          melalui action Setup Project.
        </p>
        <Link
          className="mt-5 inline-flex rounded-md bg-slate-950 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800"
          to="/proposals"
        >
          Buka Proposal
        </Link>
      </section>
    </div>
  )
}

export default ProjectsPage
