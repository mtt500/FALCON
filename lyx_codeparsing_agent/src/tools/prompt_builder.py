from typing import Dict, Any, List

class PromptBuilder:
    @staticmethod
    def create_decompile_prompt(function: Dict[str, Any]) -> str:
        """
        创建用于反编译的LLM提示词
        """
        return f"""
        请将以下汇编代码转换为C代码。要求：
        1. 保持函数的功能逻辑
        2. 使用有意义的变量名
        3. 添加必要的注释说明
        4. 正确处理控制流结构
        5. 处理内存操作和指针
        
        函数信息：
        - 名称: {function.get('name', 'unknown')}
        - 地址: {function.get('offset', 'unknown')}
        - 大小: {function.get('size', 'unknown')} bytes
        
        汇编代码：
        {function.get('instructions', '')}
        
        请提供：
        1. 完整的C代码实现
        2. 关键逻辑的注释说明
        3. 重要的数据结构定义（如果需要）
        """

    @staticmethod
    def create_analysis_prompt(functions: List[Dict[str, Any]]) -> str:
        """
        创建用于整体分析的LLM提示词
        """
        # 构建函数信息字符串
        func_info = "\n".join([
            f"函数: {func.get('name', 'unknown')}\n"
            f"地址: {func.get('offset', 'unknown')}\n"
            f"大小: {func.get('size', 'unknown')} bytes\n"
            f"指令:\n" + "\n".join([
                f"  {inst.get('mnemonic', '')} {inst.get('op_str', '')}"
                for inst in func.get('instructions', [])
            ])
            for func in functions
        ])

        return f"""
        请分析以下二进制文件的具体内容：
        
        {func_info}
        
        请提供：
        1. 每个函数的具体功能（基于指令分析）
        2. 函数之间的调用关系
        3. 关键算法或逻辑
        4. 潜在的安全问题
        5. 改进建议
        
        注意：请基于实际的指令分析，而不是提供通用建议。
        """