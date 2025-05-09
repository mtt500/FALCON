import { useEffect, useState } from "react";
import { Spinner } from "@/components/ui/spinner";
// import { useRouter } from "next/router";
// import { motion } from "framer-motion";  // Ensure that motion is imported

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
  const [displayedMessage, setDisplayedMessage] = useState(""); // 用于存储逐字打印的 message1
  const [messageIndex, setMessageIndex] = useState(0); // 控制打印进度
  // const [transformStyle, setTransformStyle] = useState(""); // 动态的 transform 样式
  
  // const router = useRouter();  // Directly use useRouter here

  useEffect(() => {
    if (messageIndex < message1.length) {
      const interval = setInterval(() => {
        setDisplayedMessage((prev) => prev + message1[messageIndex]);
        setMessageIndex((prev) => prev + 1);
      }, 5); // 控制打印速度

      return () => clearInterval(interval); // 清理定时器
    } else if (messageIndex === message1.length) {
      setTimeout(() => {
        // 当 message1 打印完成后，直接跳转到 /report 页面
        window.location.href = "/report"; // 直接跳转
      }, 1000); // 延迟1秒后跳转
    }
  }, [messageIndex, message1]);

  return (
    <div className="flex flex-col items-center justify-center space-y-6">
      <h2 className="text-2xl font-semibold text-white">正在分析任务...</h2>

      {/* 显示任务信息 */}
      <div className="bg-gray-800 p-4 rounded-xl text-white w-full max-w-md">
        <p>
          <strong>任务名称:</strong> {taskName}
        </p>
        <p>
          <strong>固件型号:</strong> {model}
        </p>
        <p>
          <strong>上传文件:</strong> {file ? file.name : "未选择文件"}
        </p>
      </div>

      <p className="text-gray-400 mt-4">请稍候，系统正在处理您的任务。</p>

      {/* 显示逐字打印的 message1 */}
      <div className="text-sm text-gray-400 mt-4">{displayedMessage}</div>

      {/* 动画：旋转进度圈 */}
      <Spinner className="text-purple-600 h-12 w-12 animate-spin" />

      <p className="text-sm text-gray-400 mt-4">分析过程可能需要几分钟，请耐心等待。</p>

      {/* 动态的 transform 样式 */}
      {/* <motion.div style={{ transform: transformStyle }} className="absolute"> */}
        {/* 你需要的动态内容 */}
      {/* </motion.div> */}
    </div>
  );
}
