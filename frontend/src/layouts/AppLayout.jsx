import { useEffect, useState } from 'react'
import { Navigate, NavLink, Outlet, useLocation, useNavigate } from 'react-router-dom'

import { getCurrentUser, logoutUser } from '../services/auth'

const navItems = [
  { label: 'Dashboard', path: '/dashboard', isReady: true },
  { label: 'Clients', path: '/clients', isReady: true },
  { label: 'Proposals', path: '/proposals', isReady: false },
  { label: 'Projects', path: '/projects', isReady: false },
  { label: 'Data', path: '/data', isReady: false },
  { label: 'AI Analysis', path: '/ai-analysis', isReady: false },
  { label: 'Reports', path: '/reports', isReady: false },
]

const pageTitles = {
  '/': 'Dashboard',
  '/dashboard': 'Dashboard',
  '/clients': 'Clients',
}

function AppLayout() {
  const navigate = useNavigate()
  const location = useLocation()
  const [user, setUser] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isUnauthorized, setIsUnauthorized] = useState(false)

  useEffect(() => {
    let isMounted = true

    async function loadUser() {
      try {
        const currentUser = await getCurrentUser()
        if (isMounted) {
          setUser(currentUser)
        }
      } catch {
        logoutUser()
        if (isMounted) {
          setIsUnauthorized(true)
        }
      } finally {
        if (isMounted) {
          setIsLoading(false)
        }
      }
    }

    loadUser()

    return () => {
      isMounted = false
    }
  }, [])

  function handleLogout() {
    logoutUser()
    navigate('/login')
  }

  const pageTitle =
    pageTitles[location.pathname] || (location.pathname.startsWith('/clients/') ? 'Client Detail' : 'Dashboard')

  if (isUnauthorized) {
    return <Navigate to="/login" replace />
  }

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#f6f7f9] text-sm font-medium text-slate-600">
        Loading ResearchAI...
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-[#f6f7f9]">
      <aside className="fixed inset-y-0 left-0 hidden w-64 border-r border-slate-200 bg-white lg:block">
        <div className="border-b border-slate-200 px-6 py-5">
          <p className="text-lg font-semibold text-slate-950">ResearchAI</p>
          <p className="mt-1 text-sm text-slate-500">Research OS</p>
        </div>
        <nav className="px-3 py-4">
          {navItems.map((item) =>
            item.isReady ? (
              <NavLink
                className={({ isActive }) =>
                  `mb-1 flex h-10 w-full items-center rounded-md px-3 text-left text-sm font-medium ${
                    isActive
                      ? 'bg-slate-950 text-white'
                      : 'text-slate-600 hover:bg-slate-100 hover:text-slate-950'
                  }`
                }
                key={item.path}
                to={item.path}
              >
                {item.label}
              </NavLink>
            ) : (
              <div
                className="mb-1 flex h-10 w-full items-center justify-between rounded-md px-3 text-sm font-medium text-slate-400"
                key={item.path}
              >
                <span>{item.label}</span>
                <span className="rounded-full bg-slate-100 px-2 py-0.5 text-[11px] font-semibold text-slate-500">
                  Planned
                </span>
              </div>
            ),
          )}
        </nav>
      </aside>

      <div className="lg:pl-64">
        <header className="sticky top-0 z-10 border-b border-slate-200 bg-white/95 px-5 py-4 backdrop-blur">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-500">MVP Workspace</p>
              <h1 className="text-xl font-semibold text-slate-950">{pageTitle}</h1>
            </div>
            <div className="flex items-center gap-3">
              <div className="hidden text-right sm:block">
                <p className="text-sm font-semibold text-slate-900">{user?.full_name}</p>
                <p className="text-xs text-slate-500">{user?.roles?.[0]}</p>
              </div>
              <button
                className="rounded-md border border-slate-300 px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
                onClick={handleLogout}
                type="button"
              >
                Logout
              </button>
            </div>
          </div>
        </header>

        <main className="px-5 py-6">
          <Outlet context={{ user }} />
        </main>
      </div>
    </div>
  )
}

export default AppLayout
