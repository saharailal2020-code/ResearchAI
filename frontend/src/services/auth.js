import { api, clearToken, saveToken } from './api'

export async function loginUser(credentials) {
  const response = await api.post('/auth/login', credentials)
  saveToken(response.data.access_token)
  return response.data
}

export async function getCurrentUser() {
  const response = await api.get('/auth/me')
  return response.data
}

export function logoutUser() {
  clearToken()
}
