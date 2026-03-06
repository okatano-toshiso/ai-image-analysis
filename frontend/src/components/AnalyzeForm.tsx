import { useState } from 'react'
import type { AnalyzeResult } from '../types/analysis'

interface Props {
  onAnalyzed: () => void
}

export function AnalyzeForm({ onAnalyzed }: Props) {
  const [imagePath, setImagePath] = useState('')
  const [result, setResult] = useState<AnalyzeResult | null>(null)
  const [loading, setLoading] = useState(false)

  const handleAnalyze = async () => {
    setLoading(true)
    const formData = new FormData()
    formData.append('image_path', imagePath.trim())
    try {
      const res = await fetch('/analyze', { method: 'POST', body: formData })
      const data: AnalyzeResult = await res.json()
      setResult(data)
      onAnalyzed()
    } catch (e) {
      alert('Error: ' + (e as Error).message)
    } finally {
      setLoading(false)
    }
  }

  const success = result?.api_response.is_success

  return (
    <div className="bg-white rounded-xl shadow p-7 mb-8">
      <h2 className="text-base font-semibold text-slate-800 mb-5 flex items-center gap-2">
        <span className="w-1 h-5 bg-slate-800 rounded inline-block" />
        画像分析
      </h2>
      <div className="flex gap-3">
        <input
          type="text"
          value={imagePath}
          onChange={e => setImagePath(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleAnalyze()}
          placeholder="/image/demo.png"
          className="flex-1 px-4 py-3 border border-slate-200 rounded-lg text-sm bg-slate-50 focus:outline-none focus:border-slate-700 focus:bg-white"
        />
        <button
          onClick={handleAnalyze}
          disabled={loading}
          className="px-7 py-3 bg-slate-800 text-white rounded-lg text-sm font-semibold hover:bg-slate-700 disabled:bg-slate-400 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? '分析中...' : '分析実行'}
        </button>
      </div>

      {result && (
        <div className={`mt-5 rounded-lg p-5 border ${success ? 'bg-green-50 border-green-300' : 'bg-red-50 border-red-300'}`}>
          <div className="flex items-center gap-2 font-bold mb-3">
            <span className={`px-2 py-0.5 rounded-full text-xs font-bold text-white ${success ? 'bg-green-500' : 'bg-red-500'}`}>
              {success ? 'SUCCESS' : 'FAILURE'}
            </span>
            <span>{result.api_response.message}</span>
          </div>
          <div className="grid grid-cols-3 gap-3">
            {success && (
              <>
                <div className="bg-white rounded-lg p-3 shadow-sm">
                  <div className="text-xs text-slate-400 uppercase tracking-wide mb-1">Class</div>
                  <div className="text-lg font-bold">{result.log.class_label ?? '-'}</div>
                </div>
                <div className="bg-white rounded-lg p-3 shadow-sm">
                  <div className="text-xs text-slate-400 uppercase tracking-wide mb-1">Confidence</div>
                  <div className="text-lg font-bold">{result.log.confidence?.toFixed(4) ?? '-'}</div>
                </div>
              </>
            )}
            <div className="bg-white rounded-lg p-3 shadow-sm">
              <div className="text-xs text-slate-400 uppercase tracking-wide mb-1">DB ID</div>
              <div className="text-lg font-bold">#{result.log.id}</div>
            </div>
          </div>
        </div>
      )}

      {/* Raw JSON Viewer */}
      {result && (
        <details className="mt-4">
          <summary className="cursor-pointer text-xs text-slate-500 hover:text-slate-700 select-none">
            Raw JSON
          </summary>
          <pre className="mt-2 p-4 bg-slate-900 text-green-400 text-xs rounded-lg overflow-x-auto leading-relaxed">
            {JSON.stringify(result, null, 2)}
          </pre>
        </details>
      )}
    </div>
  )
}
