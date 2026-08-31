# 小黑盒文案 2026-W36

本周报汇总近期值得关注的 AI Skill、Agent、MCP 与效率工具，帮助中文开发者快速了解它们的用途并完成初步筛选。内容基于公开仓库信息整理，使用前请自行核验。

## duty1g/x64dbg-mcp-server

这是一个值得进一步了解的 AI 项目；原始简介：x64dbg-MCP Server is a native MCP (Model Context Protocol) plugin for x64dbg that exposes the debugger's full functionality over HTTP. Connect any MCP-compatible AI assistant and control x64dbg programmatically: set breakpoints, step through code, read memory, dump registers, and more.  Built with Zig — zero dependencies, single-binary output, cros

项目：duty1g/x64dbg-mcp-server（1,790 Stars）。

## XiaoDuoYa/codex-with-chatgpt

codex-with-chatgpt 是一个把 ChatGPT 作为规划大脑、Codex CLI 作为执行终端的桥接项目，核心思路是让 ChatGPT 负责思考与方案生成，Codex 负责实际编码与文件操作。技术栈为 TypeScript，支持通过 OAuth 复用 ChatGPT 账号，并兼容 Model Context Protocol（MCP），可以接入外部工具与上下文。亮点：ChatGPT 与 Codex CLI 的职责分离设计；OAuth 登录降低接入成本；MCP 兼容便于扩展工具链；面向 AI Agent 场景，强调模型规划 + CLI 执行的协同模式。适用场景：在终端用自然语言驱动 Codex 完成开发任务；为已有 Codex 工作流补充更强的任务规划能力；作为 MCP 客户端参考实现；用于个人或小团队探索 ChatGPT + Codex 的协同开发流程。

## lexmount/moli

这是一个值得进一步了解的 AI 项目；原始简介：Best headless browser for AI agents. Lite, Fast, High-Compatibility. Built in Rust

项目：lexmount/moli（1,509 Stars）。

## AMAP-ML/LongHorizon-Harness

这是一个值得进一步了解的 AI 项目；原始简介：The long-horizon computer-use harness. Run AI agents across desktop apps and the CLI for extended periods while preserving task state and making reliable progress on complex workflows. Features fresh-context execution, durable verified state, independent auditing, recoverable progress, and native Claude Code / Codex / OpenClaw integration.

项目：AMAP-ML/LongHorizon-Harness（1,412 Stars）。

## 0xsline/awesome-deepseek-harness

DeepSeek Harness（DSH）是为 DeepSeek 大模型设计的 Harness 框架与插件生态，本仓库是它的精选资源列表。内容来自 dsh-external/hub 和公开的 dsh-plugin 主题，涵盖 AI Agent、MCP、LLM 工具链与编码助手等场景，以 Python 项目为主。对于想了解 DeepSeek 周边生态、寻找可复用插件或基础设施的开发者来说，可以作为一个索引起点。

本周报仅整理公开信息，不代表安全审计或使用推荐；引入项目前请核对许可证、权限和数据处理方式。
