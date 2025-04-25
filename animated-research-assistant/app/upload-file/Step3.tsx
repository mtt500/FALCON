import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"

export default function Step3({ file, setFile }: {
  file: File | null
  setFile: (file: File | null) => void
}) {
  return (
    <div>
      <Label className="block mb-2 text-gray-300">上传固件文件</Label>
      <Input
        type="file"
        className="bg-black border-gray-700 text-white"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />
      {file && <p className="text-sm text-gray-400 mt-2">已选择：{file.name}</p>}
    </div>
  )
}
