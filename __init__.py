from typing import Union

from nonebot import get_plugin_config, on_command
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    MessageSegment,
    PrivateMessageEvent,
)
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="check-mp",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

rule = on_command("cmp")

import asyncio


async def tcp_port_check(host: str, port: int) -> bool:
    for _ in range(3):
        try:
            _, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port), timeout=5
                )
            writer.close()
            await writer.wait_closed()
            return True  # noqa: TRY300
        except(TimeoutError, ConnectionRefusedError, ConnectionAbortedError, ConnectionResetError, OSError):  # noqa: E501, PERF203
            continue
    return False

@rule.handle()
async def _(bot: Bot, event: Union[PrivateMessageEvent, GroupMessageEvent]):
    result = await tcp_port_check("yee.autos", 2000)
    await bot.send(
        event,
        MessageSegment.reply(event.message_id) +
        MessageSegment.at(event.get_user_id()) +
        MessageSegment.text("稍等一下喵~")
        )
    if result:
        await rule.finish(
        MessageSegment.reply(event.message_id) +
        MessageSegment.at(event.get_user_id()) +
        MessageSegment.text("✅ 服务器 yee.autos:2000 可用")
        )
    await rule.finish(
        MessageSegment.reply(event.message_id) +
        MessageSegment.at(event.get_user_id()) +
        MessageSegment.text("❌ 3 次尝试均失败，服务器不可用")
        )
