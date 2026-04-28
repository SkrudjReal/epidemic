from aiogram.types import Message
from asyncmy.cursors import Cursor
from aiogram import Bot
from datetime import datetime, timedelta
from core.data.icons import LabIco, Marryico
from humanize import intcomma
from core.utils.db_api.repo_biowar import RequestsRepoBiowar
from core.utils.db_api.repo_chat_manage import RequestsRepoChatManage
from core.data.texttriggers import deep_links
from core.keyboards.inline.marriage import *
from core.data.tricks.tricks_chat_manage import tricks_cm
from core import func

async def top_marriages_exp(msg: Message, bot: Bot, db: Cursor, repo_cm: RequestsRepoChatManage, repo_biowar: RequestsRepoBiowar):
    chat_id = msg.chat.id
    id = msg.from_user.id

    marry_chat_members = func.go_get_top_marriage(chat_id, 3)

    if not marry_chat_members:
        await msg.answer(tricks_cm['marry']['chat_marry_not_found'])
        return

    marriages_message = "\n".join(
        f"{index}. <a href='{deep_links['mention']}{info['husband_id']}'>{info['full_name1']}</a> + "
        f"<a href='{deep_links['mention']}{info['wife_id']}'>{info['full_name2']}</a> — "
        f"{LabIco.bio_experience.value} {info['bio_experience1'] + info['bio_experience2']} био-опыта" 
        for index, info in enumerate(marry_chat_members, 1)
    )

    text = tricks_cm['marry']['marriage_top_exp'].format(marriages_message)
    await msg.answer(text=text, reply_markup=top_buttons(status=2, id=id))

async def top_marriages_sms(msg: Message, bot: Bot, db: Cursor, repo_cm: RequestsRepoChatManage, repo_biowar: RequestsRepoBiowar):

    chat_id = msg.chat.id
    id = msg.from_user.id

    marry_chat_members = func.go_get_top_marriage(chat_id, 2)

    if not marry_chat_members:
        await msg.answer(tricks_cm['marry']['chat_marry_not_found'])
        return

    marriages_message = "\n".join(
        f"{index}. <a href='{deep_links['mention']}{info['husband_id']}'>{info['full_name1']}</a> + "
        f"<a href='{deep_links['mention']}{info['wife_id']}'>{info['full_name2']}</a> — "
        f"{Marryico.con} {info['marriage_sms']} смс" 
        for index, info in enumerate(marry_chat_members, 1)
    )

    text = tricks_cm['marry']['marriage_top_sms'].format(marriages_message)
    await msg.answer(text=text, reply_markup=top_buttons(status=3, id=id))

async def top_marriages_time(msg: Message, bot: Bot, db: Cursor, repo_cm: RequestsRepoChatManage, repo_biowar: RequestsRepoBiowar):
    
    chat_id = msg.chat.id
    id = msg.from_user.id

    marry_chat_members = func.go_get_top_marriage(chat_id, 1)

    if not marry_chat_members:
        await msg.answer(tricks_cm['marry']['chat_marry_not_found'])
        return
    # 1. [Юзер1] + [Юзер2]  — Время
    marriages_message = "\n".join(
        f"{index}. <a href='{deep_links['mention']}{info['husband_id']}'>{info['full_name1']}</a> + "
        f"<a href='{deep_links['mention']}{info['wife_id']}'>{info['full_name2']}</a> — "
        f"{info['duration_formatted']}" 
        for index, info in enumerate(marry_chat_members, 1)
    )

    text = tricks_cm['marry']['chat_marriages'].format(marriages_message)

    await msg.answer(text, reply_markup=top_buttons(status=1, id=id))
