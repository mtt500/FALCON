import unittest
from src.agents.code_parsing_agent import CodeParsingAgent

class TestAgentLLM(unittest.TestCase):
    def setUp(self):
        """测试前的准备工作"""
        self.agent = CodeParsingAgent()

    def test_agent_response(self):
        """测试 Agent 的基本响应能力"""
        # 测试一个简单的指令
        test_query = "请解释一下二进制文件分析的基本步骤"
        
        # 使用 agent 的 query 方法
        response = self.agent.agent.query(test_query)
        
        # 验证响应
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.response)
        self.assertGreater(len(response.response), 0)
        
        # 打印响应内容，方便查看
        print("\nAgent 响应内容:")
        print(response.response)

    def test_agent_tool_usage(self):
        """测试 Agent 是否能正确使用工具"""
        # 测试一个需要工具支持的指令
        test_query = """
        请列出你可以使用的所有工具，并解释每个工具的用途。
        """
        
        response = self.agent.agent.query(test_query)
        
        # 验证响应
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.response)
        
        # 检查响应中是否包含工具相关的信息
        self.assertIn("analyze_binary", response.response)
        self.assertIn("decompile_binary", response.response)
        
        # 打印响应内容，方便查看
        print("\nAgent 工具使用说明:")
        print(response.response)

if __name__ == '__main__':
    unittest.main() 