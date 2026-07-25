import { api } from './api'

export async function getProposals(params = {}) {
  const response = await api.get('/proposals', { params })
  return response.data
}
