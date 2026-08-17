# 小黑盒文案 2026-W34

本周报汇总近期值得关注的 AI Skill、Agent、MCP 与效率工具，帮助中文开发者快速了解它们的用途并完成初步筛选。内容基于公开仓库信息整理，使用前请自行核验。

## NVIDIA-NeMo/labs-OO-Agents

NVIDIA NeMo 推出的面向对象 Agent 框架 labs-OO-AgAgents，把 Agent 的逻辑封装到 Python 类中，强调继承、组合与模块化，方便在生产项目中复用和扩展。核心特性是 Pythonic 的 API、清晰的 Agent 结构设计，以及与 NeMo 模型生态的集成。典型场景包括自定义 Agent 开发、多 Agent 工作流编排，以及在企业级 Python 项目中集成大模型能力。

## VictorTaelin/OptMem

OptMem 解决的是 AI Agent 缺乏持久记忆的问题，通过约 426 token 的提示词加脚本实现即插即用的跨会话记忆，不依赖向量库或外部服务。技术亮点包括极简部署、无外部依赖、低 token 开销以及结构化的提示词设计，便于按需扩展。适用场景涵盖个人 Agent 项目、本地脚本化 Agent、低资源环境下的上下文保持，以及作为 Agent 记忆机制的实验与教学样例。

## petergyang/human-review

human-review 是一个面向 AI Agent 的可视化反馈工具，用于在浏览器中批注 HTML 与 Markdown 文件并将评论回传给 AI 编程助手。核心能力包括类 Google Doc 的可视化批注、结构化反馈输出、与 Claude Code 和 Codex 等工具的集成，以及对人在回路协作流程的支持。典型场景包括 AI 生成内容后的人工修订、团队对 AI 输出物的评审，以及在自动化流水线中插入人工审核环节。

## miuuyy/codex-chatgpt-web

项目摘要：这是一个把 ChatGPT Web（含 Pro）封装为 Codex 原生模型的桥接工具，让 Codex 能突破使用额度限制，获得上下文、工具调用、流式输出和图像等能力。

亮点：基于 TypeScript 与 Playwright 自动化浏览器，把 ChatGPT Web 作为后端接入 Codex；支持上下文保持、工具调用、流式响应和图像输入输出；兼容 ChatGPT Pro 账号，提供 MCP 相关能力扩展；面向 macOS 等本地开发环境，便于在 Codex 应用中直接使用。

适用场景：在 Codex 中使用 ChatGPT Pro 模型而消耗 Pro 额度；需要长上下文或多模态输入输出的开发任务；希望把 ChatGPT Web 能力接入现有 Codex 工作流的开发者；在本地 macOS 环境搭建自定义 AI 编程助手后端；通过 MCP 扩展为 Codex 增加更多工具和外部能力。

## pireel/pireel

Pireel 是一个开源 AI 视频剪辑工具，作为剪映和 ChatCut 的替代方案，可通过 MCP 协议被任意 AI Agent 驱动。

亮点：开源替代剪映与 ChatCut；支持 MCP 协议，可被任意 AI Agent 调用；覆盖字幕、对话剪辑、关键帧、口播等 AI 视频场景；TypeScript 实现，便于二次开发。

适用场景：希望通过 AI Agent 自动生成字幕与剪辑的团队；想用自然语言指令驱动视频编辑流程的创作者；需要在自有产品中集成视频编辑能力并希望避免商业工具绑定的开发者。

本周报仅整理公开信息，不代表安全审计或使用推荐；引入项目前请核对许可证、权限和数据处理方式。
