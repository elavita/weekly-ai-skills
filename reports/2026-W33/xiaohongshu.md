# 小红书文案 2026-W33

本周报汇总近期值得关注的 AI Skill、Agent、MCP 与效率工具，帮助中文开发者快速了解它们的用途并完成初步筛选。内容基于公开仓库信息整理，使用前请自行核验。

## trycompai/crm

Comp AI CRM 是一个面向 AI Agent 的开源 CRM 系统，强调 Agentic-first 设计，让 AI 代理可以直接驱动客户管理流程。项目使用 TypeScript 开发，支持自托管和二次开发，适合希望把 AI Agent 接入真实业务场景的团队。亮点包括原生 Agent 支持、开源可定制以及较高的社区关注度。适用场景包括为 AI Agent 提供客户数据后端、自动化销售与客服流程，以及作为研究 Agentic CRM 架构的参考项目。

## genspark-ai/genoffice

GenOffice 是一款开源的跨平台 AI 办公套件，支持在 macOS、Windows 和 Linux 上编辑 Word、Excel、PowerPoint、PDF 和 Markdown 文档，并内置 AI Agent 辅助办公。

亮点：完全开源免费，覆盖五大主流文档格式；基于 Electron + TypeScript 构建，跨平台体验一致；内置 AI Agent，可在写作、整理与排版等场景提供智能化辅助；可作为 Microsoft Office 的轻量替代方案。

适用场景：需要统一处理多种办公文档的个人或团队；希望降低软件成本、寻找开源办公套件的开发者与中小企业；在不同桌面系统之间切换、要求一致编辑体验的用户；想基于成熟项目二次开发自定义办公工具的工程师。

## Jakubantalik/thinking-orbs

Thinking Orbs 是一个为 AI 与智能体界面设计的点阵思维球加载动画组件库。它提供 9 种调优样式与两种尺寸，并自动适配深色与浅色主题，适合用来替代传统 spinner，让等待过程更有质感。亮点包括：9 种可调优动画样式、sm 与 lg 双尺寸、自动深浅色适配、TypeScript 类型支持，以及面向 AI 对话与 Agent 流程的视觉反馈设计。适用场景包括 AI 聊天与 Agent 应用的加载指示、多步骤 Agent 流程的阶段性反馈、主题切换界面中的统一加载体验，以及作为可复用组件集成到前端项目。

## QwenAudio/qwen-audio-agent

QwenAudio/qwen-audio-agent 是一个面向 AI Agent 的实时语音运行时，让 Agent 能够像真人一样持续进行语音对话。它在 Agent 与用户之间提供低延迟的语音识别与语音合成通道，支持边听边说、边工作边交流的交互模式。

亮点：实时语音运行时专为 AI Agent 设计，强调低延迟与持续在线；端到端集成 ASR 与 TTS，打通语音输入到 Agent 再到语音输出的完整链路；与 ACP、Claude Code、Codex、OpenCode 等主流 Agent 与编码工具兼容，可作为语音接入层；使用 JavaScript 实现，便于在 Node.js 与前端环境中集成；基于 QwenAudio 开源体系，支持自定义语音模型与交互流程。

适用场景：为编码 Agent 增加语音交互能力，实现边说边写代码；为客服、销售等对话 Agent 提供实时语音通道；本地或私有化部署可定制的语音助手，集成到 IDE、终端或 Web 应用；作为研究平台探索 Agentic AI 在多模态语音场景下的交互；为无障碍或移动场景提供语音优先的 Agent 接入方式。

## makecindy/cindy

Cindy 是一款开源、开箱即用的 AI Agent 应用，基于 Electron 与 React Native 构建，覆盖 macOS、Windows、iOS 与 Android。它集成了 Claude Code、Codex 等大模型能力，主打用自然语言驱动 Agent 完成各类任务，适合想快速拥有本地化 AI Agent 体验的个人开发者和跨端用户。

本周报仅整理公开信息，不代表安全审计或使用推荐；引入项目前请核对许可证、权限和数据处理方式。
