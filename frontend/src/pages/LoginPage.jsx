function LoginPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-[#f6f7f9] px-5">
      <section className="w-full max-w-md rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <div>
          <p className="text-sm font-semibold uppercase tracking-wide text-slate-500">
            ResearchAI
          </p>
          <h1 className="mt-2 text-2xl font-semibold text-slate-950">Sign in</h1>
        </div>

        <form className="mt-6 space-y-4">
          <label className="block">
            <span className="text-sm font-medium text-slate-700">Email</span>
            <input
              className="mt-1 h-11 w-full rounded-md border border-slate-300 px-3 text-sm outline-none focus:border-slate-950"
              defaultValue="admin@researchai.local"
              type="email"
            />
          </label>

          <label className="block">
            <span className="text-sm font-medium text-slate-700">Password</span>
            <input
              className="mt-1 h-11 w-full rounded-md border border-slate-300 px-3 text-sm outline-none focus:border-slate-950"
              defaultValue="Admin123!"
              type="password"
            />
          </label>

          <button
            className="h-11 w-full rounded-md bg-slate-950 text-sm font-semibold text-white hover:bg-slate-800"
            type="button"
          >
            Sign in
          </button>
        </form>

        <p className="mt-4 text-sm leading-6 text-slate-500">
          API connection will be enabled in the next step.
        </p>
      </section>
    </main>
  )
}

export default LoginPage
