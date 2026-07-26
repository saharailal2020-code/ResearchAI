import { api } from './api'

export async function getProposals(params = {}) {
  const response = await api.get('/proposals', { params })
  return response.data
}

export async function getProposal(proposalId) {
  const response = await api.get(`/proposals/${proposalId}`)
  return response.data
}

export async function createProposal(payload) {
  const response = await api.post('/proposals', payload)
  return response.data
}

export async function updateProposalStatus(proposalId, status) {
  const response = await api.patch(`/proposals/${proposalId}/status`, { status })
  return response.data
}
