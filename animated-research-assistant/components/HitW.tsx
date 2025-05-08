"use client"

import { Upload, Search, ShieldCheck, ArrowRight } from "lucide-react"
import { motion } from "framer-motion"
import React, { useRef } from "react"
import { AnimatedBeam } from "@/components/AnimatedBeam"
import {FloatingPaper} from "@/components/floating-paper";
import {SparklesCore} from "@/components/SparklesCore"; // 确保路径正确
import AnimatedBeamMultipleOutputDemo from "@/components/animated-beam-multiple-outputs"
import {RoboAnimation} from "@/components/robo-animation";


export default function HowItWorks() {
  const containerRef = useRef(null)
  const fromRef = useRef(null)
  const toRef = useRef(null)

  const steps = [
    {
      icon: <Upload className="w-8 h-8 text-purple-500" />,
      title: "上传目标",
      desc: "上传固件或输入网站地址。",
    },
    {
      icon: <Search className="w-8 h-8 text-purple-500" />,
      title: "漏洞扫描",
      desc: "系统自动运行多引擎检测，精准识别潜在威胁。",
    },
    {
      icon: <ShieldCheck className="w-8 h-8 text-purple-500" />,
      title: "获取报告",
      desc: "实时展示漏洞详情与修复建议。",
    },
  ]

  return (
    <div className="min-h-screen text-white relative" ref={containerRef}>
      {/* 标题介绍 */}
      <div className="absolute inset-0 overflow-hidden">
        <FloatingPaper count={6} />
      </div>

      <section className="text-center py-16 px-6 max-w-3xl mx-auto z-10 relative">
        <h2 className="text-4xl font-bold text-white mb-4">How It Works</h2>
        <p className="text-gray-400 text-lg">
          FALCON 自动分析固件/网站漏洞并提供可操作的安全建议。只需三步，即可获取安全洞察。
        </p>
      </section>

      {/* 三步骤流程卡片 + 箭头指示 */}
      <section className="flex flex-col items-center gap-8 md:flex-row md:justify-center px-6 pb-24 z-10 relative">
        {steps.map(({ icon, title, desc }, i) => (
          <div key={i} className="flex items-center gap-4">
            <div
              ref={i === 0 ? fromRef : i === 2 ? toRef : undefined}
              className="bg-gray-900/60 p-6 rounded-xl backdrop-blur-md border border-gray-800 shadow-lg w-72 text-left transition hover:scale-105"
            >
              <div className="mb-4">{icon}</div>
              <h3 className="text-xl font-semibold mb-2">{title}</h3>
              <p className="text-gray-400">{desc}</p>
            </div>
            {i < steps.length - 1 && (
              <ArrowRight className="text-purple-500 w-6 h-6 hidden md:inline" />
            )}
          </div>
        ))}
      </section>

      {/* 光束动画效果连接第一个和最后一个卡片 */}
      <AnimatedBeam
        containerRef={containerRef}
        fromRef={fromRef}
        toRef={toRef}
        pathWidth={2}
        gradientStartColor="#00f0ff"
        gradientStopColor="#a000ff"
      />
        {/* 插件组件插入位置 */}
          <div className="flex justify-center mb-6">
            <AnimatedBeamMultipleOutputDemo/>
          </div>
        <div className="absolute bottom-0 right-0 w-96 h-96">
        <RoboAnimation />
      </div>
    </div>
  )
}
