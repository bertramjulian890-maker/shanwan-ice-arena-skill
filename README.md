# 汕头万象城冰场 AI Skill

![Version](https://img.shields.io/badge/version-0.1.0-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![MCP](https://img.shields.io/badge/protocol-MCP-purple) ![Transport](https://img.shields.io/badge/transport-Streamable%20HTTP-orange)

这是一个可交付给冰场门店的 **公开 Skill 元数据包**：安装后，Agent 通过 **远程 MCP（Streamable HTTP）** 回答票价、冰时、位置、教练、课程、公告等事实信息，并在用户确认后通过 **`submit_booking_record`** 提交预约登记（写入动作仅在服务端完成，客户端不接触任何写入凭据）。

**本仓库 intentionally 不包含** MCP 服务代码、经营性数据文件及任何服务端密钥；这些由你在私有部署环境（如 Render）托管。

适用优先级：**OpenClaw / Claw 类工具优先**，Cursor / Trae 也可用。

## 场馆信息：汕头万象城冰场（摘要）

当前 Skill 默认对应场馆为 `shantou-mixc`：

| 项目 | 内容 |
|------|------|
| 场馆名称 | 冰纷万象滑冰场（汕头万象城店） |
| 地址 | 汕头市长平路与金环路交界汕头万象城 L556（约 5 楼） |
| 营业时间 | 周一至周四、周日 10:00–22:00；周五、周六 10:00–22:30（以 MCP 查询为准） |
| 咨询电话 | 0754-8899 2291 |

具体票价、课程与设施请以 MCP 实时查询结果为准。

## 给人看的：怎么用

### 1) 配置远程 MCP

本仓库 `skill.json` 已指向线上 MCP（可自行 fork 后改为你的端点）：

```json
"mcp_server": {
  "transport": "streamable-http",
  "url": "https://shanwan-ice-arena-skill.onrender.com/mcp"
}
```

在 OpenClaw / Cursor / Trae 的 MCP 配置中引用同一 URL（或与产品文档一致的「HTTP MCP」字段）。

### 2) 能力一览

| 能力 | 你可以问 | 对应工具 |
|------|----------|----------|
| 场馆概览 | “介绍一下冰场”“值得去吗” | `get_venue_overview` |
| 营业与冰时 | “几点开门”“清冰时段”“本周几有活动栏场” | `get_hours_and_schedule` |
| 位置与联系 | “在几楼”“电话是多少” | `get_location_and_contacts` |
| 价格与货盘 | “单次票多少钱”“护具租赁”“五一活动价”“办卡入口” | `get_ticketing_policy` |
| 场馆设施 | “有没有储物柜”“停车怎么办” | `get_facilities` |
| 教练与课程 | “都有哪些教练”“私教怎么约” | `get_coaching_and_programs` |
| FAQ | “常见问题” | `get_faq` |
| 活动公告 | “最近有什么活动” | `get_news_and_promotions` |
| 预约登记 | “帮我预约试听”“留手机号预约” | 先确认意向 → 收手机号 → **`submit_booking_record`** |

**Agent 要点**：

- 先调 MCP，再回答；不得编造价格与规则。
- 价格问题一律调 `get_ticketing_policy`。
- 预约须在用户明确同意后再调用 `submit_booking_record`；客户端不得配置服务端写入凭据。

## 目录结构（公开仓库）

```
shanwan-ice-arena-skill/
├── README.md
├── SKILL.md
├── skill.json
└── LICENSE
```

部署侧 MCP 服务与经营数据由你在 **私有仓库或托管平台控制台** 维护，不在此处开源。

## 验证

- MCP URL 可访问且返回工具列表中含上述工具（含 `submit_booking_record`）。
- 若连接失败，检查 HTTPS、路径 `/mcp`，以及线上部署是否正常对外监听。

## 技术协议

| 项目 | 说明 |
|------|------|
| 协议 | MCP (Model Context Protocol) |
| 传输 | Streamable HTTP（远程） |
| 数据与写入 | 由部署方在意图明确时通过 MCP 工具完成；凭据仅在服务端 |

## 版本

当前版本：**0.1.0**（试点初版）。

## License

[MIT](LICENSE)
