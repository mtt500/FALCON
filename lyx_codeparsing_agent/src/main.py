from src.agents.code_parsing_agent import CodeAnalysisAgent
from src.services.llm_service import LLMService
from src.utils.logger import setup_logger
from config.settings import Settings

def main():
    # 设置日志
    logger = setup_logger()
    
    # 初始化服务
    llm_service = LLMService()
    
    # 创建Agent
    agent = CodeAnalysisAgent(llm_service)
    
    # 分析固件
    binary_path = "path/to/firmware.bin"
    result = agent.analyze_binary(binary_path)
    
    # 输出结果
    logger.info("Analysis completed")
    return result

if __name__ == "__main__":
    main()
