import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"

export default function Step1({ taskName, setTaskName }: {
  taskName: string
  setTaskName: (value: string) => void
}) {
  return (
    <div>
      <Label className="block mb-2 text-gray-300">任务名称</Label>
      <Input
        className="bg-black border-gray-700 text-white"
        placeholder="如：扫描路由器固件V1.0"
        value={taskName}
        onChange={(e) => setTaskName(e.target.value)}
      />
    </div>
  )
}
