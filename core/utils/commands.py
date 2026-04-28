from aiogram.types import (
    BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats,
    BotCommandScopeDefault
)
from aiogram import Bot


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command = 'start',
            description = 'Запустить бота'
        ),
        BotCommand(
            command = 'help',
            description = '🦠 Помощь по командам'
        ),
        BotCommand(
            command = 'donate',
            description = '✨ Покупка доната'
        ),
        BotCommand(
            command = 'paysupport',
            description = 'Помощь с покупками'
        ),
        BotCommand(
            command = 'refund',
            description = 'Возврат платежа(рефанд)'
        ),
    ]
    commands1 = [
        BotCommand(
            command = 'donate',
            description = '✨ Покупка доната'
        )
    ]
    
    await bot.set_my_commands(commands1, BotCommandScopeAllGroupChats())
    await bot.set_my_commands(commands, BotCommandScopeAllPrivateChats())


async def del_commands(bot: Bot):
    
    await bot.delete_my_commands(BotCommandScopeAllGroupChats())
    await bot.delete_my_commands(BotCommandScopeAllPrivateChats())