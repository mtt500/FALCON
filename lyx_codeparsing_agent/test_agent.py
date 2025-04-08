import unittest
from pathlib import Path
from src.agents.code_parsing_agent import CodeParsingAgent

class TestCodeParsingAgent(unittest.TestCase):
    def setUp(self):
        """测试前的准备工作"""
        # 创建测试用的二进制文件
        self.test_binary = Path("tests/data/test_binary")
        self.test_binary.parent.mkdir(parents=True, exist_ok=True)
        
        # 创建一个简单的测试二进制文件
        with open(self.test_binary, 'wb') as f:
            # 创建一个简单的 ELF 文件头
            f.write(b'\x7fELF\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        
        # 初始化 Agent
        self.agent = CodeParsingAgent()

    def test_parse_binary(self):
        """测试完整的二进制解析流程"""
        result = self.agent.parse_binary(str(self.test_binary))
        
        # 验证返回结果
        self.assertEqual(result['status'], 'success')
        self.assertIn('analysis', result)
        
        # 验证分析报告内容
        analysis = result['analysis']
        self.assertIn('architecture', analysis)
        self.assertIn('functions', analysis)
        self.assertIn('importance_ranking', analysis)
        self.assertIn('cache_info', analysis)

    def tearDown(self):
        """测试后的清理工作"""
        # 删除测试文件
        if self.test_binary.exists():
            self.test_binary.unlink()

def main():
    # 初始化 Agent
    agent = CodeParsingAgent()
    
    # 使用我们刚创建的二进制文件
    binary_path = "tests/data/test_binary"
    
    # 运行分析
    result = agent.parse_binary(binary_path)
    
    # 打印结果
    if result['status'] == 'success':
        print("\n=== 分析报告 ===")
        print(result['analysis'])
    else:
        print(f"分析失败: {result['error']}")

if __name__ == "__main__":
    main() 