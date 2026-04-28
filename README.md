# 汕头万象城冰场 AI Skill

![Version](https://img.shields.io/badge/version-0.1.0-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![MCP](https://img.shields.io/badge/protocol-MCP-purple) ![Transport](https://img.shields.io/badge/transport-stdio%20%7C%20HTTP-orange)

这是一个可交付给冰场门店的 AI Skill：安装后，Agent 能回答冰场经营信息（票价、冰时、位置、教练、课程、公告），并在用户明确意向时触发预约登记（飞书多维表格）。

适用优先级：**OpenClaw / Claw 类工具优先**，Cursor / Trae 也可用。

## 场馆信息：汕头万象城冰场

当前 Skill 对应场馆为 `shantou-mixc`：

| 项目 | 内容 |
|------|------|
| 场馆名称 | 冰纷万象滑冰场（汕头万象城店） |
| 地址 | 汕头市长平路与金环路交界汕头万象城 L556（约 5 楼） |
| 营业时间 | 周一至周四、周日 10:00–22:00；周五、周六 10:00–22:30（以实际查询为准） |
| 咨询电话 | 0754-8899 2291 |

具体票价、课程与设施请以 MCP 实时查询结果为准。

## 给人看的：怎么用（OpenClaw 首选）

### 1) OpenClaw（推荐）

在 OpenClaw MCP 配置中使用 stdio：

- `command`: `<SKILL_ROOT>/mcp_server/.venv/bin/python`
- `args`: `["-m", "ice_arena_mcp"]`
- `cwd`: `<SKILL_ROOT>/mcp_server`

Windows 可改为：

- `command`: `<SKILL_ROOT>\\mcp_server\\.venv\\Scripts\\python.exe`

### 2) Cursor / Trae（可选）

在工作区 `.cursor/mcp.json` 或 `.trae/mcp.json` 中添加 `shanwan-ice-arena`，核心参数与 OpenClaw 一致（`command/args/cwd` 指向 `mcp_server`）。

### 3) 环境变量（预约写入）

在仓库根目录创建 `.env`（参考 `.env.example`）：

- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`
- `FEISHU_BITABLE_APP_TOKEN`
- `FEISHU_BITABLE_TABLE_ID`
- `FEISHU_BOOKING_PHONE_FIELD`

可选：

- `FEISHU_BOOKING_SOURCE_FIELD`
- `FEISHU_BOOKING_INTENT_FIELD`
- `FEISHU_BOOKING_STATUS_FIELD`

> `.env` 已在 `.gitignore` 中，不应提交真实凭证。

## 给 Agent 看的：怎么执行

本 Skill 基于 MCP 提供 9 个只读工具，并集成飞书预约登记流程：

| 能力 | 你可以问 | 对应工具 |
|------|----------|----------|
| 场馆概览 | “介绍一下冰场”“值得去吗” | `get_venue_overview` |
| 营业与冰时 | “几点开门”“清冰时段”“本周几有活动栏场” | `get_hours_and_schedule` |
| 位置与联系 | “在几楼”“电话是多少” | `get_location_and_contacts` |
| 价格与货盘（门票/陪同/护具/私教体验/多次卡/活动价） | “单次票多少钱”“护具租赁”“五一活动价”“办卡入口” | `get_ticketing_policy` |
| 场馆设施 | “有没有储物柜”“有没有吹风机”“停车怎么办” | `get_facilities` |
| 教练与课程 | “都有哪些教练”“私教怎么约”“课程怎么报名” | `get_coaching_and_programs` |
| FAQ | “常见问题” | `get_faq` |
| 活动公告 | “最近有什么活动” | `get_news_and_promotions` |
| 飞书预约登记 | “帮我预约试听”“留手机号预约” | 先确认意向→收手机号→写飞书多维表格 |

**Agent 关键规则**：

- 先调 MCP，再回答；禁止直接读 YAML 作为对用户回答依据。
- 价格问题一律调 `get_ticketing_policy`。
- 用户有预约意向时：先确认是否现在预约，再收手机号，再写飞书多维表格。
- MCP 不可用时降级到“建议到店或官方渠道”，不编造价格和规则。

## 目录结构

```
shanwan-ice-arena-skill/
├── README.md                 # 本文档（安装 + 使用）
├── SKILL.md                  # Agent 指令（触发场景 / 调用策略）
├── skill.json                # 机器可读：MCP 端点、工具与品牌 Prompt
├── LICENSE
├── mcp_server/               # 本地 MCP 服务（FastMCP + YAML）
│   ├── README.md             # 运行细节、环境变量、验证步骤
│   ├── pyproject.toml / requirements.txt
│   ├── ice_arena_mcp/        # FastMCP server、store、入口
│   └── data/
│       └── venues/
│           └── shantou-mixc.yaml   # 当前场馆数据
```

## 飞书预约登记

本 Skill 在主流程中集成飞书预约登记，用于在用户确认后收集手机号并通过飞书官方 API 写入多维表格预约记录。流程为：

1. 先确认用户是否现在发起预约；
2. 用户同意后收集手机号（11 位）；
3. 获取 `tenant_access_token` 后，调用多维表格新增记录接口写入预约数据（手机号、来源、意向、状态等字段）。

若鉴权失败、权限不足、字段不匹配或限流，Agent 需返回明确失败原因和下一步处理建议。

> 预约提交是**真实业务行为**，提交前 Agent 必须获得用户确认。

## 验证正常运行

常见现象速查：

- `Tools & MCPs` 里**红色 Error**：检查 `${workspaceFolder}` 是否指向正确工作区根、`mcp_server/.venv` 是否已安装、`command/args/cwd` 是否正确。
- **Agent 不调用工具**：确保在 Agent 模式，且工具未被禁用；可在设置里允许工具执行或开启 Auto-run。
- **YAML 改了没生效**：stdio 模式下需要让 Cursor 重新连接（或重启 Cursor / 重启 MCP 进程）。

## 技术协议

| 项目 | 说明 |
|------|------|
| 协议 | MCP (Model Context Protocol) |
| 传输 | stdio（本地 Cursor 推荐）/ Streamable HTTP（可上云） |
| 运行 | Python FastMCP + PyYAML，场馆 YAML 启动时驻内存 |
| 部署 | 试点阶段本地 stdio；企业场景可部署至容器 / 云厂商常驻 Web 服务 |

## 版本

当前版本：**0.1.0**（试点初版）。

## License

[MIT](LICENSE)
