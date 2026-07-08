const stats = [
  { label: 'Active Projects', value: '0' },
  { label: 'Running Proposals', value: '0' },
  { label: 'Datasets Ready', value: '0' },
  { label: 'Reports in Draft', value: '0' },
]

const modules = [
  'Client Management',
  'Proposal Management',
  'Project Management',
  'Data Processing',
  'AI Analysis',
  'Report Generator',
]

function DashboardPage() {
  const { user } = useOutletContext()

  return (
    <div className="mx-auto max-w-7xl">
      <section className="mb-6 rounded-lg border border-slate-200 bg-white p-5">
        <p className="text-sm font-medium text-slate-500">Signed in as</p>
        <h2 className="mt-1 text-lg font-semibold text-slate-950">{user.full_name}</h2>
        <p className="mt-1 text-sm text-slate-600">{user.email}</p>
      </section>

      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {stats.map((stat) => (
          <div className="rounded-lg border border-slate-200 bg-white p-5" key={stat.label}>
            <p className="text-sm font-medium text-slate-500">{stat.label}</p>
            <p className="mt-3 text-3xl font-semibold text-slate-950">{stat.value}</p>
          </div>
        ))}
      </section>

      <section className="mt-6 grid gap-6 xl:grid-cols-[1fr_360px]">
        <div className="rounded-lg border border-slate-200 bg-white">
          <div className="border-b border-slate-200 px-5 py-4">
            <h2 className="text-base font-semibold text-slate-950">MVP Modules</h2>
          </div>
          <div className="divide-y divide-slate-200">
            {modules.map((module) => (
              <div className="flex items-center justify-between px-5 py-4" key={module}>
                <span className="text-sm font-medium text-slate-800">{module}</span>
                <span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-medium text-slate-600">
                  Planned
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-lg border border-slate-200 bg-white p-5">
          <h2 className="text-base font-semibold text-slate-950">Backend Status</h2>
          <p className="mt-2 text-sm leading-6 text-slate-600">
            Login UI is connected to the FastAPI authentication endpoints and reads
            the current user profile from the backend.
          </p>
          <div className="mt-4 rounded-md bg-emerald-50 px-3 py-2 text-sm font-medium text-emerald-700">
            Auth, FastAPI, and PostgreSQL are available locally.
          </div>
        </div>
      </section>
    </div>
  )
}

export default DashboardPage
import { useOutletContext } from 'react-router-dom'
