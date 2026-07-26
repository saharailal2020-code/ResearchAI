import { api } from './api'

export async function getProjectQuestionnaires(projectId) {
  const response = await api.get(`/projects/${projectId}/questionnaires`)
  return response.data
}

export async function getProjectQuestionnaire(projectId) {
  const response = await api.get(`/projects/${projectId}/questionnaire`)
  return response.data
}

export async function createProjectQuestionnaire(projectId, payload) {
  const response = await api.post(`/projects/${projectId}/questionnaires`, payload)
  return response.data
}

export async function getQuestionnaire(questionnaireId) {
  const response = await api.get(`/questionnaires/${questionnaireId}`)
  return response.data
}

export async function updateQuestionnaire(questionnaireId, payload) {
  const response = await api.patch(`/questionnaires/${questionnaireId}`, payload)
  return response.data
}

export async function updateQuestionnaireStatus(questionnaireId, status) {
  const response = await api.patch(`/questionnaires/${questionnaireId}/status`, { status })
  return response.data
}
