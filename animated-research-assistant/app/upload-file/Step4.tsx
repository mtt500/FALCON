import { useEffect, useState, useRef } from "react";
import { Spinner } from "@/components/ui/spinner";
import { Upload, Search, ShieldCheck, ArrowRight } from "lucide-react";
import { motion } from "framer-motion";
import { AnimatedBeam } from "@/components/AnimatedBeam";
import { FloatingPaper } from "@/components/floating-paper";
import { RoboAnimation } from "@/components/robo-animation";

// 呼吸边框动画 CSS，可以放在 global.css 或直接写在 <style> 标签里
// 也可以放到 Tailwind config 的 extend -> keyframes 里
const glowAnimation = `
@keyframes glow {
  0%, 100% { box-shadow: 0 0 0px 0px rgba(168, 85, 247, 0.6); }
  50% { box-shadow: 0 0 15px 5px rgba(168, 85, 247, 0.9); }
}
.animate-glow {
  animation: glow 1.5s ease-in-out infinite;
}
`;

export default function Step4({
  taskName,
  model,
  file,
  message1,
}: {
  taskName: string;
  model: string;
  file: File | null;
  message1: string;
}) {
  const [displayedMessage, setDisplayedMessage] = useState("");
  const [messageIndex, setMessageIndex] = useState(0);

  const containerRef = useRef(null);
  const fromRef = useRef(null);
  const toRef = useRef(null);

  const steps = [
    {
      icon: <Upload className="w-8 h-8 text-purple-500" />,
      title: "正在反编译",
      desc: "正在反编译固件代码...",
    },
    {
      icon: <Search className="w-8 h-8 text-purple-500" />,
      title: "正在进行漏洞扫描",
      desc: "决策agent运行检测，精准识别潜在威胁...",
    },
    {
      icon: <ShieldCheck className="w-8 h-8 text-purple-500" />,
      title: "正在获取报告",
      desc: "正在生成漏洞检测报告...",
    },
  ];

  useEffect(() => {
    if (messageIndex < message1.length) {
      const interval = setInterval(() => {
        setDisplayedMessage((prev) => prev + message1[messageIndex]);
        setMessageIndex((prev) => prev + 1);
      }, 100);
     return () => clearInterval(interval); // 清理定时器
    } else if (messageIndex === message1.length) {
      setTimeout(() => {
        // 当 message1 打印完成后，直接跳转到 /report 页面
        window.location.href = "/report"; // 直接跳转
      }, 50000); // 延迟50秒后跳转
    }
  }, [messageIndex, message1]);

  return (
    <>
      {/* 将动画样式直接注入页面 */}
      <style>{glowAnimation}</style>

      <div className="min-h-screen text-white relative" ref={containerRef}>
        {/* 三步骤流程卡片 */}
        <section className="flex flex-col items-center gap-8 md:flex-row md:justify-center px-6 pb-24 z-10 relative">
          {steps.map(({ icon, title, desc }, i) => {
            const [highlight, setHighlight] = useState(true);

            return (
              <motion.div
                key={i}
                className="flex items-center gap-4"
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 10, duration: 1, ease: "easeOut" }}
                onAnimationComplete={() => setTimeout(() => setHighlight(false), 10000)} // 1.5s 后停止呼吸效果
              >
                <div
                  ref={i === 0 ? fromRef : i === 2 ? toRef : undefined}
                  className={`bg-gray-900/60 p-6 rounded-xl backdrop-blur-md border border-gray-800 shadow-lg w-72 text-left transition hover:scale-105 ${
                    highlight ? "animate-glow border-purple-500" : ""
                  }`}
                >
                  <div className="mb-4">{icon}</div>
                  <h3 className="text-xl font-semibold mb-2">{title}</h3>
                  <p className="text-gray-400">{desc}</p>
                </div>
                {i < steps.length - 1 && (
                  <ArrowRight className="text-purple-500 w-6 h-6 hidden md:inline" />
                )}
              </motion.div>
            );
          })}
        </section>

        {/* 光束动画效果 */}
        <AnimatedBeam
          containerRef={containerRef}
          fromRef={fromRef}
          toRef={toRef}
          pathWidth={2}
          gradientStartColor="#00f0ff"
          gradientStopColor="#a000ff"
        />

        {/* 分析任务信息展示 */}
        <div className="flex flex-col items-center justify-center space-y-6 z-10 relative">
          <h2 className="text-2xl font-semibold text-white">正在分析任务...</h2>
          <div className="bg-gray-800 p-4 rounded-xl text-white w-full max-w-md">
            <p><strong>任务名称:</strong> {taskName}</p>
            <p><strong>固件型号:</strong> {model}</p>
            <p><strong>上传文件:</strong> {file ? file.name : "未选择文件"}</p>
          </div>

          <p className="text-gray-400 mt-4">请稍候，系统正在处理您的任务。</p>
          <div className="text-sm text-gray-400 mt-4">{displayedMessage}</div>
          <Spinner className="text-purple-600 h-12 w-12 animate-spin" />
          <p className="text-sm text-gray-400 mt-4">分析过程可能需要几分钟，请耐心等待。</p>
        </div>
      </div>
    </>
  );
}
