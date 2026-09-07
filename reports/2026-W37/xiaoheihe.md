# 小黑盒文案 2026-W37

本周报汇总近期值得关注的 AI Skill、Agent、MCP 与效率工具，帮助中文开发者快速了解它们的用途并完成初步筛选。内容基于公开仓库信息整理，使用前请自行核验。

## Hisn00w/ASu-skills

ASu-skills 是一个面向求职与开发场景的 AI Skills 集合，提供简历优化、岗位投递、面试准备与开发提效等实用工具，帮助求职者和开发者更高效地完成日常任务。

亮点：聚焦求职与开发两大高频场景，整合简历优化、岗位投递、面试准备等实用 AI Skills；支持开发提效，覆盖编码、调试等常见工作流；以 Skills 形式封装，可按需调用，便于集成到 AI Agent 或 MCP 工作流中；项目使用 HTML 编写说明文档，结构清晰、上手成本低；在 GitHub 上获得超过 3700 Star，受到中文开发者社区关注。

适用场景：求职者使用 AI Skills 优化简历内容、匹配岗位 JD 并辅助生成求职信；面试前进行模拟问答、梳理技术要点与项目经验；开发者借助 Skills 提升编码、调试与文档编写等日常开发效率；将项目中的 Skills 集成到自有 AI Agent 或 MCP 工具链中；作为中文 AI Skills 资源参考，用于学习如何构建面向场景的 Agent 能力包。

## cbrock84/headcount

Headcount 把 Claude Code 的智能体能力抽象成公司组织结构，提供 15+ 部门和 125+ 技能，每个单元都封装为可独立安装的插件，方便按需启用和组合。项目以 Markdown 维护配置，兼容 Claude Code 插件与 MCP 生态，可作为智能体插件市场使用。适合希望系统化管理 Claude Code 扩展、按职能复用 AI 技能，或研究智能体编排与 MCP 集成的开发者参考。

## totec448-spec/chat-on-steroids

Chat-on-Steroids 是一个面向 ChatGPT 的本地优先跨平台 MCP 客户端，核心解决“ChatGPT 只能在网页里聊天、缺乏本地工具与持久化能力”的问题。它通过 Electron 应用与 Chrome 扩展提供 Chrome 集成，并基于 MCP 协议在本地调用工具和数据源，覆盖 Windows、macOS 与 Linux。功能上包含 Goal 目标驱动、Compact & Resume 长对话压缩续接，以及 durable multi-agent workflows 多智能体持久协作。技术栈为 TypeScript + Electron，适合关注 AI Agent、MCP 与效率工具的开发者用于本地自动化、长任务编排和 MCP 客户端参考实现。

## pgrundev/pgbot

pgbot 是一个面向 AI Agent 与应用的 PostgreSQL 智能层，让大模型能够安全、可控地查询和分析 Postgres 数据库。它通过自然语言接口把数据库能力暴露给 AI Agent，简化数据访问与洞察生成的流程。

亮点：
- 为 AI Agent 提供 Postgres 智能接入，支持自然语言驱动的数据查询与分析
- 深度适配 PostgreSQL 生态，便于在现有 Postgres 环境中部署
- 使用 Go 实现，性能与可扩展性较好，适合作为后端服务组件
- 面向 AI 应用场景设计，可作为 Agent 与数据库之间的中间层
- 开源项目，便于二次开发与定制化

适用场景：
- 为 AI Agent 提供安全、受控的 PostgreSQL 数据访问能力
- 在 AI 应用中实现自然语言转 SQL 的数据查询与分析
- 作为数据助手后端，帮助业务人员通过对话方式获取数据库洞察
- 集成到企业内部系统中，让 LLM 应用直接对接 Postgres 数据源
- 用于构建数据库相关的自动化工作流，例如报表生成、异常检测与数据探索

## 2akouwu/reverify

reverify 是一个面向 AI Agent 的 MCP 服务器与 CLI，核心思路是把 LLM 降级为「主张提出者」，由确定性工具做最终裁决，每条结论都附带可追溯证据，从而抑制大模型在逆向工程、CTF、恶意软件分析等场景下的幻觉。技术亮点包括主张-裁决-证据三段式验证流程、可对接二进制分析与反汇编工具链的 MCP 接口、以及验证后事实与上下文的持久化复用。典型用法包括 AI 辅助逆向工程中的函数与协议行为核验、CTF 解题中的逐步推理验证、恶意软件分析中的可疑行为取证，以及作为通用反幻觉层接入 AI 编码助手。

本周报仅整理公开信息，不代表安全审计或使用推荐；引入项目前请核对许可证、权限和数据处理方式。
