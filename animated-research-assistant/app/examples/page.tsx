"use client"

import React, { useState } from "react"
import {
  Search,
  Filter,
  Plus,
  Edit,
  Trash2,
  MoreHorizontal,
  Flag,
  Download,
  ChevronLeft,
  ChevronRight,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Checkbox } from "@/components/ui/checkbox"
import Link from "next/link"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import {SparklesCore} from "@/components/sparkles";

export default function VulnerabilityDashboard() {
  const [selectedProject, setSelectedProject] = useState("pentest_vulnweb")
const [vulnerabilities, setVulnerabilities] = useState([
  {
    id: 1,
    task: "firmware1",
    severity: "high",
    firmware: "firmware_v1.3",
    classification: "ICS",
    website: "http://localhost:3000/Report",
    path: "report1.pdf",
  },
  {
    id: 2,
    task: "firmware2",
    severity: "high",
    firmware: "firmware_v2.0",
    classification: "ADT",
    website: "http://localhost:3000/Report",
    path: "report2.pdf",
  },
])
const [selectedIds, setSelectedIds] = useState<number[]>([])
const [showConfirm, setShowConfirm] = useState(false)


  return (
    <div className="flex flex-col min-h-screen bg-black relative overflow-hidden">
      {/* Stars background */}
      <div className="absolute inset-0 z-0">
        <StarBackground />
      </div>

       <div className="h-full w-full absolute inset-0 z-0">
        <SparklesCore
          id="tsparticlesfullpage"
          background="transparent"
          minSize={0.6}
          maxSize={1.4}
          particleDensity={100}
          className="w-full h-full"
          particleColor="#FFFFFF"
        />
      </div>

      {/* Header */}
      <header className="relative z-10 border-b border-gray-800 bg-black/50 backdrop-blur-sm">
        <div className="container flex h-16 items-center px-4">
          <div className="flex items-center gap-2 text-purple-500 font-bold text-xl">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="lucide lucide-bot"
            >
              <path d="M12 8V4H8" />
              <rect width="16" height="12" x="4" y="8" rx="2" />
              <path d="M2 14h2" />
              <path d="M20 14h2" />
              <path d="M15 13v2" />
              <path d="M9 13v2" />
            </svg>
            FALCON
          </div>
            <nav className="ml-auto flex items-center space-x-4">
             <div className="hidden md:flex items-center space-x-8 absolute left-1/2 transform -translate-x-1/2">
              <NavLink href="/">Home</NavLink>
              <NavLink href="/how-it-works">How it Works</NavLink>
               <NavLink href="/examples">Examples</NavLink>
              <NavLink href="/report">Report</NavLink>
              </div>
            </nav>
        </div>
      </header>

      {/* Main content */}
      <main className="flex-1 relative z-10">
        <div className="container py-6 w-full max-w-screen-xl mx-auto pt-6">
          {/* Project selector and search */}
          <div className="flex items-center space-x-4 mb-6">
            <div className="w-64">
              <Select value={selectedProject} onValueChange={setSelectedProject}>
                <SelectTrigger className="bg-gray-900 border-gray-700">
                  <SelectValue placeholder="Select project" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="pentest_vulnweb">pentest_vulnweb</SelectItem>
                  <SelectItem value="security_audit">security_audit</SelectItem>
                  <SelectItem value="internal_scan">internal_scan</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="flex-1 flex items-center space-x-2">
              <div className="relative flex-1">
                <Input type="search" placeholder="Search vulns" className="bg-gray-900 border-gray-700 pl-10" />
                <Search className="absolute left-3 top-2.5 h-4 w-4 text-gray-500" />
              </div>
              <Button variant="outline" className="bg-gray-900 border-gray-700 text-gray-300">
                <Search className="h-4 w-4 mr-2" />
                Advanced search
              </Button>
              <Button variant="outline" className="bg-gray-900 border-gray-700 text-gray-300">
                Save Filter
              </Button>
            </div>
          </div>

          {/* Action buttons */}
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-2">
              <Button variant="ghost" size="icon" className="text-gray-400">
                <Edit className="h-4 w-4" />
              </Button>
              <Button variant="ghost" size="icon" className="text-gray-400">
                <Flag className="h-4 w-4" />
              </Button>
              <Button
                  variant="ghost"
                  size="icon"
                  className="text-gray-400 hover:text-gray-400"
                  onClick={() => {
                    setVulnerabilities(vulnerabilities.filter(v => !selectedIds.includes(v.id)))
                    setSelectedIds([])
                  }}
                >
                <Trash2 className="h-4 w-4" />
              </Button>

              <Button variant="ghost" size="icon" className="text-gray-400">
                <MoreHorizontal className="h-4 w-4" />
              </Button>
            </div>
          </div>

          {/* Table */}
          <div className="bg-gray-900/60 backdrop-blur-sm rounded-md border border-gray-800 overflow-hidden w-full max-w-screen-xl mx-auto pt-6">
            <Table>
              <TableHeader>
                <TableRow className="border-gray-800 hover:bg-gray-800/50">
                  <TableHead className="w-12">
                    <Checkbox />
                  </TableHead>
                  <TableHead className="w-12"></TableHead>
                  <TableHead className="w-12"></TableHead>
                  <TableHead>TASK</TableHead>
                  <TableHead>TOOL</TableHead>
                  <TableHead>STATUS</TableHead>
                  <TableHead>REPORT</TableHead>
                  <TableHead>PATH</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {vulnerabilities.map((vuln) => (
                  <TableRow key={vuln.id} className="border-gray-800 hover:bg-gray-800/50">
                   <TableCell>
                    <Checkbox
                      checked={selectedIds.includes(vuln.id)}
                      onCheckedChange={(checked) => {
                        setSelectedIds((prev) =>
                          checked ? [...prev, vuln.id] : prev.filter((id) => id !== vuln.id)
                        )
                      }}
                    />
                  </TableCell>

                    <TableCell>
                      <Badge
                        variant={vuln.severity === "high" ? "destructive" : "secondary"}
                        className="h-6 w-6 flex items-center justify-center p-0 rounded-sm"
                      >
                        {vuln.severity === "high" ? "H" : "L"}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <Flag className="h-4 w-4 text-amber-500" />
                    </TableCell>
                    <TableCell className="font-medium text-gray-200">{vuln.task}</TableCell>
                    <TableCell>{vuln.firmware}</TableCell>
                    <TableCell>
                      <span className={vuln.classification === "ICS" ? "text-purple-500" : "text-green-500"}>
                        {vuln.classification}
                      </span>
                    </TableCell>
                    <TableCell className="text-gray-400">{vuln.website}</TableCell>
                    <TableCell className="text-gray-400">{vuln.path}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </div>
      </main>
    </div>
  )
}

function StarBackground() {
  return (
    <div className="absolute inset-0">
      {Array.from({ length: 100 }).map((_, i) => {
        const size = Math.random() * 2
        const top = Math.random() * 100
        const left = Math.random() * 100
        const opacity = Math.random() * 0.7 + 0.3

        return (
          <div
            key={i}
            className="absolute rounded-full bg-white"
            style={{
              width: `${size}px`,
              height: `${size}px`,
              top: `${top}%`,
              left: `${left}%`,
              opacity,
            }}
          />
        )
      })}
    </div>
  )
}
function NavLink({ href, children }: { href: string; children: React.ReactNode }) {
  return (
    <Link href={href} className="text-gray-300 hover:text-white transition-colors relative group">
      {children}
      <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-purple-500 transition-all group-hover:w-full" />
    </Link>
  )
}
