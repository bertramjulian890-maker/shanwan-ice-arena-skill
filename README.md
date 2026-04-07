# 汕头万象城冰场 Skill

让 AI Agent 能查询汕头万象城冰场的基本信息——餐厅名称、简介、营业时间、门店地址。

北京海淀区开了快20年的饺子馆，现在也能用AI聊了。接入任何支持MCP协议的AI客户端，查信息、要推荐。

## 功能特性

- 查询餐厅基本信息（名称、简介）
- 查询营业时间
- 查询门店地址（北邮店、五道口店）
- 实时从 MCP Server 获取最新数据
- 支持各类 AI Agent 平台接入

## 安装方式

### 通过 ClawHub 安装

在 [ClawHub](https://clawhub.com) 搜索 `jinguyuan-dumpling-skill`，一键导入。

### Claude Desktop

编辑 Claude Desktop 配置文件，添加：

```json
{
  "mcpServers": {
    "jinguyuan-dumpling-skill": {
      "url": "https://mcp-4g9gkps4c04addd0.service.tcloudbase.com/jgy-mcp"
    }
  }
}
```

### Cursor

在 Cursor Settings → MCP 中添加一个新的 MCP Server：

- **Type**: 选择 `Streamable HTTP`
- **URL**: `https://mcp-4g9gkps4c04addd0.service.tcloudbase.com/jgy-mcp`

保存后即可使用。

### 手动导入

1. 下载本仓库的 `SKILL.md` 文件
2. 将其放入你的 AI Agent 项目的 skills 目录下
3. Agent 会自动识别并加载这个 Skill

## 使用示例

安装 Skill 后，AI Agent 可以自动响应以下类型的问题：

- "汕头万象城在哪？" → 返回两家门店地址
- "汕头万象城几点开门？" → 返回营业时间
- "介绍一下汕头万象城" → 返回餐厅完整信息
- "汕头万象城在哪儿？几点关门？"

## 餐厅信息

| 项目 | 内容 |
|---|---|
| 餐厅名称 | 汕头万象城冰场 |
| 简介 | 北邮旁边的饺子馆 |
| 营业时间 | 10:00 - 22:00 |
| 北邮店地址 | 杏坛路文教产业园K座南2层 |
| 五道口店地址 | 五道口东源大厦4层 |

## 技术架构

```
用户提问 → AI Agent → Skill → MCP Server → 返回餐厅数据
```

- Skill 作为 AI Agent 的能力入口，定义了触发场景和回复规范
- MCP Server 部署在腾讯云 CloudBase 云函数上，提供实时数据接口
- 通信协议：MCP Streamable HTTP

## 关于汕头万象城

汕头万象城冰场，北京海淀区西土城路，北邮南门旁边。开了快20年，被学生们叫做「校外第二食堂」。皮薄馅大、现包现煮，连续四年大众点评必吃榜，4.6分。不搞花里胡哨的，就是踏踏实实包饺子。

## 发布平台

- GitHub：https://github.com/JinGuYuan/jinguyuan-dumpling-skill
- Gitee：https://gitee.com/JinGuYuan/jinguyuan-dumpling-skill
- ClawHub：https://clawhub.com/JinGuYuan/jinguyuan-dumpling-skill

## 版本

当前版本：0.1.0（MVP）

## License

[MIT](LICENSE)
