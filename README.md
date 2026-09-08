# 智能穿搭助手 RAG 项目

基于 **Streamlit + LangChain + 通义千问(Qwen) + Chroma 向量数据库** 的 RAG（检索增强生成）问答系统。用户提问后，系统从知识库中检索相关文档片段，结合会话历史，由大模型生成专业回答。

## 功能特性

- **智能问答**：基于知识库的穿搭助手，支持尺码推荐、洗涤养护、颜色选择等领域
- **多轮会话记忆**：使用文件持久化聊天历史，支持上下文连贯对话
- **流式输出**：AI 回答实时流式展示，体验流畅
- **知识库管理**：支持上传 TXT 文件动态扩充知识库
- **向量检索**：基于 DashScope Embeddings + Chroma 进行语义检索
- **内容去重**：通过 MD5 校验避免重复入库

## 项目结构

```
.
├── app_qa.py              # 智能穿搭助手问答界面 (Streamlit)
├── app_file_uploader.py   # 知识库更新服务 (Streamlit)
├── rag.py                 # RAG 核心服务：链式调用、检索、生成
├── config_data.py         # 项目配置（模型名、分块参数、相似度阈值等）
├── knowledge_base.py      # 知识库服务：文本切分、向量化入库、MD5去重
├── vector_stores.py       # Chroma 向量存储服务
├── file_history_store.py  # 文件持久化聊天历史管理
├── data/                  # 知识库源数据
│   ├── 尺码推荐.txt
│   ├── 洗涤养护.txt
│   └── 颜色选择.txt
├── requirements.txt       # Python 依赖
└── .gitignore
```

## 技术栈

| 组件 | 说明 |
|------|------|
| Streamlit | Web 界面框架 |
| LangChain | LLM 应用编排框架 |
| 通义千问 (qwen3-max) | 对话大模型 |
| DashScope Embeddings (text-embedding-v4) | 文本向量化 |
| Chroma | 向量数据库 |
| RecursiveCharacterTextSplitter | 文本切分 |

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

需要设置 DashScope API Key（用于通义千问模型调用和 Embeddings）：

```bash
# Windows PowerShell
$env:DASHSCOPE_API_KEY = "your_api_key_here"

# Linux / macOS
export DASHSCOPE_API_KEY="your_api_key_here"
```

API Key 获取地址：https://dashscope.console.aliyun.com/

### 3. 运行问答应用

```bash
streamlit run app_qa.py
```

浏览器访问 `http://localhost:8501` 即可开始对话。

### 4. 运行知识库更新服务（可选）

如需上传新的 TXT 文件扩充知识库：

```bash
streamlit run app_file_uploader.py --server.port 8502
```

## 工作流程

1. 用户在问答界面输入问题
2. 系统将问题通过 DashScope Embeddings 向量化
3. 从 Chroma 向量库中检索最相关的文档片段
4. 将检索结果 + 会话历史 + 用户问题组装为 Prompt
5. 调用通义千问模型生成回答（流式输出）
6. 回答实时展示并保存到聊天历史
