"use client"

import React, { useState } from "react"
import Step1 from "./Step1"
import Step2 from "./Step2"
import Step3 from "./Step3"
import Step4 from "./Step4"  // 导入第四步组件
// import Link from "next/link"
import HIW from "@/components/HIW"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { SparklesCore } from "@/components/SparklesCore"
import {FloatingPaper} from "@/components/floating-paper"
import { RoboAnimation } from "@/components/robo-animation"
import Reportbody from "@/components/Reportbody";
// import { useRouter } from "next/router";

export default function UploadWizardPage() {
  const [step, setStep] = useState(1)  // 当前步骤，初始为步骤 1
  const [taskName, setTaskName] = useState("")  // 任务名称
  const [model, setModel] = useState("")  // 固件型号
  const [file, setFile] = useState<File | null>(null)  // 上传的文件，初始为 null
  const [message1, setMessage1] = useState("")  // 用于存储后端返回的 message1
  // const [isLoading, setIsLoading] = useState(false)  // 用于控制加载状态
  // const router = useRouter()  // 用于跳转到 /report

  // const next = () => setStep((prev) => Math.min(prev + 1, 3))  // 下一步
  const prev = () => setStep((prev) => Math.max(prev - 1, 1))  // 上一步
  const next = () => {
  setStep((prev) => {
    const newStep = Math.min(prev + 1, 4);
    console.log("当前步骤：", newStep);  // 打印新的步骤
    return newStep;
  });
};

  // 提交任务处理函数
  const handleSubmit = async () => {
    // 检查是否填写完整信息
    if (!taskName || !model || !file) {
      alert("请填写完整信息")
      return
    }

    // 创建 FormData 对象，将文件加入到表单数据中
    const formData = new FormData()
    formData.append("file", file)

    try {
      // 发送 POST 请求，将文件上传到后端
      const res = await fetch("http://localhost:8000/upload/", {
        method: "POST",
        body: formData,  // 将文件数据作为请求体发送
      })

      // 如果响应状态不是 OK（200），抛出错误
      if (!res.ok) throw new Error(`HTTP ${res.status}`)

      // 打印后端返回的原始响应内容和类型
      const text = await res.text()
      // 解析响应为 JSON 格式
      const data = JSON.parse(text)
      console.log('message2:', data.message2)

      // alert(`后端返回：\n${data.message1}\n${data.message2}`)

      // 获取后端返回的 message1
      setMessage1(data.message1)


      // 提交成功后，跳转到第四步
      // setIsLoading(true)  // 开始加载动画
      next()  // 跳到第四步
      console.log('已经跳转第四步？')
    } catch (err) {
      console.error(err)
      alert("上传失败，请查看控制台日志")
    }
  }

  return (
    <div className="min-h-screen bg-black text-white relative overflow-hidden">
      {/* 导航栏 */}
       <div className="relative z-10">
        <HIW />
      </div>

      {/* 背景粒子效果 */}
      <div className="fixed inset-0 z-0">
        <SparklesCore
          id="wizard-bg"
          background="transparent"
          className="absolute inset-0 z-0"
          particleColor="#8b5cf6"
          particleDensity={80}
          minSize={0.5}
          maxSize={1.4}
        />
      </div>

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
            className="mb-8 h-2 w-[1200px] bg-gray-800 [&>div]:bg-purple-600"
        />


        {/* 各步骤组件 */}
        <div className="bg-gray-900/70 border border-gray-800 rounded-xl p-8 shadow-xl backdrop-blur-md text-left space-y-6 w-[1200px]">
          {step === 1 && <Step1 taskName={taskName} setTaskName={setTaskName} />}
          {step === 2 && <Step2 model={model} setModel={setModel} />}
          {step === 3 && <Step3 file={file} setFile={setFile} />}
          {/* 将 message1 传递到第四步 */}
          {/* {step === 4 && <Step4 taskName={taskName} model={model} file={file} message1={message1} />} */}
          {step === 4 && <Step4 taskName={taskName} model={model} file={file} />}
        </div>

        {/* 步骤控制按钮 */}
        <div className="mt-8 flex justify-between w-full">
          {/* 只有在 step !== 4 时才显示 "上一步" 按钮 */}
          {step !== 4 && (
            <Button variant="outline" onClick={prev} disabled={step === 1}>上一步</Button>
          )}

          {step === 1 || step === 2 ? (
            <Button className="bg-purple-600 hover:bg-purple-700 text-white" onClick={next}>下一步</Button>
          ) : null}

          {step === 3 ? (
            <Button className="bg-purple-600 hover:bg-purple-700 text-white" onClick={handleSubmit}>
              创建任务
            </Button>
          ) : null}

        </div>
      </div>
        <div className="absolute bottom-10 right-10 w-60 h-60 z-10 pointer-events-none">
        <RoboAnimation />
      </div>
    </div>
  )
}
