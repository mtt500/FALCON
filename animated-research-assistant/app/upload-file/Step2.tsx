import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"

export default function Step2({ model, setModel }: {
  model: string
  setModel: (value: string) => void
}) {
  return (
    <div>
      <Label className="block mb-2 text-gray-300">固件型号</Label>
      <Input
        className="bg-black border-gray-700 text-white"
        placeholder="如：TP-Link AX1800"
        value={model}
        onChange={(e) => setModel(e.target.value)}
      />
    </div>
  )
}
