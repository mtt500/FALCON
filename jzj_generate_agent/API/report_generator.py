# report_generator.py
import os
import json
import openai
import hashlib
from pathlib import Path
from datetime import datetime

# LlamaIndex相关模块
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings, StorageContext, load_index_from_storage, VectorStoreIndex
from llama_index.core.readers import SimpleDirectoryReader
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent
from llama_index.core.node_parser import SimpleNodeParser

# ========== 初始化 OpenAI 和 LlamaIndex ==========
openai.api_key = "sk-42kUEMoma40GUNhl595bE5D53e994eC59a7a469534564f11"
openai.base_url = "https://api.gptapi.us/v1"

Settings.llm = OpenAI(model="gpt-4o",
                      api_key=openai.api_key,
                      base_url=openai.base_url)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")


# ========== 工具函数 ==========
def compute_file_hash(file_path: Path) -> str:
    with open(file_path, "rb") as f:
        content = f.read()
    return hashlib.sha256(content).hexdigest()


def update_vuln_kb_index(index_dir: str, data_dir: str) -> VectorStoreIndex:
    current_files = {
        os.path.abspath(os.path.join(data_dir, f))
        for f in os.listdir(data_dir)
        if os.path.isfile(os.path.join(data_dir, f))
    }

    try:
        storage_context = StorageContext.from_defaults(persist_dir=index_dir)
        index = load_index_from_storage(storage_context)
        print("✅ 成功加载已有索引。")

        existing_file_paths = set()
        for node in storage_context.docstore.docs.values():
            file_path = node.metadata.get("file_path")
            if file_path:
                existing_file_paths.add(os.path.abspath(file_path))

        new_files = current_files - existing_file_paths
        deleted_files = existing_file_paths - current_files

        if new_files:
            new_documents = SimpleDirectoryReader(
                input_files=list(new_files)).load_data()
            new_nodes = SimpleNodeParser().get_nodes_from_documents(
                new_documents)
            index.insert_nodes(new_nodes)
            print(f"✅ 已更新文档数：{len(new_files)}")

        if deleted_files:
            delete_ids = []
            for node_id, node in storage_context.docstore.docs.items():
                file_path = node.metadata.get("file_path")
                if file_path and os.path.abspath(file_path) in deleted_files:
                    delete_ids.append(node_id)
            if delete_ids:
                index.delete_nodes(delete_ids)
                print(f"🗑️ 已删除失效节点数：{len(delete_ids)}")

    except Exception as e:
        print(f"⚠️ 索引加载失败，正在重建：{e}")
        documents = SimpleDirectoryReader(input_dir=data_dir).load_data()
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=index_dir)
        print("✅ 索引重建完成。")

    index.storage_context.persist(persist_dir=index_dir)
    return index


# ========== 创建 Agent ==========
vuln_kb_index = update_vuln_kb_index(index_dir="./storage/vuln_kb",
                                     data_dir="./data/vuln_kb")
kb_engine = vuln_kb_index.as_query_engine(similarity_top_k=3)


def query_kb(query: str) -> str:
    response = kb_engine.query(query)
    answer = response.response.strip()

    references = []
    for i, node_with_score in enumerate(response.source_nodes):
        node = node_with_score.node
        file_path = node.metadata.get("file_path", "未知文件")
        content = node.get_content().strip()
        references.append(f"【引用{i+1}】文件：`{file_path}`\n摘录内容：\n> {content}")

    full_response = f"{answer}\n\n引用内容：\n" + "\n\n".join(references)
    return full_response


kb_tool = FunctionTool.from_defaults(
    fn=query_kb,
    name="vuln_knowledge_base",
    description="提供漏洞背景知识，如原理、危害和修复建议。输入是漏洞名称，如 SQL 注入")

report_agent = ReActAgent.from_tools(tools=[kb_tool],
                                     llm=Settings.llm,
                                     verbose=True)


# ========== 对外提供的核心函数 ==========
def generate_report(decision_data: dict) -> str:
    """
    输入：决策JSON字典
    输出：Markdown格式的漏洞报告字符串
    """
    input_desc = "下面是漏洞检测器输出的结果 JSON：\n"
    input_desc += json.dumps(decision_data, ensure_ascii=False, indent=2)
    input_desc += "\n\n请分析这个 JSON，并按如下格式生成markdown报告：\n"
    input_desc += """
### 漏洞函数名：`<function_name>`
- **漏洞位置**：<location>
- **风险等级**：<severity>
- **漏洞类型**：<vulnerability_type>
- **漏洞描述**：
  <中文的description>
- **修复建议**：
  <建议的修复方法>
---
"""
    input_desc += "\n请务必在每条漏洞报告中写出你引用的文件路径及内容片段，用如下格式：\n"
    input_desc += "来自文件：`<file_path>`\n内容节选：\n> 被引用的内容\n"

    result = report_agent.chat(input_desc)
    return result.response.strip()
