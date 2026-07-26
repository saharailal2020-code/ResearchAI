import { Navigate, Route, Routes } from 'react-router-dom'

import AppLayout from './layouts/AppLayout.jsx'
import ClientDetailPage from './pages/ClientDetailPage.jsx'
import ClientsPage from './pages/ClientsPage.jsx'
import DashboardPage from './pages/DashboardPage.jsx'
import LoginPage from './pages/LoginPage.jsx'
import ProposalCreatePage from './pages/ProposalCreatePage.jsx'
import ProposalDetailPage from './pages/ProposalDetailPage.jsx'
import ProposalsPage from './pages/ProposalsPage.jsx'
import { getToken } from './services/api.js'

function RequireAuth() {
  if (!getToken()) {
    return <Navigate to="/login" replace />
  }

  return <AppLayout />
}

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/" element={<RequireAuth />}>
        <Route index element={<DashboardPage />} />
        <Route path="dashboard" element={<DashboardPage />} />
        <Route path="clients" element={<ClientsPage />} />
        <Route path="clients/:clientId" element={<ClientDetailPage />} />
        <Route path="proposals" element={<ProposalsPage />} />
        <Route path="proposals/new" element={<ProposalCreatePage />} />
        <Route path="proposals/:proposalId" element={<ProposalDetailPage />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default App
