"use client"

import { useEffect, useState } from "react"
import { motion } from "framer-motion"

interface AnimatedBeamProps {
  containerRef: React.RefObject<HTMLElement>
  fromRef: React.RefObject<HTMLElement>
  toRef: React.RefObject<HTMLElement>
  pathColor?: string
  pathWidth?: number
  gradientStartColor?: string
  gradientStopColor?: string
}

export const AnimatedBeam = ({
  containerRef,
  fromRef,
  toRef,
  pathColor = "gray",
  pathWidth = 2,
  gradientStartColor = "#ffaa40",
  gradientStopColor = "#9c40ff",
}: AnimatedBeamProps) => {
  const [path, setPath] = useState("")

  useEffect(() => {
    const updatePath = () => {
      if (
        !containerRef.current ||
        !fromRef.current ||
        !toRef.current
      ) return

      const containerRect = containerRef.current.getBoundingClientRect()
      const fromRect = fromRef.current.getBoundingClientRect()
      const toRect = toRef.current.getBoundingClientRect()

      const startX = fromRect.left + fromRect.width / 2 - containerRect.left
      const startY = fromRect.top + fromRect.height / 2 - containerRect.top
      const endX = toRect.left + toRect.width / 2 - containerRect.left
      const endY = toRect.top + toRect.height / 2 - containerRect.top

      const curvature = 0.4
      const dx = endX - startX
      const dy = endY - startY
      const curveX = startX + dx * curvature
      const curveY = startY + dy * curvature

      const svgPath = `M ${startX} ${startY} Q ${curveX} ${curveY} ${endX} ${endY}`
      setPath(svgPath)
    }

    updatePath()
    window.addEventListener("resize", updatePath)
    return () => window.removeEventListener("resize", updatePath)
  }, [containerRef, fromRef, toRef])

  return (
    <svg className="absolute top-0 left-0 w-full h-full pointer-events-none z-0">
      <defs>
        <linearGradient id="beamGradient" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stopColor={gradientStartColor} />
          <stop offset="100%" stopColor={gradientStopColor} />
        </linearGradient>
      </defs>
      <motion.path
        d={path}
        stroke="url(#beamGradient)"
        strokeWidth={pathWidth}
        fill="none"
        initial={{ pathLength: 0 }}
        animate={{ pathLength: 1 }}
        transition={{ duration: 1.5, ease: "easeInOut" }}
      />
    </svg>
  )
}
