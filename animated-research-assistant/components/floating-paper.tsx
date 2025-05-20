"use client"

import { useEffect, useState } from "react"
import { motion } from "framer-motion"

// ✅ 自定义芯片图标组件
function FirmwareChipIcon({ className = "" }) {
  return (
    <svg
      className={className}
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      viewBox="0 0 24 24"
      xmlns="http://www.w3.org/2000/svg"
    >
      <rect x="5" y="5" width="14" height="14" rx="2" ry="2" />
      <path d="M9 2v3" />
      <path d="M12 2v3" />
      <path d="M15 2v3" />
      <path d="M9 19v3" />
      <path d="M12 19v3" />
      <path d="M15 19v3" />
      <path d="M2 9h3" />
      <path d="M2 12h3" />
      <path d="M2 15h3" />
      <path d="M19 9h3" />
      <path d="M19 12h3" />
      <path d="M19 15h3" />
      <circle cx="12" cy="12" r="2" />
    </svg>
  )
}

// ✅ 浮动芯片动画组件
export function FloatingPaper({ count = 7 }) {
  const [dimensions, setDimensions] = useState({ width: 1200, height: 800 })

  useEffect(() => {
    const updateDimensions = () => {
      setDimensions({
        width: window.innerWidth,
        height: window.innerHeight,
      })
    }

    // 初始化和监听窗口大小变化
    updateDimensions()
    window.addEventListener("resize", updateDimensions)
    return () => window.removeEventListener("resize", updateDimensions)
  }, [])

  return (
    <div className="relative w-full h-full">
      {Array.from({ length: count }).map((_, i) => (
        <motion.div
          key={i}
          className="absolute"
          initial={{
            x: Math.random() * dimensions.width,
            y: Math.random() * dimensions.height,
          }}
          animate={{
            x: [
              Math.random() * dimensions.width,
              Math.random() * dimensions.width,
              Math.random() * dimensions.width,
            ],
            y: [
              Math.random() * dimensions.height,
              Math.random() * dimensions.height,
              Math.random() * dimensions.height,
            ],
            rotate: [0, 180, 360],
          }}
          transition={{
            duration: 20 + Math.random() * 10,
            repeat: Infinity,
            ease: "linear",
          }}
        >
          <div className="relative w-16 h-20 bg-white/5 backdrop-blur-sm rounded-lg border border-white/10 flex items-center justify-center transform hover:scale-110 transition-transform">
            <img
              src="/固件管理.svg"
              alt="Firmware Icon"
              className="w-8 h-8 opacity-50"
            />
          </div>
        </motion.div>
      ))}
    </div>
  )
}
