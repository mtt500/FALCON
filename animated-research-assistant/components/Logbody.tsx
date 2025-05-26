'use client';

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import Link from "next/link";
import { Bot } from "lucide-react";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();

  const handleLogin = async () => {
    const res = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    if (res.ok) {
      const { token } = await res.json();
      localStorage.setItem("authToken", token);
      router.push("/dashboard");
    } else {
      alert("登录失败！");
    }
  };

  return (
    <div className="relative min-h-screen flex items-center justify-center bg-black overflow-hidden">
      {/* ✨ 背景效果 */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-900 via-black to-black opacity-60 z-0" />
      <div className="absolute w-[1000px] h-[1000px] bg-purple-700 rounded-full blur-3xl opacity-20 -top-1/2 left-1/2 transform -translate-x-1/2 z-0" />

      {/* 🚀 顶部中央 Logo + 动效 */}
      <Link href="/" className="absolute top-8 left-1/2 transform -translate-x-1/2 z-10">
        <motion.div
          animate={{
            scale: [1, 1.05, 1],
            textShadow: [
              "0 0 4px #a855f7",
              "0 0 12px #a855f7",
              "0 0 4px #a855f7",
            ],
          }}
          transition={{ duration: 3, repeat: Infinity }}
          className="flex items-center space-x-3"
        >
          <Bot className="w-10 h-10 text-purple-400 drop-shadow-xl" />
          <span className="text-white text-3xl font-bold tracking-widest drop-shadow-md">
            FALCON
          </span>
        </motion.div>
      </Link>

      {/* 🔐 登录框主内容 */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="relative z-10 bg-white/5 backdrop-blur-lg border border-purple-800/30 rounded-2xl p-10 shadow-2xl w-[90%] max-w-md"
      >
        <h2 className="text-3xl font-bold text-center text-purple-300 mb-8">欢迎回来</h2>

        <input
          type="text"
          placeholder="用户名"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full p-3 mb-5 rounded-xl bg-white/10 border border-purple-500/20 placeholder-purple-300 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
        />
        <input
          type="password"
          placeholder="密码"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full p-3 mb-6 rounded-xl bg-white/10 border border-purple-500/20 placeholder-purple-300 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
        />

        <motion.button
          whileTap={{ scale: 0.95 }}
          whileHover={{ scale: 1.03 }}
          onClick={handleLogin}
          className="w-full py-3 rounded-xl bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold hover:from-pink-600 hover:to-purple-600 transition"
        >
          登录
        </motion.button>
      </motion.div>
    </div>
  );
}
