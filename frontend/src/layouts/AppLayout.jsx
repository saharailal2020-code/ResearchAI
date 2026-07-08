import { Outlet } from 'react-router-dom'

const navItems = [
  'Dashboard',
  'Clients',
  'Proposals',
  'Projects',
  'Data',
  'AI Analysis',
  'Reports',
]

function AppLayout() {
  return (
    <div className="min-h-screen bg-[#f6f7f9]">
      <aside className="fixed inset-y-0 left-0 hidden w-64 border-r border-slate-200 bg-white lg:block">
        <div className="border-b border-slate-200 px-6 py-5">
          <p className="text-lg font-semibold text-slate-950">ResearchAI</p>
          <p className="mt-1 text-sm text-slate-500">Research OS</p>
        </div>
        <nav className="px-3 py-4">
          {navItems.map((item) => (
            <button
              className="mb-1 flex h-10 w-full items-center rounded-md px-3 text-left text-sm font-medium text-slate-600 hover:bg-slate-100 hover:text-slate-950"
              key={item}
              type="button"
            >
              {item}
            </button>
          ))}
        </nav>
      </aside>

      <div className="lg:pl-64">
        <header className="sticky top-0 z-10 border-b border-slate-200 bg-white/95 px-5 py-4 backdrop-blur">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-500">MVP Workspace</p>
              <h1 className="text-xl font-semibold text-slate-950">Dashboard</h1>
            </div>
            <a
              className="rounded-md border border-slate-300 px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
              href="/login"
            >
              Login
            </a>
          </div>
        </header>

        <main className="px-5 py-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}

export default AppLayout
