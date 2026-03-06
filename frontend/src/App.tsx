import { useEffect, useState, useCallback } from 'react'
import { AnalyzeForm } from './components/AnalyzeForm'
import { LogTable } from './components/LogTable'
import type { AnalysisLog } from './types/analysis'

export default function App() {
  const [logs, setLogs] = useState<AnalysisLog[]>([])

  const fetchLogs = useCallback(async () => {
    const res = await fetch('/logs')
    const data: AnalysisLog[] = await res.json()
    setLogs(data)
  }, [])

  useEffect(() => { fetchLogs() }, [fetchLogs])

  return (
    <div className="min-h-screen bg-slate-100 text-slate-900">
      <header className="bg-gradient-to-r from-slate-900 to-slate-700 text-white px-10 py-6 shadow-lg">
        <h1 className="text-xl font-semibold tracking-wide">🤖 AI Image Analysis</h1>
        <p className="text-sm text-slate-400 mt-1">Submit an image path for AI analysis and view results.</p>
      </header>
      <main className="max-w-5xl mx-auto px-6 py-8">
        <AnalyzeForm onAnalyzed={fetchLogs} />
        <LogTable logs={logs} onRefresh={fetchLogs} />
      </main>
    </div>
  )
}
