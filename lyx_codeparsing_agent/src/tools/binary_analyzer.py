import magic
from capstone import *
from capstone.x86 import *
from capstone.arm import *
from capstone.arm64 import *
from typing import Dict, Any
import struct
import os
import logging
import pefile

class BinaryAnalyzer:
    def __init__(self):
        # 初始化 Capstone
        self.cs_x86 = Cs(CS_ARCH_X86, CS_MODE_32)
        self.cs_x86_64 = Cs(CS_ARCH_X86, CS_MODE_64)
        self.cs_arm = Cs(CS_ARCH_ARM, CS_MODE_ARM)
        self.cs_arm64 = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
        
        # 启用详细模式
        for cs in [self.cs_x86, self.cs_x86_64, self.cs_arm, self.cs_arm64]:
            cs.detail = True

        self.logger = logging.getLogger(__name__)

    def analyze(self, binary_path: str) -> Dict[str, Any]:
        self.logger.debug(f"开始分析文件: {binary_path}")
        
        try:
            # 检查文件是否存在
            if not os.path.exists(binary_path):
                self.logger.error(f"文件不存在: {binary_path}")
                raise FileNotFoundError(f"文件不存在: {binary_path}")
            
            # 获取文件类型
            file_type = self._get_file_type(binary_path)
            self.logger.debug(f"检测到的文件类型: {file_type}")
            
            # 如果是 PE 文件，返回 PE32
            if "dosexec" in file_type.lower():
                file_type = "PE32"
            
            return {
                "file_info": {
                    "type": file_type
                },
                "architecture": self._get_architecture(binary_path),
                "sections": self._get_sections(binary_path),
                "entry_point": self._get_entry_point(binary_path)
            }
            
        except Exception as e:
            self.logger.error(f"分析过程中出错: {str(e)}")
            raise

    def _get_file_info(self, binary_path: str) -> Dict[str, Any]:
        """获取文件基本信息"""
        try:
            mime = magic.Magic(mime=True)
            file_type = mime.from_file(binary_path)
            return {"type": file_type}
        except Exception as e:
            # 如果 magic 库失败，尝试直接读取文件头
            with open(binary_path, 'rb') as f:
                header = f.read(16)
                if header.startswith(b'MZ'):
                    return {"type": "PE32"}
                elif header.startswith(b'\x7fELF'):
                    return {"type": "ELF"}
                return {"type": "unknown"}

    def _get_architecture_info(self, binary_path: str) -> Dict[str, Any]:
        """获取架构信息"""
        with open(binary_path, 'rb') as f:
            header = f.read(16)
            
            if header.startswith(b'MZ'):
                # PE 文件
                f.seek(0x3c)
                pe_offset = struct.unpack('I', f.read(4))[0]
                f.seek(pe_offset + 4)
                machine = struct.unpack('H', f.read(2))[0]
                if machine == 0x014c:
                    return {"architecture": "x86"}
                elif machine == 0x8664:
                    return {"architecture": "x86_64"}
            return {"architecture": "unknown"}

    def _get_section_info(self, binary_path: str) -> Dict[str, Any]:
        """获取段信息"""
        with open(binary_path, 'rb') as f:
            header = f.read(16)
            
            if header.startswith(b'\x7fELF'):
                # 解析 ELF 段信息
                return self._parse_elf_sections(f)
            elif header.startswith(b'MZ'):
                # 解析 PE 段信息
                return self._parse_pe_sections(f)
            
            return {"error": "不支持的文件格式"}

    def _parse_pe_sections(self, f) -> Dict[str, Any]:
        """解析 PE 文件的段信息"""
        sections = []
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
                
                # 使用 bytes 切片而不是 decode
                name = section[0:8].strip(b'\x00')
                virtual_size = struct.unpack('I', section[8:12])[0]
                virtual_address = struct.unpack('I', section[12:16])[0]
                raw_size = struct.unpack('I', section[16:20])[0]
                raw_ptr = struct.unpack('I', section[20:24])[0]
                
                sections.append({
                    "name": name,
                    "virtual_size": virtual_size,
                    "virtual_address": virtual_address,
                    "raw_size": raw_size,
                    "raw_ptr": raw_ptr
                })
        except Exception as e:
            print(f"解析段信息时出错: {str(e)}")
            
        return {"sections": sections}

    def _get_entry_point(self, binary_path: str) -> Dict[str, Any]:
        """获取入口点"""
        with open(binary_path, 'rb') as f:
            header = f.read(16)
            
            if header.startswith(b'\x7fELF'):
                # 获取 ELF 入口点
                entry = struct.unpack('I', header[24:28])[0]
                return {"address": hex(entry)}
            elif header.startswith(b'MZ'):
                # 获取 PE 入口点
                f.seek(0x3c)
                pe_offset = struct.unpack('I', f.read(4))[0]
                f.seek(pe_offset + 40)
                entry = struct.unpack('I', f.read(4))[0]
                return {"address": hex(entry)}
            
            return {"error": "不支持的文件格式"}

    def _get_file_type(self, binary_path: str) -> str:
        self.logger.debug(f"开始识别文件类型: {binary_path}")
        
        try:
            import magic  # 确保已安装 python-magic 库
            
            # 使用 magic 库识别文件类型
            mime = magic.Magic(mime=True)
            file_type = mime.from_file(binary_path)
            self.logger.debug(f"MIME 类型: {file_type}")
            
            # 如果是 PE 文件，返回 PE32
            if "dosexec" in file_type.lower():
                return "PE32"
            
            return file_type
            
        except Exception as e:
            self.logger.error(f"文件类型识别失败: {str(e)}")
            raise

    def _get_architecture(self, binary_path: str) -> Dict[str, str]:
        """获取二进制文件的架构信息"""
        try:
            pe = pefile.PE(binary_path)
            if pe.OPTIONAL_HEADER.Magic == 0x10b:  # PE32
                return {"architecture": "x86"}
            elif pe.OPTIONAL_HEADER.Magic == 0x20b:  # PE32+
                return {"architecture": "x64"}
            return {"architecture": "unknown"}
        except Exception as e:
            self.logger.error(f"获取架构信息失败: {str(e)}")
            return {"architecture": "unknown"}

    def _get_sections(self, binary_path: str) -> Dict[str, Any]:
        """获取二进制文件的段信息"""
        try:
            pe = pefile.PE(binary_path)
            sections = []
            for section in pe.sections:
                sections.append({
                    "name": section.Name.decode().strip('\x00'),
                    "address": section.VirtualAddress,
                    "size": section.SizeOfRawData
                })
            return {"sections": sections}
        except Exception as e:
            self.logger.error(f"获取段信息失败: {str(e)}")
            return {"sections": []} 