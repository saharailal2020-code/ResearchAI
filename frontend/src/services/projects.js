import { api } from './api'

export async function setupProjectFromProposal(proposalId, payload) {
  const response = await api.post(`/proposals/${proposalId}/setup-project`, payload)
  return response.data
}

export async function getProject(projectId) {
  const response = await api.get(`/projects/${projectId}`)
  return response.data
}

export async function updateProjectStatus(projectId, status) {
  const response = await api.patch(`/projects/${projectId}/status`, { status })
  return response.data
}
