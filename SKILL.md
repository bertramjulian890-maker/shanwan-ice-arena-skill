---
name: shanwan-ice-arena-skill
display_name: 汕头万象城冰场信息查询
description: 查询汕头万象城冰场信息。
version: 0.1.0
author: 汕万AI
license: MIT
repository: ""
category: 信息查询
alwaysApply: false
keywords:
  - 汕头万象城
  - 万象城冰场
  - 汕头冰场
  - 汕头滑冰
  - 汕头溜冰
  - 冰场
  - 滑冰
  - 溜冰
  - 真冰
  - 冰刀
  - 冰场信息
  - 冰场价格
  - 冰场票价
  - 冰场门票
  - 冰场营业时间
  - 冰场设施
  - 冰场活动
  - 冰场预约
  - 冰场取消
  - 冰场退款
  - 冰场投诉
  - 冰场教练
  - 冰场课程
  - 私教
  - 办卡
  - 会员卡
  - 次卡
  - 年卡
  - 护具租赁
  - 冰场排队
  - 清冰
---

> **⚠️ AI Agent 必读（OpenClaw/Claw 优先）**
>
> 本文档中的示例话术仅作语气参考。票价、时间、电话、链接等事实数据必须以 MCP 工具返回 JSON 为准。
>
> **客户端优先级**：OpenClaw / Claw 类工具优先，Cursor / Trae 次之。
>
> **统一接入建议（优先 stdio）**：
> - 在客户端侧配置 `command + args + cwd` 由客户端拉起 MCP 子进程；
> - 不依赖“某个终端里手动起过一次服务”；
> - 仅当客户端不支持 stdio 时，才使用 HTTP `http://127.0.0.1:8710/mcp`。
>
> **禁止绕过 MCP 读 YAML**：即使仓库里有 `mcp_server/data/venues/*.yaml`，Agent 也不得直接读文件回答用户。MCP 不可用时只能降级，不得编造价格与规则。
>
> **降级策略**：MCP 不可用时，简述“建议到店或查看官方渠道”，不编造价格与规则。

# 汕头万象城冰场 · 信息查询 Skill

## 安装后引导

用户刚启用技能时，Agent 可主动说明：
1. 可询问营业时间、门票、护具租赁、教练与课程、预约/办卡链接等。
2. 推荐首次提问示例：
   - 「汕头万象城冰场在几楼？」
   - 「单次票多少钱、包含什么？」
   - 「有没有教练预约链接？」
3. 信息由 MCP 读取场馆 YAML，运营更新 YAML 后即对外生效。

## 触发场景

| 用户可能会问 | 调用什么 |
|---|---|
| 有哪些场馆 / 多店 ID | `list_venues` |
| 介绍冰场、是否适合新手 | `get_venue_overview` |
| 营业时间、清冰、当日/某日每半小时冰时（公共场/活动栏场/清冰/闭店） | `get_hours_and_schedule` |
| 楼层位置、怎么去、电话 | `get_location_and_contacts` |
| 任何价格问题（单次票、陪同票、私教体验、护具租赁/买断、当期活动/节假日货盘、美团/直播/团购价），以及使用规则与购票/办卡入口 | `get_ticketing_policy` |
| 储物柜、WiFi、充电宝、卫生间、休息区、停车等设施说明 | `get_facilities` |
| 教练档案（简介/经历/擅长方向）、课程体系、预约/报名入口 | `get_coaching_and_programs` |
| 常见问题 | `get_faq` |
| 最近活动、公告 | `get_news_and_promotions` |
| 预约试听、留电话回访、登记预约 | 按本文件「飞书多维表格预约登记流程」执行 |

> **价格问题一律走 `get_ticketing_policy`**：门票、陪同、护具、私教单次体验、多次卡、节假日活动价都在 `pricing.catalog` 里。不要调用 `get_coaching_and_programs` 或 `get_facilities` 去找价格。

## 飞书多维表格预约登记流程

**触发条件**：用户明确要“预约试听/留手机号让门店回电/现在就约”时，必须按本流程执行。

**执行约束**：
1. 先询问一次“是否现在预约”。
2. 用户确认后再收集手机号（11 位）。
3. 通过飞书官方 API 将预约写入多维表格，不再走点评 App 页面提交流程。
4. 写入成功后回传“已提交预约，留意门店来电”。
5. 写入失败时返回失败原因（鉴权失败、字段不匹配、限流等）并给出下一步处理建议。

**必要配置（从仓库根目录 `.env` 读取）**：
- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`
- `FEISHU_BITABLE_APP_TOKEN`
- `FEISHU_BITABLE_TABLE_ID`
- `FEISHU_BOOKING_PHONE_FIELD`（示例：`手机号`）
- 可选：`FEISHU_BOOKING_SOURCE_FIELD`、`FEISHU_BOOKING_INTENT_FIELD`、`FEISHU_BOOKING_STATUS_FIELD`

若缺任一必填配置，不执行写入，直接返回“配置缺失 + 待补配置项”。

## 盲区应对

超出 YAML 与预约登记能力的问题（如个体伤病建议、与合同/发票相关的法律结论），应：
1. 明确不编造；
2. 给出已知的官方渠道（前台、公众号、预约链接）；
3. 建议以现场公示为准。

## 品牌调性与语气

- 专业、清楚、好懂；像现场值班同事做说明。
- 有转化引导时自然带出**官方链接**，不夸大优惠。

## 维护者参考

- **YAML 路径**：`mcp_server/data/venues/`，新增场馆可复制 `shantou-mixc.yaml`。
- **默认场馆**：环境变量 `ICE_ARENA_DEFAULT_VENUE`（可选）。
- **本地 HTTP**：`ICE_ARENA_MCP_TRANSPORT=streamable-http python -m ice_arena_mcp`（在 `mcp_server` 目录、已安装依赖的前提下）。
- **性能**：数据驻留内存；水平扩展时多进程/多实例 + 前置负载均衡，注意**无状态**与 YAML 版本一致。
