import type { AnalysisLog } from '../types/analysis'

interface Props {
  logs: AnalysisLog[]
  onRefresh: () => void
}

export function LogTable({ logs, onRefresh }: Props) {
  return (
    <div className="bg-white rounded-xl shadow p-7">
      <div className="flex justify-between items-center mb-5">
        <h2 className="text-base font-semibold text-slate-800 flex items-center gap-2">
          <span className="w-1 h-5 bg-slate-800 rounded inline-block" />
          分析ログ（最新50件）
        </h2>
        <button
          onClick={onRefresh}
          className="px-4 py-2 border border-slate-800 text-slate-800 rounded-lg text-sm font-semibold hover:bg-slate-800 hover:text-white transition-colors"
        >
          ↻ 更新
        </button>
      </div>
      <div className="overflow-x-auto rounded-lg border border-slate-200">
        <table className="w-full text-sm">
          <thead className="bg-slate-50">
            <tr>
              {['ID','Status','Image Path','Class','Confidence','Message','Request Time','Response Time'].map(h => (
                <th key={h} className="px-4 py-3 text-left font-semibold text-slate-500 whitespace-nowrap border-b border-slate-200">{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {logs.length === 0 ? (
              <tr><td colSpan={8} className="text-center py-10 text-slate-400">まだ分析ログがありません</td></tr>
            ) : logs.map(log => (
              <tr key={log.id} className="hover:bg-slate-50 border-b border-slate-100 last:border-0">
                <td className="px-4 py-3">{log.id}</td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-0.5 rounded-full text-xs font-bold ${log.is_success ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-600'}`}>
                    {log.is_success ? 'SUCCESS' : 'FAILURE'}
                  </span>
                </td>
                <td className="px-4 py-3 max-w-[200px] truncate text-slate-500 text-xs" title={log.image_path ?? ''}>{log.image_path ?? '-'}</td>
                <td className="px-4 py-3">{log.class_label ?? '-'}</td>
                <td className="px-4 py-3">
                  {log.confidence != null ? (
                    <div className="flex items-center gap-2">
                      <div className="w-14 h-1.5 bg-slate-200 rounded overflow-hidden">
                        <div className="h-full bg-gradient-to-r from-slate-700 to-blue-400 rounded" style={{ width: `${Math.round(log.confidence * 100)}%` }} />
                      </div>
                      {log.confidence.toFixed(4)}
                    </div>
                  ) : '-'}
                </td>
                <td className="px-4 py-3">{log.message ?? '-'}</td>
                <td className="px-4 py-3 whitespace-nowrap">{log.request_timestamp?.replace('T', ' ').slice(0, 19) ?? '-'}</td>
                <td className="px-4 py-3 whitespace-nowrap">{log.response_timestamp?.replace('T', ' ').slice(0, 19) ?? '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
