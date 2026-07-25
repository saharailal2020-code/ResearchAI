import { api } from './api'

export async function getClients(params = {}) {
  const response = await api.get('/clients', { params })
  return response.data
}

export async function createClient(payload) {
  const response = await api.post('/clients', payload)
  return response.data
}
