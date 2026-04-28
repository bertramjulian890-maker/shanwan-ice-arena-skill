# mcp_server 内部说明

该目录用于本地 MCP 服务运行（非用户文档）。

## 最小启动步骤

```bash
cd mcp_server
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
ICE_ARENA_MCP_TRANSPORT=stdio python -m ice_arena_mcp
```

如需 HTTP：

```bash
ICE_ARENA_MCP_TRANSPORT=streamable-http ICE_ARENA_MCP_HOST=127.0.0.1 ICE_ARENA_MCP_PORT=8710 python -m ice_arena_mcp
```

## 当前场馆数据

- `data/venues/shantou-mixc.yaml`

更新 YAML 后，重启 MCP 进程（或让客户端重连）即可生效。

## 关键环境变量

- `ICE_ARENA_DATA_DIR`
- `ICE_ARENA_DEFAULT_VENUE`
- `ICE_ARENA_MCP_TRANSPORT`
- `ICE_ARENA_MCP_HOST`
- `ICE_ARENA_MCP_PORT`
- `ICE_ARENA_MCP_JSON_RESPONSE`
