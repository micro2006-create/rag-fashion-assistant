# 作品集：基于 RAG 的智能穿搭助手问答系统

## 项目信息

| 项目 | 内容 |
|------|------|
| **项目名称** | 基于 RAG 的智能穿搭助手问答系统 |
| **GitHub 仓库** | https://github.com/micro2006-create/rag-fashion-assistant |
| **技术栈** | Python / Streamlit / LangChain / Chroma / DashScope / 通义千问(qwen3-max) |
| **项目类型** | 个人项目 |

## 项目简介

面向穿搭场景的知识问答系统，用户通过自然语言提问，系统从内置知识库（尺码推荐、洗涤养护、颜色选择）检索相关内容，由大模型生成精准回答，并支持多轮对话。同时提供文件上传服务，允许将新的 TXT 文档增量扩充至向量知识库，实现知识库动态维护。

## 核心功能

1. **RAG 完整链路**：文本切分(chunk_size=200) → DashScope Embeddings 向量化 → Chroma 持久化向量库 → similarity_search 检索 → ChatTongyi 生成回答
2. **多轮会话记忆**：基于 RunnableWithMessageHistory 维护对话上下文，避免跨轮次信息丢失
3. **知识库增量维护**：文件上传 + MD5 文件级去重，避免重复文档入库
4. **流式输出**：Streamlit streaming 实现 AI 回复实时逐字渲染

## 运行截图

### 1. 初始页面

系统启动后的问答界面：

![初始页面](https://cdn.jsdelivr.net/gh/micro2006-create/rag-fashion-assistant@main/portfolio/images/01_initial.png)

### 2. 测试问题一：颜色推荐

**用户提问**：夏天穿什么颜色的衣服？

**系统行为**：Agent 从颜色选择知识库中检索相关内容，基于检索结果给出夏天颜色推荐建议。

![颜色推荐问答](https://cdn.jsdelivr.net/gh/micro2006-create/rag-fashion-assistant@main/portfolio/images/02_question_color.png)

### 3. 测试问题二：洗涤养护

**用户提问**：衣服应该怎么洗涤和养护？

**系统行为**：Agent 从洗涤养护知识库中检索相关内容，给出衣物洗涤与养护的具体建议。

![洗涤养护问答](https://cdn.jsdelivr.net/gh/micro2006-create/rag-fashion-assistant@main/portfolio/images/03_question_wash.png)

### 4. 测试问题三：尺码推荐

**用户提问**：我身高180cm，体重70kg，应该选什么尺码？

**系统行为**：Agent 从尺码推荐知识库中检索匹配信息，根据身高体重给出 L/XL 尺码推荐。

![尺码推荐问答](https://cdn.jsdelivr.net/gh/micro2006-create/rag-fashion-assistant@main/portfolio/images/04_question_size.png)

## 技术架构

```
用户提问 → Streamlit 前端
    ↓
LangChain RunnableWithMessageHistory (多轮会话)
    ↓
Chroma similarity_search (检索 top-k 知识片段)
    ↓
提示词模板注入检索结果
    ↓
ChatTongyi (qwen3-max) 生成回答
    ↓
streaming 流式输出 → Streamlit 前端
```

## 知识库数据

| 文件 | 内容 |
|------|------|
| `data/尺码推荐.txt` | 不同身高体重对应的服装尺码建议 |
| `data/洗涤养护.txt` | 各类材质衣物的洗涤与养护方法 |
| `data/颜色选择.txt` | 不同场景/季节的颜色搭配建议 |
