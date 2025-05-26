"use client";

import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Bot, Menu, User } from "lucide-react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";

export default function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  // 点击外部关闭下拉菜单
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setMenuOpen(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="relative flex items-center justify-between px-6 py-4 backdrop-blur-sm border-b border-white/10 z-50"
    >
      {/* 左侧 LOGO */}
      <Link href="/" className="flex items-center space-x-2">
        <Bot className="w-8 h-8 text-purple-600" />
        <span className="text-white font-medium text-xl">FALCON</span>
      </Link>

      {/* 中间导航 */}
      <div className="hidden md:flex items-center space-x-8 absolute left-1/2 transform -translate-x-1/2">
        <NavLink href="/">Home</NavLink>
        <NavLink href="/how-it-works">How it Works</NavLink>
        <NavLink href="/report">Report</NavLink>
      </div>

      {/* 右侧下拉菜单 */}
      <div className="flex items-center space-x-4 relative" ref={menuRef}>
        {/* 小人图标按钮 */}
        <button
          onClick={() => setMenuOpen(!menuOpen)}
          className="text-white hover:text-purple-400 transition relative z-20"
        >
          <User className="w-7 h-7" />
        </button>

        {/* 下拉菜单内容 */}
        <AnimatePresence>
          {menuOpen && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
              className="absolute top-14 right-4 w-52 z-40
  rounded-xl shadow-2xl backdrop-blur-lg bg-black/60 border border-purple-400/30
  ring-1 ring-white/10 overflow-hidden"
            >
              <Link
                href="/profile"
                className="block px-5 py-3 text-sm text-white hover:bg-white/10 hover:text-purple-300 transition"
              >
                👤 个人资料
              </Link>
              <button
                onClick={() => {
                  localStorage.removeItem("authToken");
                  window.location.href = "/login";
                }}
                className="w-full text-left px-5 py-3 text-sm text-white hover:bg-white/10 hover:text-pink-400 transition"
              >
                🚪 退出登录
              </button>
            </motion.div>
          )}
        </AnimatePresence>

        {/* 移动端菜单按钮 */}
        <Button variant="ghost" size="icon" className="md:hidden text-white">
          <Menu className="w-6 h-6" />
        </Button>
      </div>
    </motion.nav>
  );
}

// 导航链接样式组件
function NavLink({ href, children }: { href: string; children: React.ReactNode }) {
  return (
    <Link
      href={href}
      className="text-gray-300 hover:text-white transition-colors relative group"
    >
      {children}
      <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-purple-500 transition-all group-hover:w-full" />
    </Link>
  );
}
