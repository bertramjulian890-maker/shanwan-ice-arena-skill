from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from ice_arena_mcp.store import get_store

READ_ONLY = ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=False,
)

mcp = FastMCP(
    name="shanwan-ice-arena-mcp",
    instructions=(
        "汕头万象城冰场官方信息查询工具。"
        "回答票价、时间、位置、教练、课程、预约/办卡链接等，一律以工具返回的 JSON 为准，勿编造。"
    ),
)


def _store():
    return get_store()


@mcp.tool(annotations=READ_ONLY)
def list_venues() -> dict[str, Any]:
    """列出当前已加载的场馆 venue_id（用于确认当前配置是否生效）。"""
    s = _store()
    return {"venues": s.list_venue_ids()}


@mcp.tool(annotations=READ_ONLY)
def get_venue_overview(venue_id: str | None = None) -> dict[str, Any]:
    """场馆概览：名称、简介、面向用户的消费引导说明、合规提示摘要。"""
    return _store().section(venue_id, "overview")


@mcp.tool(annotations=READ_ONLY)
def get_hours_and_schedule(venue_id: str | None = None) -> dict[str, Any]:
    """营业时间、清冰时段说明，以及分日半小时粒度的 dynamic_schedule（公共场/活动栏场/清冰/闭店）。"""
    return _store().section(venue_id, "hours")


@mcp.tool(annotations=READ_ONLY)
def get_location_and_contacts(venue_id: str | None = None) -> dict[str, Any]:
    """位置（含楼层/动线）、交通方式、前台与业务联系电话。"""
    return _store().section(venue_id, "location_and_contacts")


@mcp.tool(annotations=READ_ONLY)
def get_ticketing_policy(venue_id: str | None = None) -> dict[str, Any]:
    """门票/护具/会员/私教体验等所有在售货盘（pricing.catalog 为唯一价格源），外加使用规则与购票/办卡入口。"""
    s = _store()
    ticketing = s.section(venue_id, "ticketing")
    if isinstance(ticketing, dict):
        ticketing["pricing"] = s.section(venue_id, "pricing", redact=True)
    return ticketing


@mcp.tool(annotations=READ_ONLY)
def get_facilities(venue_id: str | None = None) -> dict[str, Any]:
    """场馆设施说明：储物柜/WiFi/充电宝/卫生间/休息区/停车等。护具租赁与寄存收费如有，走 get_ticketing_policy 的 pricing.catalog。"""
    return _store().section(venue_id, "facilities")


@mcp.tool(annotations=READ_ONLY)
def get_coaching_and_programs(venue_id: str | None = None) -> dict[str, Any]:
    """教练档案（coaching.coaches）与课程体系（programs），以及教练/课程预约入口。私教单次价请走 get_ticketing_policy 的 pricing.catalog。"""
    s = _store()
    return {
        "venue_id": s.get_raw(venue_id).get("venue_id"),
        "display_name": s.get_raw(venue_id).get("display_name"),
        "coaching": s.section(venue_id, "coaching", redact=True),
        "programs": s.section(venue_id, "programs", redact=True),
    }


@mcp.tool(annotations=READ_ONLY)
def get_faq(venue_id: str | None = None) -> dict[str, Any]:
    """高频 FAQ 与标准答复。"""
    return _store().section(venue_id, "faq")


@mcp.tool(annotations=READ_ONLY)
def get_news_and_promotions(venue_id: str | None = None) -> dict[str, Any]:
    """活动/公告/限时优惠（按需更新）。"""
    return _store().section(venue_id, "news")
