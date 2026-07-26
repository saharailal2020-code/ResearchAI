import { useCallback, useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import { DetailItem, ErrorState, InfoCard, StatusBadge } from '../components/ui.jsx'
import {
  getQuestionnaire,
  updateQuestionnaire,
  updateQuestionnaireStatus,
} from '../services/questionnaires'
import { displayValue, formatDate } from '../utils/formatters'
import { questionnaireStatusStyles } from '../utils/statusStyles'

function QuestionnaireDetailSkeleton() {
  return (
    <div className="mx-auto max-w-7xl animate-pulse space-y-4">
      <p className="text-sm font-medium text-slate-500">Memuat questionnaire...</p>
      <section className="h-44 rounded-lg border border-slate-200 bg-white" />
      <section className="h-96 rounded-lg border border-slate-200 bg-white" />
    </div>
  )
}

function QuestionnaireDetailPage() {
  const { questionnaireId } = useParams()
  const [questionnaire, setQuestionnaire] = useState(null)
  const [form, setForm] = useState({
    questionnaire_name: '',
    target_respondent: '',
    instrument_type: 'Quantitative Survey',
    kobo_link: '',
    xlsform_link: '',
  })
  const [isEditing, setIsEditing] = useState(false)
  const [error, setError] = useState('')
  const [actionError, setActionError] = useState('')
  const [validationError, setValidationError] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isActionLoading, setIsActionLoading] = useState(false)

  const loadQuestionnaire = useCallback(async () => {
    setIsLoading(true)
    setError('')
    try {
      const data = await getQuestionnaire(questionnaireId)
      setQuestionnaire(data)
      setForm({
        questionnaire_name: data.questionnaire_name || '',
        target_respondent: data.target_respondent || '',
        instrument_type: data.instrument_type || 'Quantitative Survey',
        kobo_link: data.kobo_link || '',
        xlsform_link: data.xlsform_link || '',
      })
    } catch (requestError) {
      if (requestError?.response?.status === 404) {
        setError('Questionnaire tidak ditemukan.')
      } else {
        setError('Tidak dapat mengambil detail questionnaire. Periksa koneksi server lalu coba lagi.')
      }
    } finally {
      setIsLoading(false)
    }
  }, [questionnaireId])

  useEffect(() => {
    loadQuestionnaire()
  }, [loadQuestionnaire])

  function updateField(field, value) {
    setForm((current) => ({ ...current, [field]: value }))
  }

  async function handleSave(event) {
    event.preventDefault()
    const name = form.questionnaire_name.trim()
    setValidationError('')
    setActionError('')
    if (name.length < 3) {
      setValidationError('Nama questionnaire wajib diisi minimal 3 karakter.')
      return
    }
    if (form.target_respondent.trim().length < 2) {
      setValidationError('Target respondent wajib diisi.')
      return
    }
    if (form.instrument_type.trim().length < 2) {
      setValidationError('Instrument type wajib diisi.')
      return
    }

    setIsSubmitting(true)
    try {
      const updated = await updateQuestionnaire(questionnaireId, {
        questionnaire_name: name,
        target_respondent: form.target_respondent.trim(),
        instrument_type: form.instrument_type.trim(),
        kobo_link: form.kobo_link.trim() || null,
        xlsform_link: form.xlsform_link.trim() || null,
      })
      setQuestionnaire(updated)
      setIsEditing(false)
    } catch (requestError) {
      if (requestError?.response?.status === 400) {
        setActionError('Questionnaire Ready tidak dapat diedit pada MVP.')
      } else {
        setActionError('Questionnaire belum bisa diperbarui. Silakan coba lagi.')
      }
    } finally {
      setIsSubmitting(false)
    }
  }

  async function handleReady() {
    setActionError('')
    setIsActionLoading(true)
    try {
      const updated = await updateQuestionnaireStatus(questionnaireId, 'Ready')
      setQuestionnaire(updated)
      setIsEditing(false)
    } catch {
      setActionError('Questionnaire belum bisa ditandai Ready. Silakan coba lagi.')
    } finally {
      setIsActionLoading(false)
    }
  }

  if (isLoading) {
    return <QuestionnaireDetailSkeleton />
  }

  if (error) {
    return (
      <div className="mx-auto max-w-7xl">
        <ErrorState
          actions={
            <button
              className="rounded-md border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50"
              onClick={loadQuestionnaire}
              type="button"
            >
              Coba Lagi
            </button>
          }
          message={error}
          title="Detail questionnaire belum bisa ditampilkan"
        />
      </div>
    )
  }

  const isDraft = questionnaire.status === 'Draft'

  return (
    <div className="mx-auto max-w-7xl">
      <div className="mb-4 flex items-center gap-2 text-sm font-medium text-slate-500">
        <Link className="hover:text-slate-950" to={`/projects/${questionnaire.project_id}`}>
          Project Detail
        </Link>
        <span>/</span>
        <span className="text-slate-950">Questionnaire Detail</span>
      </div>

      <section className="rounded-lg border border-slate-200 bg-white">
        <div className="flex flex-col gap-5 border-b border-slate-200 px-6 py-5 lg:flex-row lg:items-start lg:justify-between">
          <div>
            <p className="text-sm font-semibold text-slate-500">Questionnaire</p>
            <h1 className="mt-1 text-3xl font-bold text-slate-950">{questionnaire.questionnaire_name}</h1>
            <p className="mt-2 text-sm text-slate-500">
              Project: {questionnaire.project.project_number} | Version: {questionnaire.version_number}
            </p>
          </div>
          <StatusBadge
            label={questionnaire.status}
            status={questionnaire.status}
            styles={questionnaireStatusStyles}
          />
        </div>

        <div className="grid gap-4 p-6 lg:grid-cols-[minmax(0,1.2fr)_minmax(320px,0.8fr)]">
          <div className="space-y-4">
            <InfoCard title="Informasi Questionnaire">
              {isEditing ? (
                <form onSubmit={handleSave}>
                  <label className="block">
                    <span className="text-sm font-semibold text-slate-700">Questionnaire Name *</span>
                    <input
                      className={`mt-2 h-10 w-full rounded-md border px-3 text-sm outline-none focus:border-slate-950 ${
                        validationError ? 'border-red-300' : 'border-slate-300'
                      }`}
                      onChange={(event) => updateField('questionnaire_name', event.target.value)}
                      value={form.questionnaire_name}
                    />
                  </label>
                  {validationError && <p className="mt-2 text-sm font-medium text-red-700">{validationError}</p>}
                  <div className="mt-5 grid gap-4 md:grid-cols-2">
                    <label className="block">
                      <span className="text-sm font-semibold text-slate-700">Target Respondent *</span>
                      <input
                        className="mt-2 h-10 w-full rounded-md border border-slate-300 px-3 text-sm outline-none focus:border-slate-950"
                        onChange={(event) => updateField('target_respondent', event.target.value)}
                        value={form.target_respondent}
                      />
                    </label>
                    <label className="block">
                      <span className="text-sm font-semibold text-slate-700">Instrument Type *</span>
                      <select
                        className="mt-2 h-10 w-full rounded-md border border-slate-300 px-3 text-sm outline-none focus:border-slate-950"
                        onChange={(event) => updateField('instrument_type', event.target.value)}
                        value={form.instrument_type}
                      >
                        <option value="Quantitative Survey">Quantitative Survey</option>
                        <option value="Screener">Screener</option>
                        <option value="Observation Checklist">Observation Checklist</option>
                        <option value="Other">Other</option>
                      </select>
                    </label>
                    <label className="block">
                      <span className="text-sm font-semibold text-slate-700">KoBo Link</span>
                      <input
                        className="mt-2 h-10 w-full rounded-md border border-slate-300 px-3 text-sm outline-none focus:border-slate-950"
                        onChange={(event) => updateField('kobo_link', event.target.value)}
                        value={form.kobo_link}
                      />
                    </label>
                    <label className="block">
                      <span className="text-sm font-semibold text-slate-700">XLSForm Link</span>
                      <input
                        className="mt-2 h-10 w-full rounded-md border border-slate-300 px-3 text-sm outline-none focus:border-slate-950"
                        onChange={(event) => updateField('xlsform_link', event.target.value)}
                        value={form.xlsform_link}
                      />
                    </label>
                  </div>
                  <div className="mt-5 flex flex-wrap gap-3">
                    <button
                      className="rounded-md bg-slate-950 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-300 disabled:text-slate-500"
                      disabled={isSubmitting}
                      type="submit"
                    >
                      {isSubmitting ? 'Menyimpan...' : 'Simpan Perubahan'}
                    </button>
                    <button
                      className="rounded-md border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50"
                      onClick={() => setIsEditing(false)}
                      type="button"
                    >
                      Batal
                    </button>
                  </div>
                </form>
              ) : (
                <div className="grid gap-5 md:grid-cols-2">
                  <DetailItem label="Questionnaire Name" value={questionnaire.questionnaire_name} strong />
                  <DetailItem label="Target Respondent" value={questionnaire.target_respondent} strong />
                  <DetailItem label="Instrument Type" value={questionnaire.instrument_type} />
                  <DetailItem label="Version Number" value={questionnaire.version_number} strong />
                  <DetailItem label="Status" value={questionnaire.status} />
                  <DetailItem label="KoBo Link" value={displayValue(questionnaire.kobo_link)} />
                  <DetailItem label="XLSForm Link" value={displayValue(questionnaire.xlsform_link)} />
                  <DetailItem label="Last Updated" value={formatDate(questionnaire.updated_at)} />
                  <DetailItem label="Ready Date" value={formatDate(questionnaire.ready_at)} />
                </div>
              )}
            </InfoCard>
          </div>

          <aside className="space-y-4">
            <InfoCard title="Project Reference">
              <div className="space-y-4">
                <DetailItem label="Project Number" value={questionnaire.project.project_number} strong />
                <DetailItem label="Project Name" value={questionnaire.project.project_name} />
                <DetailItem label="Project Status" value={questionnaire.project.status} />
                <DetailItem label="Research Type" value={displayValue(questionnaire.project.research_type)} />
              </div>
              <Link
                className="mt-5 inline-flex w-full justify-center rounded-md border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50"
                to={`/projects/${questionnaire.project_id}`}
              >
                Buka Project
              </Link>
            </InfoCard>

            <InfoCard title="Next Business Action">
              {isDraft ? (
                <div className="space-y-3">
                  <button
                    className="inline-flex h-10 w-full items-center justify-center rounded-md border border-slate-300 px-4 text-sm font-semibold text-slate-700 hover:bg-slate-50"
                    onClick={() => setIsEditing(true)}
                    type="button"
                  >
                    Edit Questionnaire
                  </button>
                  <button
                    className="inline-flex h-10 w-full items-center justify-center rounded-md bg-slate-950 px-4 text-sm font-semibold text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-300 disabled:text-slate-500"
                    disabled={isActionLoading}
                    onClick={handleReady}
                    type="button"
                  >
                    {isActionLoading ? 'Menandai Ready...' : 'Tandai Ready'}
                  </button>
                </div>
              ) : (
                <div className="rounded-md bg-slate-50 px-4 py-3 text-sm font-medium text-slate-600">
                  Questionnaire sudah Ready dan tidak dapat diedit langsung pada MVP.
                </div>
              )}
              {actionError && (
                <div className="mt-4 rounded-md bg-red-50 px-4 py-3 text-sm font-semibold text-red-700">
                  {actionError}
                </div>
              )}
            </InfoCard>
          </aside>
        </div>
      </section>
    </div>
  )
}

export default QuestionnaireDetailPage
