# 小红书文案 2026-W34

本周报汇总近期值得关注的 AI Skill、Agent、MCP 与效率工具，帮助中文开发者快速了解它们的用途并完成初步筛选。内容基于公开仓库信息整理，使用前请自行核验。

## NVIDIA-NeMo/labs-OO-Agents

NVIDIA NeMo 开源的面向对象 Agent 框架，主打用 Python 类的方式来组织 AI Agent 的状态、行为和工具调用，结构清晰、易于复用和扩展，适合想把 Agent 工程化落地的开发者。亮点包括 Pythonic 的 API 设计、模块化的 Agent 组合能力，以及与 NeMo 生态的结合。适合需要构建可维护自定义 Agent、进行多 Agent 协作，或在企业应用中集成大模型自动化的团队。

## VictorTaelin/OptMem

OptMem 是一个为 AI Agent 提供永久记忆能力的轻量方案，核心是一段约 426 token 的提示词加上一个脚本，无需向量数据库或外部存储即可让 Agent 跨会话保留上下文。亮点在于极简集成、低资源占用和可定制的记忆结构，适合个人项目或低预算场景。典型用法包括为本地脚本 Agent 添加长期记忆、在受限环境中维持对话连续性，以及作为学习 Agent 记忆机制的参考实现。

## petergyang/human-review

human-review 是一个让 AI Agent 工作流加入人工审阅环节的可视化工具。它可以在浏览器中打开 HTML 或 Markdown 文件，像 Google Doc 一样选中内容并添加评论，再把结构化反馈回传给 Claude Code、Codex 等 AI 编程助手。亮点包括可视化批注界面、结构化反馈回传、兼容主流 AI 编程工具、支持 HTML 与 Markdown 双格式，以及人在回路设计。适合需要让 AI 生成文档或网页后由人工把关的开发者与团队，也可用作自动化流水线中的质量审核中间层。

## miuuyy/codex-chatgpt-web

项目摘要：这是一个把 ChatGPT Web（含 Pro）封装为 Codex 原生模型的桥接工具，让 Codex 能突破使用额度限制，获得上下文、工具调用、流式输出和图像等能力。

亮点：基于 TypeScript 与 Playwright 自动化浏览器，把 ChatGPT Web 作为后端接入 Codex；支持上下文保持、工具调用、流式响应和图像输入输出；兼容 ChatGPT Pro 账号，提供 MCP 相关能力扩展；面向 macOS 等本地开发环境，便于在 Codex 应用中直接使用。

适用场景：在 Codex 中使用 ChatGPT Pro 模型而消耗 Pro 额度；需要长上下文或多模态输入输出的开发任务；希望把 ChatGPT Web 能力接入现有 Codex 工作流的开发者；在本地 macOS 环境搭建自定义 AI 编程助手后端；通过 MCP 扩展为 Codex 增加更多工具和外部能力。

## pireel/pireel

Pireel 是一个开源 AI 视频剪辑工具，作为剪映和 ChatCut 的替代方案，可通过 MCP 协议被任意 AI Agent 驱动。

亮点：开源替代剪映与 ChatCut；支持 MCP 协议，可被任意 AI Agent 调用；覆盖字幕、对话剪辑、关键帧、口播等 AI 视频场景；TypeScript 实现，便于二次开发。

适用场景：希望通过 AI Agent 自动生成字幕与剪辑的团队；想用自然语言指令驱动视频编辑流程的创作者；需要在自有产品中集成视频编辑能力并希望避免商业工具绑定的开发者。

本周报仅整理公开信息，不代表安全审计或使用推荐；引入项目前请核对许可证、权限和数据处理方式。
