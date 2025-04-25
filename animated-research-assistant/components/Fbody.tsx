"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { SparklesCore } from "@/components/SparklesCore"
import { Progress } from "@/components/ui/progress"
import { FloatingPaper } from "@/components/floating-paper"
import { RoboAnimation } from "@/components/robo-animation"

export default function UploadWizardStep1() {
  const [firmwareName, setFirmwareName] = useState("")
  const [file, setFile] = useState<File | null>(null)

  return (
    <div className="min-h-screen bg-black text-white relative px-6 py-12">
      {/* 粒子背景 */}
     <div className="relative min-h-[calc(100vh-76px)] flex items-center">
      {/* Floating papers background */}
      <div className="absolute inset-0 overflow-hidden">
        <FloatingPaper count={6} />
      </div>

      {/* 主体卡片容器 */}
      <div className="relative z-10 max-w-2xl mx-auto text-center">
        <h1 className="text-3xl font-bold text-white mb-2">创建漏洞检测任务</h1>
        <p className="text-gray-400 mb-6">上传固件文件，开始自动化漏洞分析</p>

        {/* 顶部进度条 */}
        <Progress value={33} className="mb-8 h-2 bg-gray-700" />

        {/* 卡片内容 */}
        <div className="bg-gray-900/70 border border-gray-800 rounded-xl p-8 shadow-xl backdrop-blur-md text-left space-y-6">
          <div>
            <Label className="block mb-2 text-gray-300">固件名称</Label>
            <Input
              className="bg-black border-gray-700 text-white"
              placeholder="如：router_v1.2.0.bin"
              value={firmwareName}
              onChange={(e) => setFirmwareName(e.target.value)}
            />
          </div>

          <div>
            <Label className="block mb-2 text-gray-300">上传文件</Label>
            <Input
              type="file"
              className="bg-black border-gray-700 text-white"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
            />
            {file && <p className="text-sm text-gray-400 mt-2">已选择：{file.name}</p>}
          </div>
        </div>

        {/* 步骤导航按钮 */}
        <div className="mt-8 flex justify-between">
          <Button variant="outline" disabled>上一步</Button>
          <Button className="bg-purple-600 hover:bg-purple-700 transition-colors">
            下一步
          </Button>
        </div>
      </div>
    </div>
       <div className="absolute bottom-10 right-10 w-60 h-60 z-10 pointer-events-none">
        <RoboAnimation />
      </div>
    </div>
  )
}
