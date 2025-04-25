"use client"

import React, { useState } from "react"
import Step1 from "./Step1"
import Step2 from "./Step2"
import Step3 from "./Step3"
import Link from "next/link"
import Fhead from "@/components/Fhead"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { SparklesCore } from "@/components/SparklesCore"
import {FloatingPaper} from "@/components/floating-paper"
import { RoboAnimation } from "@/components/robo-animation";

export default function UploadWizardPage() {
  const [step, setStep] = useState(1)
  const [taskName, setTaskName] = useState("")
  const [model, setModel] = useState("")
  const [file, setFile] = useState<File | null>(null)

  const next = () => setStep((prev) => Math.min(prev + 1, 3))
  const prev = () => setStep((prev) => Math.max(prev - 1, 1))

  const handleSubmit = () => {
    if (!taskName || !model || !file) {
      alert("请填写完整信息")
      return
    }
    alert(`创建成功：\n任务名称: ${taskName}\n固件型号: ${model}\n文件: ${file.name}`)
    // 可替换为路由跳转或 API 提交逻辑
  }

  return (
    <div className="min-h-screen bg-black text-white relative overflow-hidden">
      {/* 导航栏 */}
      <Fhead />

      {/* 背景粒子效果 */}
      <SparklesCore
        id="wizard-bg"
        background="transparent"
        className="absolute inset-0 z-0"
        particleColor="#8b5cf6"
        particleDensity={80}
        minSize={0.5}
        maxSize={1.4}
      />

      <div className="absolute inset-0 overflow-hidden">
        <FloatingPaper count={6} />
      </div>

      {/* 主体内容区域 */}
      <div className="relative z-10 max-w-2xl mx-auto flex flex-col items-center justify-center min-h-[calc(100vh-80px)] text-center px-6 py-8">
        <h1 className="text-3xl font-bold text-white mb-2">创建检测任务</h1>
        <p className="text-gray-400 mb-6">快速配置任务，开始检测</p>

        {/* 顶部进度条 */}
        <Progress
            value={(step / 3) * 100}
            className="mb-8 h-2 bg-gray-800 [&>div]:bg-purple-600"
        />


        {/* 各步骤组件 */}
        <div className="bg-gray-900/70 border border-gray-800 rounded-xl p-8 shadow-xl backdrop-blur-md text-left space-y-6 w-full">
          {step === 1 && <Step1 taskName={taskName} setTaskName={setTaskName} />}
          {step === 2 && <Step2 model={model} setModel={setModel} />}
          {step === 3 && <Step3 file={file} setFile={setFile} />}
        </div>

        {/* 步骤控制按钮 */}
        <div className="mt-8 flex justify-between w-full">
          <Button variant="outline" onClick={prev} disabled={step === 1}>上一步</Button>
          {step < 3 ? (
            <Button className="bg-purple-600 hover:bg-purple-700 text-white" onClick={next}>下一步</Button>
          ) : (
              <Link href="/">
                <Button className="bg-purple-600 hover:bg-purple-700 text-white" onClick={handleSubmit}>创建任务</Button>
              </Link>
          )}
        </div>
      </div>
        <div className="absolute bottom-10 right-10 w-60 h-60 z-10 pointer-events-none">
        <RoboAnimation />
      </div>
    </div>
  )
}
