from capstone import *
from capstone.x86 import *
from typing import Dict, Any, List
import struct
import os
import pefile
import logging

class Decompiler:
    def __init__(self):
        # 初始化 logger
        self.logger = logging.getLogger(__name__)
        
        # 初始化 Capstone
        self.cs_x86 = Cs(CS_ARCH_X86, CS_MODE_32)
        self.cs_x86_64 = Cs(CS_ARCH_X86, CS_MODE_64)
        
        # 启用详细模式
        for cs in [self.cs_x86, self.cs_x86_64]:
            cs.detail = True

    def decompile(self, binary_path: str) -> Dict[str, Any]:
        """反编译二进制文件"""
        try:
            # 获取代码段
            code_section = self._get_code_section(binary_path)
            if not code_section:
                raise Exception("未找到代码段")

            # 反汇编
            disassembly = self._disassemble(code_section['data'], code_section['address'])
            
            # 生成伪代码
            pseudocode = self._generate_pseudocode(disassembly)
            
            return {
                "disassembly": disassembly,
                "pseudocode": pseudocode
            }
            
        except Exception as e:
            raise Exception(f"反编译失败: {str(e)}")

    def _get_code_section(self, binary_path: str) -> Dict[str, Any]:
        try:
            self.logger.debug(f"开始分析文件: {binary_path}")
            
            pe = pefile.PE(binary_path)
            
            # 查找 .text 段
            for section in pe.sections:
                if section.Name.decode().strip('\x00') == '.text':
                    self.logger.debug(f"找到 .text 段，地址: {hex(section.VirtualAddress)}")
                    return {
                        'data': section.get_data(),
                        'address': section.VirtualAddress
                    }
            
            self.logger.error("未找到 .text 段")
            return None
            
        except Exception as e:
            self.logger.error(f"提取代码段时出错: {str(e)}")
            return None

    def _get_elf_code_section(self, f) -> Dict[str, Any]:
        """获取 ELF 文件的代码段"""
        # 读取 ELF 头
        f.seek(0)
        elf_header = f.read(52)
        
        # 获取段表偏移和大小
        sh_offset = struct.unpack('I', elf_header[32:36])[0]
        sh_size = struct.unpack('H', elf_header[46:48])[0]
        sh_num = struct.unpack('H', elf_header[48:50])[0]
        
        # 遍历段表
        for i in range(sh_num):
            f.seek(sh_offset + i * sh_size)
            section = f.read(sh_size)
            
            # 检查是否是代码段
            if section[4] == 1:  # SHT_PROGBITS
                flags = struct.unpack('I', section[8:12])[0]
                if flags & 0x4:  # SHF_EXECINSTR
                    offset = struct.unpack('I', section[16:20])[0]
                    size = struct.unpack('I', section[20:24])[0]
                    addr = struct.unpack('I', section[12:16])[0]
                    
                    f.seek(offset)
                    data = f.read(size)
                    
                    return {
                        "address": addr,
                        "data": data,
                        "size": size
                    }
        
        return None

    def _get_pe_code_section(self, f) -> Dict[str, Any]:
        """获取 PE 文件的代码段"""
        try:
            # 读取 PE 头
            f.seek(0x3c)
            pe_offset = struct.unpack('I', f.read(4))[0]
            f.seek(pe_offset + 24)
            num_sections = struct.unpack('H', f.read(2))[0]

            # 遍历节表
            for i in range(num_sections):
                f.seek(pe_offset + 24 + 20 + i * 40)
                section = f.read(40)

                # 检查是否是代码段
                name = section[0:8].strip(b'\x00')
                if name == b'.text':
                    virtual_address = struct.unpack('I', section[12:16])[0]
                    raw_size = struct.unpack('I', section[16:20])[0]
                    raw_ptr = struct.unpack('I', section[20:24])[0]

                    # 读取代码段数据
                    f.seek(raw_ptr)
                    data = f.read(raw_size)

                    return {
                        "address": virtual_address,
                        "data": data
                    }
        except Exception as e:
            print(f"获取代码段时出错: {str(e)}")
            return None

    def _disassemble(self, code: bytes, start_address: int) -> List[Dict[str, Any]]:
        """反汇编代码"""
        instructions = []
        
        # 选择正确的 Capstone 实例
        cs = self.cs_x86_64 if len(code) > 0x1000 else self.cs_x86
        
        for i in cs.disasm(code, start_address):
            instructions.append({
                "address": hex(i.address),
                "mnemonic": i.mnemonic,
                "operands": i.op_str,
                "bytes": i.bytes.hex()
            })
        
        return instructions

    def _generate_pseudocode(self, disassembly: List[Dict[str, Any]]) -> str:
        """生成伪代码"""
        pseudocode = []
        current_function = None
        stack_vars = {}
        stack_offset = 0
        
        for instr in disassembly:
            # 检测函数开始
            if instr['mnemonic'] == 'push' and instr['operands'] == 'rbp':
                current_function = f"func_{instr['address']}"
                pseudocode.append(f"\nvoid {current_function}() {{")
                continue
            
            # 检测函数结束
            if instr['mnemonic'] == 'ret':
                if current_function:  # 只在有当前函数时才添加结束大括号
                    pseudocode.append("}")
                    current_function = None
                    stack_vars.clear()
                    stack_offset = 0
                continue
            
            # 转换指令为伪代码
            if current_function:
                # 避免重复的指令
                pseudocode_line = self._instruction_to_pseudocode(instr, stack_vars, stack_offset)
                if pseudocode_line not in pseudocode:  # 避免重复行
                    pseudocode.append(pseudocode_line)
        
        return "\n".join(pseudocode)

    def _instruction_to_pseudocode(self, instr: Dict[str, Any], stack_vars: Dict[str, str], stack_offset: int) -> str:
        """将汇编指令转换为伪代码"""
        mnemonic = instr['mnemonic']
        operands = instr['operands']
        
        # 基本指令转换
        if mnemonic == 'mov':
            dest, src = operands.split(',')
            return f"    {dest.strip()} = {src.strip()};"
        elif mnemonic == 'add':
            dest, src = operands.split(',')
            return f"    {dest.strip()} += {src.strip()};"
        elif mnemonic == 'sub':
            dest, src = operands.split(',')
            return f"    {dest.strip()} -= {src.strip()};"
        elif mnemonic == 'push':
            stack_vars[f"var_{stack_offset}"] = operands
            stack_offset += 8
            return f"    // 保存 {operands} 到栈"
        elif mnemonic == 'pop':
            stack_offset -= 8
            return f"    // 从栈恢复 {operands}"
        elif mnemonic == 'call':
            return f"    {operands}();"
        elif mnemonic == 'jmp':
            return f"    goto {operands};"
        elif mnemonic == 'je':
            return f"    if (ZF) goto {operands};"
        elif mnemonic == 'jne':
            return f"    if (!ZF) goto {operands};"
        elif mnemonic == 'cmp':
            dest, src = operands.split(',')
            return f"    // 比较 {dest.strip()} 和 {src.strip()}"
        else:
            return f"    // {mnemonic} {operands}"