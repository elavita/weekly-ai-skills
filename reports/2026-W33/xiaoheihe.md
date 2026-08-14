# 小黑盒文案 2026-W33

本周报汇总近期值得关注的 AI Skill、Agent、MCP 与效率工具，帮助中文开发者快速了解它们的用途并完成初步筛选。内容基于公开仓库信息整理，使用前请自行核验。

## trycompai/crm

Comp AI CRM 定位为 Agentic-first 的开源 CRM，目标是让 AI Agent 能够直接操作客户关系管理流程，而非仅仅作为人类使用的工具。项目基于 TypeScript，代码结构清晰，便于集成到现有 Agent 框架中。亮点在于开源可自托管、原生面向 Agent 设计以及活跃的社区。适合需要把 AI Agent 接入 CRM 流程的开发者、构建自动化销售或客服系统的团队，以及研究 Agentic 业务系统架构的工程师参考使用。

## genspark-ai/genoffice

GenOffice 是一款开源、跨平台的 AI 办公套件，基于 Electron 与 TypeScript 开发，支持在 macOS、Windows 和 Linux 上编辑 Word、Excel、PowerPoint、PDF 和 Markdown 文档，并内置 AI Agent。

亮点：完全开源免费，跨平台覆盖三大桌面系统；统一支持 docx、xlsx、pptx、PDF 与 Markdown 编辑；内置 AI Agent，可在文档处理流程中提供智能化辅助；项目结构清晰，适合作为 Electron 办公类应用的参考实现。

适用场景：需要一站式处理多种办公文档的个人与团队；希望替代商业办公软件、降低成本的开发者与中小企业；需要在不同操作系统下保持一致编辑体验的用户；计划基于该项目进行二次开发或集成 AI 能力的工程师。

## Jakubantalik/thinking-orbs

Thinking Orbs 是一个面向 AI 与 Agent 界面的点阵思维球加载动画组件库，提供 9 种调优样式与两种尺寸，并自动适配深色与浅色主题。亮点：9 种可调优动画样式、sm 与 lg 双尺寸、自动深浅色适配、TypeScript 类型支持，专为 AI 对话与 Agent 流程设计。适用场景：AI 聊天与 Agent 应用的加载指示、多步骤 Agent 流程的阶段性反馈、主题切换界面中的统一加载体验，以及作为可复用组件集成到前端项目。

## QwenAudio/qwen-audio-agent

QwenAudio/qwen-audio-agent 是一个面向 AI Agent 的实时语音运行时，让 Agent 能够持续进行语音对话并保持在线状态。它在 Agent 与语音通道之间提供低延迟的语音识别与语音合成能力，使 Agent 可以边听边说、边工作边交流。

亮点：实时语音运行时专为 AI Agent 设计，强调低延迟与持续在线的交互模式；端到端集成 ASR 与 TTS，打通语音输入到 Agent 再到语音输出的完整链路；与 ACP、Claude Code、Codex、OpenCode 等 Agent 与编码工具兼容，可作为语音接入层；使用 JavaScript 实现，便于在 Node.js 与前端环境中集成和二次开发；基于 QwenAudio 开源体系，开发者可自定义语音模型、提示词与交互流程。

适用场景：为 Claude Code、Codex、OpenCode 等编码 Agent 增加语音交互能力；为客服、销售等对话 Agent 提供实时语音通道；本地或私有化部署可定制的语音助手，集成到 IDE、终端或 Web 应用；作为研究平台探索 Agentic AI 在多模态、实时语音场景下的交互模式；为无障碍或移动场景提供语音优先的 Agent 接入方式。

## makecindy/cindy

Cindy 是一款开源、开箱即用的 AI Agent 桌面与移动端应用，基于 Electron 与 React Native 构建，支持 macOS、Windows、iOS 与 Android。它内置对 Claude Code、Codex 等 LLM 的集成，主打用自然语言驱动 Agent 执行任务，适合希望快速搭建本地 AI Agent、构建自定义工作流或参考跨端架构的开发者。

本周报仅整理公开信息，不代表安全审计或使用推荐；引入项目前请核对许可证、权限和数据处理方式。
