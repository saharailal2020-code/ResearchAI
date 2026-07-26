import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'

import { DetailItem, ErrorState, InfoCard, StatusBadge } from '../components/ui.jsx'
import { getProject } from '../services/projects'
import { createProjectQuestionnaire } from '../services/questionnaires'
import { displayValue } from '../utils/formatters'
import { questionnaireStatusStyles } from '../utils/statusStyles'

function QuestionnaireFormSkeleton() {
  return (
    <div className="mx-auto max-w-7xl animate-pulse space-y-4">
      <p className="text-sm font-medium text-slate-500">Memuat data questionnaire...</p>
      <section className="h-40 rounded-lg border border-slate-200 bg-white" />
      <section className="h-96 rounded-lg border border-slate-200 bg-white" />
    </div>
  )
}

function QuestionnaireCreatePage() {
  const navigate = useNavigate()
  const { projectId } = useParams()
  const [project, setProject] = useState(null)
  const [form, setForm] = useState({
    questionnaire_name: '',
    target_respondent: '',
    instrument_type: 'Quantitative Survey',
    kobo_link: '',
    xlsform_link: '',
  })
  const [error, setError] = useState('')
  const [validationError, setValidationError] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)

  useEffect(() => {
    let isMounted = true

    async function loadProject() {
      setIsLoading(true)
      setError('')
      try {
        const projectData = await getProject(projectId)
        if (isMounted) {
          setProject(projectData)
          setForm((current) => ({
            ...current,
            questionnaire_name: `${projectData.project_name} Questionnaire`,
          }))
        }
      } catch (requestError) {
        if (requestError?.response?.status === 404) {
          setError('Project tidak ditemukan.')
        } else {
          setError('Tidak dapat memuat data project. Periksa koneksi server lalu coba lagi.')
        }
      } finally {
        if (isMounted) {
          setIsLoading(false)
        }
      }
    }

    loadProject()

    return () => {
      isMounted = false
    }
  }, [navigate, projectId])

  function updateField(field, value) {
    setForm((current) => ({ ...current, [field]: value }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    const name = form.questionnaire_name.trim()
    setValidationError('')
    if (name.length < 3) {
      setValidationError('Nama questionnaire wajib diisi minimal 3 karakter.')
      return
    }
    if (name.length > 150) {
      setValidationError('Nama questionnaire maksimal 150 karakter.')
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
      const questionnaire = await createProjectQuestionnaire(projectId, {
        questionnaire_name: name,
        target_respondent: form.target_respondent.trim(),
        instrument_type: form.instrument_type.trim(),
        kobo_link: form.kobo_link.trim() || null,
        xlsform_link: form.xlsform_link.trim() || null,
      })
      navigate(`/questionnaires/${questionnaire.id}`)
    } catch {
      setError('Questionnaire belum bisa disimpan. Silakan coba lagi.')
    } finally {
      setIsSubmitting(false)
    }
  }

  if (isLoading) {
    return <QuestionnaireFormSkeleton />
  }

  if (error && !project) {
    return (
      <div className="mx-auto max-w-7xl">
        <ErrorState
          actions={
            <Link
              className="rounded-md bg-slate-950 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800"
              to="/projects"
            >
              Kembali ke Project
            </Link>
          }
          message={error}
          title="Questionnaire belum bisa dibuat"
        />
      </div>
    )
  }

  return (
    <div className="mx-auto max-w-7xl">
      <div className="mb-4 flex items-center gap-2 text-sm font-medium text-slate-500">
        <Link className="hover:text-slate-950" to={`/projects/${project.id}`}>
          Project Detail
        </Link>
        <span>/</span>
        <span className="text-slate-950">Buat Questionnaire</span>
      </div>

      <section className="rounded-lg border border-slate-200 bg-white">
        <div className="flex flex-col gap-4 border-b border-slate-200 px-6 py-5 lg:flex-row lg:items-start lg:justify-between">
          <div>
            <p className="text-sm font-semibold text-slate-500">Research Preparation</p>
            <h1 className="mt-1 text-3xl font-bold text-slate-950">Buat Questionnaire</h1>
            <p className="mt-2 text-sm text-slate-500">Buat metadata instrumen survey kuantitatif untuk project ini.</p>
          </div>
          <StatusBadge label="Draft" status="Draft" styles={questionnaireStatusStyles} />
        </div>

        <form className="grid gap-4 p-6 lg:grid-cols-[minmax(0,1.2fr)_minmax(320px,0.8fr)]" onSubmit={handleSubmit}>
          <div className="space-y-4">
            <InfoCard title="Informasi Questionnaire">
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
                    placeholder="Rumah Tangga, UMKM, Bank Peserta"
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
                    placeholder="https://..."
                    value={form.kobo_link}
                  />
                </label>
                <label className="block">
                  <span className="text-sm font-semibold text-slate-700">XLSForm Link</span>
                  <input
                    className="mt-2 h-10 w-full rounded-md border border-slate-300 px-3 text-sm outline-none focus:border-slate-950"
                    onChange={(event) => updateField('xlsform_link', event.target.value)}
                    placeholder="https://..."
                    value={form.xlsform_link}
                  />
                </label>
              </div>
            </InfoCard>
          </div>

          <aside className="space-y-4">
            <InfoCard title="Informasi Project">
              <div className="space-y-4">
                <DetailItem label="Project Number" value={project.project_number} strong />
                <DetailItem label="Project Name" value={project.project_name} />
                <DetailItem label="Research Type" value={displayValue(project.research_type)} />
                <DetailItem label="Target Respondent" value={form.target_respondent || '-'} />
                <DetailItem label="Instrument Type" value={form.instrument_type} />
                <DetailItem label="Status Questionnaire" value="Draft" />
                <DetailItem label="Version Number" value="1" />
              </div>
            </InfoCard>

            {error && <div className="rounded-md bg-red-50 px-4 py-3 text-sm font-semibold text-red-700">{error}</div>}

            <div className="rounded-lg border border-slate-200 bg-white p-5">
              <div className="flex flex-col gap-3">
                <Link
                  className="inline-flex h-10 items-center justify-center rounded-md border border-slate-300 px-4 text-sm font-semibold text-slate-700 hover:bg-slate-50"
                  to={`/projects/${project.id}`}
                >
                  Batal
                </Link>
                <button
                  className="inline-flex h-10 items-center justify-center rounded-md bg-slate-950 px-4 text-sm font-semibold text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-300 disabled:text-slate-500"
                  disabled={isSubmitting}
                  type="submit"
                >
                  {isSubmitting ? 'Menyimpan Questionnaire...' : 'Simpan Draft'}
                </button>
              </div>
            </div>
          </aside>
        </form>
      </section>
    </div>
  )
}

export default QuestionnaireCreatePage
