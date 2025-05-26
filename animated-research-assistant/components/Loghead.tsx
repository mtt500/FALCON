"use client";

import { Button } from "@/components/ui/button";
import { Bot, Menu } from "lucide-react";
import { motion } from "framer-motion";
import Link from "next/link";
import type React from "react";

export default function Navbar() {
  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
      className="relative flex items-center justify-between px-6 py-4
        bg-gradient-to-br from-purple-900/50 via-black/30 to-black/50
        backdrop-blur-md border-b border-purple-800/30
        shadow-md z-50"
    >
      {/* Logo & Brand */}
      <Link href="/" className="flex items-center space-x-2">
        <Bot className="w-8 h-8 text-purple-400" />
        <span className="text-white font-medium text-xl tracking-wide">FALCON</span>
      </Link>

      {/* Mobile Button */}
      <Button variant="ghost" size="icon" className="md:hidden text-white hover:bg-white/10">
        <Menu className="w-6 h-6" />
      </Button>
    </motion.nav>
  );
}

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
