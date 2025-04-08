import unittest
import os
import subprocess
from src.tools.binary_analyzer import BinaryAnalyzer
from src.tools.decompiler import Decompiler
import logging
import time
import win32api
import shutil
import tempfile
from src.agents.code_parsing_agent import CodeParsingAgent

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TestBinaryAnalysis(unittest.TestCase):
    def setUp(self):
        # 初始化 logger
        self.logger = logging.getLogger(__name__)
        
        # 使用临时目录而不是项目目录
        self.test_dir = tempfile.mkdtemp()
        self.test_binary = os.path.join(self.test_dir, "test_binary.exe")
        self.c_source = os.path.join(self.test_dir, "test.c")
        
        # 初始化 CodeParsingAgent
        self.agent = CodeParsingAgent()
        
        # 创建测试用的 C 程序
        self.c_code = """
        #include <stdio.h>
        
        int add(int a, int b) {
            return a + b;
        }
        
        int multiply(int a, int b) {
            return a * b;
        }
        
        int main() {
            int x = 5;
            int y = 3;
            printf("Add: %d\\n", add(x, y));
            printf("Multiply: %d\\n", multiply(x, y));
            return 0;
        }
        """
        
        # 编译测试程序
        self._compile_test_program()

    def _compile_test_program(self):
        """编译测试程序"""
        try:
            # 写入 C 源文件
            with open(self.c_source, "w", encoding='utf-8') as f:
                f.write(self.c_code)
            
            # 使用正确的 gcc 路径
            gcc_path = r"D:\vscode\MinGW\mingw64\bin\gcc.exe"
            
            # 直接使用路径，不获取短路径名
            compile_cmd = [gcc_path, "-o", self.test_binary, self.c_source]
            
            # 执行编译
            result = subprocess.run(compile_cmd, capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode != 0:
                raise Exception(f"编译失败: {result.stderr}")
            
            if not os.path.exists(self.test_binary):
                raise Exception("编译后的文件未创建")
                
        except Exception as e:
            self.fail(f"测试程序编译失败: {str(e)}")

    def test_binary_analyzer(self):
        """测试二进制分析器"""
        logger.debug("开始测试二进制分析器")
        analyzer = BinaryAnalyzer()
        
        # 测试文件路径
        test_file = self.test_binary
        logger.debug(f"测试文件路径: {test_file}")
        
        # 检查文件是否存在
        if not os.path.exists(test_file):
            logger.error(f"测试文件不存在: {test_file}")
            return
        
        # 分析文件
        result = analyzer.analyze(test_file)
        logger.debug(f"分析结果: {result}")
        
        # 验证基本信息
        self.assertIn("file_info", result)
        self.assertIn("architecture", result)
        self.assertIn("sections", result)
        self.assertIn("entry_point", result)
        
        # 验证文件类型 - 修改为检查 PE 文件
        self.assertIn("PE32", result["file_info"]["type"])
        
        # 验证架构信息
        self.assertIn(result["architecture"]["architecture"], ["x86", "x64"])
        
        # 验证段信息
        self.assertGreater(len(result["sections"]["sections"]), 0)
        
        # 验证入口点
        self.assertIsNotNone(result["entry_point"]["address"])

    def test_decompiler(self):
        """测试反编译器功能"""
        # 使用编译生成的测试文件
        test_binary = self.test_binary
        
        # 直接使用 Decompiler 工具进行反编译
        decompiler = Decompiler()
        result = decompiler.decompile(test_binary)
        
        # 打印反编译结果
        print("\n反编译结果:")
        print("反汇编:")
        for line in result['disassembly']:
            print(line)
        print("\n伪代码:")
        print(result['pseudocode'])
        
        # 验证反编译结果
        self.assertIsInstance(result, dict)
        self.assertIn('disassembly', result)
        self.assertIn('pseudocode', result)
        
        # 验证反汇编结果
        self.assertIsInstance(result['disassembly'], list)
        self.assertGreater(len(result['disassembly']), 0)
        
        # 验证伪代码结果
        self.assertIsInstance(result['pseudocode'], str)
        self.assertGreater(len(result['pseudocode']), 0)
        
        # 验证伪代码内容
        self.assertIn("void", result['pseudocode'])
        self.assertIn("{", result['pseudocode'])
        self.assertIn("}", result['pseudocode'])

    def tearDown(self):
        """清理测试文件"""
        time.sleep(1)  # 等待文件释放
        
        # 清理测试文件
        for file in [self.test_binary, self.c_source]:
            if os.path.exists(file):
                try:
                    os.remove(file)
                except PermissionError:
                    self.logger.warning(f"无法删除文件 {file}，可能仍在被使用")
        
        # 使用 shutil.rmtree 替代 os.rmdir
        if os.path.exists(self.test_dir):
            try:
                shutil.rmtree(self.test_dir)
            except Exception as e:
                self.logger.warning(f"无法删除目录 {self.test_dir}: {str(e)}")

if __name__ == "__main__":
    unittest.main() 