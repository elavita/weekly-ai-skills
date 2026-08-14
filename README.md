# AI 技能周报工作流

这是一个可直接上传到公开 GitHub 仓库的 Python 3.11 项目。它每周检索新创建且已有一定关注度的 AI skill、Agent、MCP 和 AI tool 仓库，先用模型将项目元数据加工为简体中文，再生成周报、两个社交平台文案、结构化数据与配图，并通过 GitHub Actions 提交结果和创建或更新当期 Issue。每期文档开头会说明周报用途，每个项目先用摘要回答“这个项目是做什么的”，再列出亮点和适用场景。

## 安全边界

工作流只调用 GitHub Search/README API、下载受限图片并调用可选的 OpenCode Zen 接口。**不会 clone、安装或执行任何第三方仓库代码**。本项目不自动访问第三方项目的公开 Demo，也不生成 Demo 浏览器截图，因为网页可能包含追踪、恶意下载、登录诱导或动态执行风险；配图只使用 README 中明确的 screenshot/demo/preview/showcase 图片、GitHub Open Graph 图片，或本地生成的信息卡。

本项目只生成内容和 GitHub Issue，**不会自动发布到小红书、小黑盒或其他社交平台**。发布前需要人工核对事实、许可证、图片授权与平台规则。

## 本地运行

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m src.main --config config.json --dry-run
python -m src.main --config config.json
pytest
```

`--dry-run` 会生成当期 `reports/` 文件用于检查，但不会写入 `state/published.json`，也不会提交、推送或发布远程内容。CLI 本身从不执行 Git 提交；提交和 Issue 发布只存在于 Actions 工作流中。

本地 GitHub API 未认证限额较低。可通过环境变量 `GITHUB_TOKEN` 提供低权限令牌；不要把令牌写入配置或提交到仓库。

## 配置

直接修改仓库根目录的 `config.json`。它只包含非敏感运行参数，会随项目上传并由 GitHub Actions 使用；`config.example.json` 保留为默认配置备份。主要配置包括：

- `github.min_stars`、`windows_days`、`max_projects`：星标阈值、递增检索窗口和每期项目数。
- `github.search_terms`、分页上限和超时：GitHub Search API 参数。
- `zen.endpoint`、`model`、`auth_header`、`auth_scheme`：OpenAI Chat Completions 兼容接口。
- `content`：报告标题、受众与文案参数。
- `images`：尺寸、最大下载字节数、超时、允许的内容类型、README 图片关键词与 badge 过滤规则。

`.env.example` 仅列出环境变量名称。程序不会自动读取 `.env`，避免意外将密钥带入子进程；请在 shell 或 GitHub Secrets 中设置。

## 模型接口

当前配置使用 NVIDIA 的 OpenAI Chat Completions 兼容接口 `https://integrate.api.nvidia.com/v1` 和模型 `minimaxai/minimax-m3`，请求路径为 `/chat/completions`，密钥读取自 `ZEN_API_KEY`。认证 header 和 scheme 可在配置中调整。提示词要求严格 JSON，并根据 `content.language` 和 `content.audience` 将英文项目简介归纳、翻译和润色为中文；项目名、技术名及 API 名称可以保留原文。程序还会校验必需字段、非空文本和列表内容。

没有密钥、请求失败、超时、返回非 JSON 或校验失败时，程序固定使用以下结构化模板降级，不中断整期生成：

- 摘要：`仓库名：GitHub description`
- 亮点：Stars、主要语言、人工核对提示
- 场景：评估其在 AI Agent、MCP 或开发工具工作流中的适用性
- 平台文案：仓库名、Stars/description，以及许可证和数据安全核对提示

免费模型可能存在速率限制、临时不可用、输出质量波动或服务政策变化。密钥只通过请求 header 发送，不写入日志、报告、manifest 或 state。

## GitHub Actions

`.github/workflows/weekly.yml` 支持：

- 每周一北京时间 09:17 执行，对应 cron `17 1 * * 1`（GitHub cron 使用 UTC）。
- 手动 `workflow_dispatch`。
- `permissions: contents: write` 和 `issues: write`。
- 同分支 concurrency，防止定时与手动任务并行重复生成。
- 同一 ISO 周已经发布时直接复用结果；历史项目按 `state/published.json` 的 `node_id` 去重。
- 仅在 `reports` 或 `state` 变化时提交，提交信息包含 `[skip ci]`；工作流没有 `push` 触发，因此不会递归。
- 当期 Issue 带隐藏 period 标记，存在则更新，不存在则创建；即使当期报告已存在、无需产生新提交，也会补建缺失的 Issue。

首次上传公开仓库后：

1. 在仓库 `Settings > Actions > General > Workflow permissions` 允许 Read and write permissions，确保组织策略没有覆盖工作流声明。
2. 在 `Settings > Secrets and variables > Actions` 新建可选 Secret `ZEN_API_KEY`。不配置也能使用固定模板运行。
3. 在 Actions 页打开 `Weekly AI Skill Report`，执行一次 `Run workflow`（`workflow_dispatch`）验证权限和输出。

工作流使用官方 actions 的明确稳定主版本 tag：`actions/checkout@v4`、`actions/setup-python@v5`、`actions/github-script@v7`。这些 tag 易维护但不等同于不可变 commit SHA；对供应链要求更高时，应在上传前将其固定到官方发布对应的完整 SHA，并定期通过 Dependabot 更新。

## 输出

每期写入 `reports/YYYY-Www/`：

- `report.md`：主周报；只有创建不超过 7 天的项目才标记“本周新增”，扩窗结果会显示实际天数。
- `data.json`：完整结构化数据。
- `xiaohongshu.md`、`xiaoheihe.md`：待人工审核的平台文案。
- `manifest.json`：文件、数量和每张图片来源。
- `images/`：README 图片、GitHub Open Graph 图片或本地信息卡。

`state/published.json` 保存已发布 `node_id`、最后期号和更新时间。GitHub Search API 最多只返回前 1000 个结果，本项目通过多个关键词、分页和 `node_id` 去重缓解该限制；它不是全量索引。Stars 是运行时快照，热门新仓库仍可能因搜索索引延迟到下一期才出现。
