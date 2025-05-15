import { useEffect, useState, useRef } from "react";
import { Spinner } from "@/components/ui/spinner";
import { Upload, Search, ShieldCheck, ArrowRight } from "lucide-react";
import { motion } from "framer-motion";
import { AnimatedBeam } from "@/components/AnimatedBeam";

// 呼吸动画样式
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
}: {
  taskName: string;
  model: string;
  file: File | null;
}) {
  const [displayedMessage, setDisplayedMessage] = useState("");
  const [currentStep, setCurrentStep] = useState(0);
  const [isTyping, setIsTyping] = useState(false);
  const [hasStarted, setHasStarted] = useState(false); // 防止重复执行

  const currentTypingId = useRef<number | null>(null);
  const containerRef = useRef(null);
  const fromRef = useRef(null);
  const toRef = useRef(null);

  const steps = [
    {
      icon: <Upload className="w-8 h-8 text-purple-500" />,
      title: "正在反编译",
      desc: "正在反编译固件代码...",
      api: "upload",
    },
    {
      icon: <Search className="w-8 h-8 text-purple-500" />,
      title: "正在进行漏洞扫描",
      desc: "决策agent运行检测，精准识别潜在威胁...",
      api: "analysis",
    },
    {
      icon: <ShieldCheck className="w-8 h-8 text-purple-500" />,
      title: "正在获取报告",
      desc: "正在生成漏洞检测报告...",
      api: "report",
    },
  ];

  // 防重复打字逻辑
  const typeMessage = (message: string): Promise<void> => {
    return new Promise((resolve) => {
      let index = 0;
      setDisplayedMessage("");
      setIsTyping(true);
      const typingId = Date.now();
      currentTypingId.current = typingId;

      const interval = setInterval(() => {
        if (currentTypingId.current !== typingId) {
          clearInterval(interval); // 如果中途被打断，终止
          return;
        }

        setDisplayedMessage((prev) => prev + message[index]);
        index++;

        if (index === message.length) {
          clearInterval(interval);
          setIsTyping(false);
          resolve();
        }
      }, 50);
    });
  };

  // 主步骤流程控制器
  const runStepsSequentially = async () => {
    for (let i = 0; i < steps.length; i++) {
      setCurrentStep(i);
      const api = steps[i].api;

      try {
        const formData = new FormData();
        if (file) formData.append("file", file);

        const res = await fetch(`http://localhost:8000/${api}/`, {
          method: "POST",
          body: formData,
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);

        const text = await res.text();
        const data = JSON.parse(text);

        console.log(`来自 /${api}/ 的响应：`, data.message1);
        await typeMessage(data.message1);
      } catch (err) {
        console.error(`步骤 ${api} 加载失败:`, err);
        break;
      }
    }

    // alert('success')
    // window.location.href = "/report";
    setTimeout(() => {
        // 当 message 打印完成后，跳转到 /report 页面
        window.location.href = "/report"; // 直接跳转
    }, 1000); // 延迟1秒后跳转
  };

  // 确保 runStepsSequentially 只执行一次
  useEffect(() => {
    if (!hasStarted) {
      setHasStarted(true);
      runStepsSequentially();
    }
  }, [hasStarted]);

  return (
    <>
      <style>{glowAnimation}</style>

      <div className="min-h-screen text-white relative px-4" ref={containerRef}>
        {/* 步骤卡片区域 */}
        <section className="flex justify-between items-center gap-4 w-full max-w-6xl mx-auto pb-24 z-10 relative">
          {steps.map(({ icon, title, desc }, i) => (
            <div key={i} className="flex items-center w-1/3 min-w-[240px] justify-center">
              {i <= currentStep ? (
                <motion.div
                  className="flex flex-col items-center w-full"
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.6, ease: "easeOut" }}
                >
                  <div
                    ref={i === 0 ? fromRef : i === 2 ? toRef : undefined}
                    className={`bg-gray-900/60 p-6 rounded-xl backdrop-blur-md border border-gray-800 shadow-lg text-left w-full transition hover:scale-105 
                      ${i === currentStep && isTyping ? "animate-glow border-purple-500" : ""}
                      ${i === 1 ? "scale-105" : ""} // 第二个组件更大
                    `}
                  >
                    <div className="mb-4">{icon}</div>
                    <h3 className="text-xl font-semibold mb-2">{title}</h3>
                    <p className="text-gray-400">{desc}</p>
                  </div>
                </motion.div>
              ) : (
                <div className="w-full"></div>
              )}

              {/* 箭头（仅前两个组件后） */}
              {/* {i < 2 && (
                <div className="flex items-center justify-center ml-2">
                  <ArrowRight className="text-purple-500 w-6 h-6" />
                </div>
              )} */}
            {/* 连接第一和第二组件的箭头，只有当currentStep >= 1时显示 */}
            {i === 0 && currentStep >= 1 && (
                <div className="flex items-center justify-center ml-2">
                <ArrowRight className="text-purple-500 w-6 h-6" />
                </div>
            )}

            {/* 连接第二和第三组件的箭头，只有当currentStep >= 2时显示 */}
            {i === 1 && currentStep >= 2 && (
                <div className="flex items-center justify-center ml-2">
                <ArrowRight className="text-purple-500 w-6 h-6" />
                </div>
            )}
            </div>
          ))}
        </section>

        {/* 光束连线 */}
        <AnimatedBeam
          containerRef={containerRef}
          fromRef={fromRef}
          toRef={toRef}
          pathWidth={2}
          gradientStartColor="#00f0ff"
          gradientStopColor="#a000ff"
        />

        {/* 信息展示区域 */}
        <div className="flex flex-col items-center justify-center space-y-6 z-10 relative -mt-12">
          <h2 className="text-2xl font-semibold text-white">正在分析任务...</h2>
          <div className="bg-gray-800 p-4 rounded-xl text-white w-full max-w-md">
            <p><strong>任务名称:</strong> {taskName}</p>
            <p><strong>固件型号:</strong> {model}</p>
            <p><strong>上传文件:</strong> {file ? file.name : "未选择文件"}</p>
          </div>

          <p className="text-gray-400 mt-4">请稍候，系统正在处理您的任务。</p>
          <div className="text-sm text-gray-400 mt-4 whitespace-pre-wrap">{displayedMessage}</div>
          <Spinner className="text-purple-600 h-12 w-12 animate-spin" />
          <p className="text-sm text-gray-400 mt-4">分析过程可能需要几分钟，请耐心等待。</p>
        </div>
      </div>
    </>
  );
}
