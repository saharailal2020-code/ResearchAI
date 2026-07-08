import { Navigate, Route, Routes } from 'react-router-dom'

import AppLayout from './layouts/AppLayout.jsx'
import DashboardPage from './pages/DashboardPage.jsx'
import LoginPage from './pages/LoginPage.jsx'

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/" element={<AppLayout />}>
        <Route index element={<DashboardPage />} />
        <Route path="dashboard" element={<DashboardPage />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default App
