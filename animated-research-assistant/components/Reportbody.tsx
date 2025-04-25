"use client"

import { PieChart, Pie, Cell, Tooltip, BarChart, Bar, XAxis, YAxis, ResponsiveContainer } from "recharts"
import { Badge } from "@/components/ui/badge"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Button } from "@/components/ui/button"
import { useState } from "react"
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select"

const COLORS = ["#ef4444", "#f59e0b", "#3b82f6"]

const firmwareOptions = [
  {
    name: "firmware_v1.3.bin",
    time: "2025-04-23 12:30",
    severityData: [
      { name: "高危", value: 3 },
      { name: "中危", value: 5 },
      { name: "低危", value: 8 },
    ],
    moduleData: [
      { name: "网络模块", count: 4 },
      { name: "文件系统", count: 3 },
      { name: "内核逻辑", count: 5 },
      { name: "驱动程序", count: 2 },
    ],
    vulnerabilities: [
      {
        id: 1,
        file: "/net/conn.c",
        line: 103,
        type: "缓冲区溢出",
        severity: "高危",
        module: "网络模块",
        description: "未检查的内存写入，可能导致执行任意代码。",
        suggestion: "加入边界检查或使用安全内存函数。",
      },
      {
        id: 2,
        file: "/fs/mount.c",
        line: 88,
        type: "空指针解引用",
        severity: "中危",
        module: "文件系统",
        description: "未检查指针是否为 NULL。",
        suggestion: "添加空指针校验逻辑。",
      },
      {
        id: 3,
        file: "/kernel/core.c",
        line: 47,
        type: "未初始化变量",
        severity: "低危",
        module: "内核逻辑",
        description: "局部变量在使用前未初始化。",
        suggestion: "为变量设置初始值。",
      },
    ],
  },
  {
    name: "firmware_v2.0.img",
    time: "2025-04-22 10:45",
    severityData: [
      { name: "高危", value: 1 },
      { name: "中危", value: 2 },
      { name: "低危", value: 6 },
    ],
    moduleData: [
      { name: "内核逻辑", count: 2 },
      { name: "文件系统", count: 4 },
      { name: "驱动程序", count: 3 },
    ],
    vulnerabilities: [
      {
        id: 1,
        file: "/fs/log.c",
        line: 42,
        type: "格式化字符串",
        severity: "中危",
        module: "文件系统",
        description: "使用用户可控格式字符串调用 printf。",
        suggestion: "改用安全格式输出函数。",
      },
      {
        id: 2,
        file: "/driver/io.c",
        line: 64,
        type: "空指针解引用",
        severity: "低危",
        module: "驱动程序",
        description: "驱动中缺少空指针判断。",
        suggestion: "添加 NULL 检查。",
      },
    ],
  },
]

export default function Report() {
  const [selectedFirmware, setSelectedFirmware] = useState(firmwareOptions[0])
  const [filteredModule, setFilteredModule] = useState<string | null>(null)
  const vulnerabilities = filteredModule
    ? selectedFirmware.vulnerabilities.filter((v) => v.module === filteredModule)
    : selectedFirmware.vulnerabilities



  return (
    <div className="min-h-screen text-white px-6 py-10">
      <div className="max-w-7xl mx-auto" id="report-container">
        {/* 固件选择器 + 报告头部 */}
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-4xl font-bold mb-2">漏洞检测报告</h1>
            <Select onValueChange={(val) => {
              const firmware = firmwareOptions.find(f => f.name === val)
              if (firmware) {
                setSelectedFirmware(firmware)
                setFilteredModule(null)
              }
            }}>
              <SelectTrigger className="w-64 bg-gray-900 border border-gray-700">
                <SelectValue placeholder="firmware_v1.3.bin" />
              </SelectTrigger>
              <SelectContent>
                {firmwareOptions.map(f => (
                  <SelectItem key={f.name} value={f.name}>{f.name}</SelectItem>
                ))}
              </SelectContent>
            </Select>
            <p className="text-sm text-gray-500 mt-1">检测时间：{selectedFirmware.time}</p>
          </div>
          <Button >导出报告 PDF</Button>
        </div>

        {/* 图表区域 */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-10 mb-12">
          {/* 饼图 */}
          <div className="bg-gray-900/60 rounded-lg p-6 border border-gray-800 shadow-md">
            <h2 className="text-lg font-semibold mb-4">按漏洞等级统计</h2>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={selectedFirmware.severityData}
                  dataKey="value"
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  label
                >
                  {selectedFirmware.severityData.map((entry, index) => (
                    <Cell key={index} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>

          {/* 柱状图 */}
          <div className="bg-gray-900/60 rounded-lg p-6 border border-gray-800 shadow-md">
            <h2 className="text-lg font-semibold mb-4">按模块分布（点击过滤）</h2>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={selectedFirmware.moduleData} onClick={(data) => {
                const activeLabel = data?.activeLabel as string
                setFilteredModule(activeLabel === filteredModule ? null : activeLabel)
              }}>
                <XAxis dataKey="name" stroke="#ccc" />
                <YAxis />
                <Bar dataKey="count" fill="#a855f7" barSize={30} />
                <Tooltip />
              </BarChart>
            </ResponsiveContainer>
            {filteredModule && (
              <p className="text-sm text-purple-400 mt-2">当前筛选模块：{filteredModule}</p>
            )}
          </div>
        </div>

        {/* 漏洞详情表格 */}
        <div className="bg-gray-900/60 rounded-lg p-6 border border-gray-800 shadow-md">
          <h2 className="text-lg font-semibold mb-4">漏洞详情</h2>
          <Table>
            <TableHeader>
              <TableRow className="border-gray-800">
                <TableHead>ID</TableHead>
                <TableHead>文件路径</TableHead>
                <TableHead>行号</TableHead>
                <TableHead>类型</TableHead>
                <TableHead>等级</TableHead>
                <TableHead>描述</TableHead>
                <TableHead>建议</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {vulnerabilities.map((vuln) => (
                <TableRow key={vuln.id} className="border-gray-800 hover:bg-gray-800/50">
                  <TableCell>{vuln.id}</TableCell>
                  <TableCell>{vuln.file}</TableCell>
                  <TableCell>{vuln.line}</TableCell>
                  <TableCell>{vuln.type}</TableCell>
                  <TableCell>
                    <Badge variant={vuln.severity === "高危" ? "destructive" : "secondary"}>{vuln.severity}</Badge>
                  </TableCell>
                  <TableCell className="text-sm text-gray-300">{vuln.description}</TableCell>
                  <TableCell className="text-sm text-gray-400">{vuln.suggestion}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </div>
    </div>
  )
}
