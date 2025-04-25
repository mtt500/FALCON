"use client"

import type React from "react"
import { forwardRef, useRef } from "react"
import { cn } from "@/lib/utils"
import { AnimatedBeam } from "@/components/magicui/animated-beam"
import { User, FileText, Bot } from "lucide-react"
import {RoboAnimation} from "@/components/robo-animation";

const Circle = forwardRef<HTMLDivElement, { className?: string; children?: React.ReactNode }>(
  ({ className, children }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          "z-10 flex size-12 items-center justify-center rounded-full border-2 bg-white p-3 shadow-[0_0_20px_-12px_rgba(0,0,0,0.8)]",
          className,
        )}
      >
        {children}
      </div>
    )
  },
)

Circle.displayName = "Circle"

export default function AnimatedBeamDemo() {
  const containerRef = useRef<HTMLDivElement>(null)
  const userRef = useRef<HTMLDivElement>(null)
  const openaiRef = useRef<HTMLDivElement>(null)
  const botPurpleRef = useRef<HTMLDivElement>(null)
  const botGreenRef = useRef<HTMLDivElement>(null)
  const botYellowRef = useRef<HTMLDivElement>(null)
  const docsRef = useRef<HTMLDivElement>(null)

  return (
    <div
      ref={containerRef}
        className="relative flex items-center justify-center overflow-hidden
                   rounded-xl p-6 md:shadow-xl
                   w-[1000px] h-[420px]
                   border-2 border-white/50
                   hover:border-purple-500 transition-all duration-500
                   hover:shadow-[0_0_20px_4px_rgba(139,92,246,0.4)] hover:animate-pulse"
    >
      <div className="flex size-full max-w-[800px] items-center justify-between">
        {/* Left side - User icon */}
        <Circle ref={userRef} className="size-16">
          <User className="h-8 w-8 text-gray-700" />
        </Circle>



        {/* Middle left - OpenAI icon */}
        <Circle ref={openaiRef} className="size-16">
          <OpenAIIcon />
        </Circle>


        {/* Middle right - Stacked bot icons */}
        <div className="flex flex-col gap-4">
          <Circle ref={botPurpleRef} className="border-purple-500">
            <Bot className="h-6 w-6 text-purple-500" />
          </Circle>
          <Circle ref={botGreenRef} className="border-green-500">
            <Bot className="h-6 w-6 text-green-500" />
          </Circle>
          <Circle ref={botYellowRef} className="border-yellow-500">
            <Bot className="h-6 w-6 text-yellow-500" />
          </Circle>
        </div>

        {/* Right side - Docs icon */}
        <Circle ref={docsRef} className="size-16">
          <FileText className="h-8 w-8 text-gray-700" />
        </Circle>
      </div>

      {/* Beams from user to OpenAI */}
      <AnimatedBeam containerRef={containerRef} fromRef={userRef} toRef={openaiRef} curvature={-20} />

      {/* Beams from OpenAI to bots */}
      <AnimatedBeam
        containerRef={containerRef}
        fromRef={openaiRef}
        toRef={botPurpleRef}
        curvature={-20}
        gradientStartColor="#9c40ff"
        gradientStopColor="#9c40ff"
        startXOffset={0}
        startYOffset={0}
      />
      <AnimatedBeam
        containerRef={containerRef}
        fromRef={openaiRef}
        toRef={botGreenRef}
        gradientStartColor="#40ff9c"
        gradientStopColor="#40ff9c"
        startXOffset={0}
        startYOffset={0}
      />
      <AnimatedBeam
        containerRef={containerRef}
        fromRef={openaiRef}
        toRef={botYellowRef}
        curvature={20}
        gradientStartColor="#ffaa40"
        gradientStopColor="#ffaa40"
        startXOffset={0}
        startYOffset={0}
      />

      {/* Beams from bots to docs */}
      <AnimatedBeam
        containerRef={containerRef}
        fromRef={botPurpleRef}
        toRef={docsRef}
        curvature={-20}
        gradientStartColor="#9c40ff"
        gradientStopColor="#9c40ff"
        reverse
      />
      <AnimatedBeam
        containerRef={containerRef}
        fromRef={botGreenRef}
        toRef={docsRef}
        gradientStartColor="#40ff9c"
        gradientStopColor="#40ff9c"
        reverse
      />
      <AnimatedBeam
        containerRef={containerRef}
        fromRef={botYellowRef}
        toRef={docsRef}
        curvature={20}
        gradientStartColor="#ffaa40"
        gradientStopColor="#ffaa40"
        reverse
      />
    </div>

  )
}

const OpenAIIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
    <path d="M22.2819 9.8211a5.9847 5.9847 0 0 0-.5157-4.9108 6.0462 6.0462 0 0 0-6.5098-2.9A6.0651 6.0651 0 0 0 4.9807 4.1818a5.9847 5.9847 0 0 0-3.9977 2.9 6.0462 6.0462 0 0 0 .7427 7.0966 5.98 5.98 0 0 0 .511 4.9107 6.051 6.051 0 0 0 6.5146 2.9001A5.9847 5.9847 0 0 0 13.2599 24a6.0557 6.0557 0 0 0 5.7718-4.2058 5.9894 5.9894 0 0 0 3.9977-2.9001 6.0557 6.0557 0 0 0-.7475-7.0729zm-9.022 12.6081a4.4755 4.4755 0 0 1-2.8764-1.0408l.1419-.0804 4.7783-2.7582a.7948.7948 0 0 0 .3927-.6813v-6.7369l2.02 1.1686a.071.071 0 0 1 .038.052v5.5826a4.504 4.504 0 0 1-4.4945 4.4944zm-9.6607-4.1254a4.4708 4.4708 0 0 1-.5346-3.0137l.142.0852 4.783 2.7582a.7712.7712 0 0 0 .7806 0l5.8428-3.3685v2.3324a.0804.0804 0 0 1-.0332.0615L9.74 19.9502a4.4992 4.4992 0 0 1-6.1408-1.6464zM2.3408 7.8956a4.485 4.485 0 0 1 2.3655-1.9728V11.6a.7664.7664 0 0 0 .3879.6765l5.8144 3.3543-2.0201 1.1685a.0757.0757 0 0 1-.071 0l-4.8303-2.7865A4.504 4.504 0 0 1 2.3408 7.872zm16.5963 3.8558L13.1038 8.364 15.1192 7.2a.0757.0757 0 0 1 .071 0l4.8303 2.7913a4.4944 4.4944 0 0 1-.6765 8.1042v-5.6772a.79.79 0 0 0-.407-.667zm2.0107-3.0231l-.142-.0852-4.7735-2.7818a.7759.7759 0 0 0-.7854 0L9.409 9.2297V6.8974a.0662.0662 0 0 1 .0284-.0615l4.8303-2.7866a4.4992 4.4992 0 0 1 6.6802 4.66zM8.3065 12.863l-2.02-1.1638a.0804.0804 0 0 1-.038-.0567V6.0742a4.4992 4.4992 0 0 1 7.3757-3.4537l-.142.0805L8.704 5.459a.7948.7948 0 0 0-.3927.6813zm1.0976-2.3654l2.602-1.4998 2.6069 1.4998v2.9994l-2.5974 1.4997-2.6067-1.4997Z" />
  </svg>
)
