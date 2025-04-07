import json
import openai
# 导入 LlamaIndex 相关模块
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.agent import ReActAgent
from llama_index.core import Settings, StorageContext, VectorStoreIndex
from llama_index.core.tools import QueryEngineTool
from datetime import datetime

# 设置 API key 和 base_url
openai.api_key = "sk-42kUEMoma40GUNhl595bE5D53e994eC59a7a469534564f11"
openai.base_url = "https://api.gptapi.us/v1"

Settings.llm = OpenAI(model="gpt-3.5-turbo",
                      api_key=openai.api_key,
                      base_url=openai.base_url)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

# ------------------ 构建/加载固件漏洞知识库索引 ------------------
try:
    kb_storage_context = StorageContext.from_defaults(
        persist_dir="./storage/vuln_kb")
    vuln_kb_index = load_index_from_storage(kb_storage_context)
    print("固件漏洞知识库索引加载成功。")
except Exception as e:
    print("固件漏洞知识库索引加载失败，正在构建索引……")
    # 从漏洞知识库文档所在目录加载数据
    documents = SimpleDirectoryReader("./data/vuln_kb").load_data()
    vuln_kb_index = VectorStoreIndex.from_documents(documents)
    vuln_kb_index.storage_context.persist(persist_dir="./storage/vuln_kb")
    print("固件漏洞知识库索引构建并持久化完成。")

# 创建基于知识库索引的查询引擎（返回相似度最高的 3 个结果）
kb_query_engine = vuln_kb_index.as_query_engine(similarity_top_k=3)

# 将知识库查询引擎包装为工具
kb_tool = QueryEngineTool.from_defaults(
    query_engine=kb_query_engine,
    name="vuln_knowledge_base",
    description=("提供有关固件漏洞、漏洞检测技术以及补救措施的外部背景知识。"
                 "在生成报告时可以利用该工具补充详细背景信息。"),
)

# ------------------ 构建报告生成 Agent ------------------
# 该 Agent 使用 ReAct 框架整合外部知识工具，并调用 OpenAI 的大模型生成报告
report_agent = ReActAgent.from_tools(tools=[kb_tool],
                                     llm=OpenAI(model="gpt-3.5-turbo"),
                                     verbose=True)


def generate_vulnerability_report(decision_json_str: str) -> str:
    """
    接收决策 Agent 输出的 JSON 字符串（包含固件漏洞检测分析信息），
    利用 ReAct Agent 结合外部知识生成详细的漏洞检测报告，
    并将报告以 Markdown 格式保存为 vulnerability_report.md。
    """
    try:
        decision_data = json.loads(decision_json_str)
    except Exception as e:
        return f"JSON 解析错误：{e}"

    report_md = "# 固件漏洞检测报告\n\n---\n"

    for idx, item in enumerate(decision_data, 1):
        func_name = item["function_name"]
        location = item["location"]
        severity = item["severity"]
        vuln_type = item["vulnerability_type"]
        is_vul = item["is_vulnerable"]
        desc = item["description"]

        if is_vul:
            # 构造用于查询背景知识的 prompt
            query_prompt = f"{vuln_type} 漏洞的原理、危害和修复方法"
            bg_knowledge = report_agent.chat(query_prompt).response

            report_md += (f"## 漏洞 {idx}：{func_name}()\n\n"
                          f"- **类型**：{vuln_type}  \n"
                          f"- **位置**：{location}  \n"
                          f"- **风险等级**：{severity.capitalize()}  \n\n"
                          f"**漏洞描述**：  \n{desc}\n\n"
                          f"**补充背景知识与修复建议**：  \n{bg_knowledge}\n\n---\n")
        else:
            report_md += (f"## 漏洞 {idx}：{func_name}()\n\n"
                          f"- **状态**：未发现漏洞  \n"
                          f"- **位置**：{location}  \n\n"
                          f"**说明**：  \n该函数实现规范，未检测到明显安全风险。\n\n---\n")

    report_date = datetime.today().strftime("%Y年%m月%d日")

    report_md += (f"> **报告日期**：{report_date}  \n"
                  f"> **生成工具**：FALCON ")

    # 保存 Markdown 报告
    with open("vulnerability_report.md", "w", encoding="utf-8") as f:
        f.write(report_md)

    print("✅ 漏洞检测报告已保存为 vulnerability_report.md")
    return report_md


# ------------------ 主程序入口 ------------------
if __name__ == "__main__":
    # 假设决策 Agent 的输出保存在 "output.json" 文件中，请将该文件放在项目根目录下
    try:
        with open("output.json", "r", encoding="utf-8") as f:
            decision_json_str = f.read()
    except Exception as e:
        print(f"读取决策 Agent 输出文件失败：{e}")
        exit(1)

    report = generate_vulnerability_report(decision_json_str)
    print("生成的漏洞检测报告：\n")
    print(report)
