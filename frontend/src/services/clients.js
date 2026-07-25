import { api } from './api'

export async function getClients(params = {}) {
  const response = await api.get('/clients', { params })
  return response.data
}

export async function getClient(clientId) {
  const response = await api.get(`/clients/${clientId}`)
  return response.data
}

export async function getClientActivities(clientId) {
  const response = await api.get(`/clients/${clientId}/activities`)
  return response.data
}

export async function createClientContact(clientId, payload) {
  const response = await api.post(`/clients/${clientId}/contacts`, payload)
  return response.data
}

export async function updateClientContact(clientId, contactId, payload) {
  const response = await api.patch(`/clients/${clientId}/contacts/${contactId}`, payload)
  return response.data
}

export async function setPrimaryClientContact(clientId, contactId) {
  const response = await api.patch(`/clients/${clientId}/contacts/${contactId}/primary`)
  return response.data
}

export async function deleteClientContact(clientId, contactId) {
  await api.delete(`/clients/${clientId}/contacts/${contactId}`)
}

export async function createClient(payload) {
  const response = await api.post('/clients', payload)
  return response.data
}
