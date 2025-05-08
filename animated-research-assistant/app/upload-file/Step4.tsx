// Step4.tsx
"use client"
import { useEffect, useState } from "react"

type Step4Props = {
  taskName: string
}

type Log = {
  agent: string
  message: string
}

export default function Step4({ taskName }: Step4Props) {
  const [logs, setLogs] = useState<Log[]>([])

  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/${taskName}`)

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      setLogs((prev) => [...prev, data])
    }

    ws.onerror = () => {
      setLogs((prev) => [...prev, { agent: "system", message: "连接错误" }])
    }

    return () => ws.close()
  }, [taskName])

  return (
    <div>
      <h2 className="text-xl font-semibold text-white mb-4">任务执行中</h2>
      <div className="h-64 overflow-y-auto bg-black/80 border border-gray-700 rounded p-4 text-sm font-mono">
        {logs.map((log, index) => (
          <div key={index} className="mb-1">
            <span className="text-purple-400">{log.agent}</span>:{" "}
            <span className="text-white">{log.message}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
