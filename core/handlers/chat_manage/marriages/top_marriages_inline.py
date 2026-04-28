from aiogram import F, types, Router, Bot
from aiogram.types import Message

from core.utils.callbackdata import (
    about_marriage_data, accept_marriage_data, reject_marriage_data, 
    accept_MarriageDevorce_data, reject_MarriageDevorce_data,
    reject_restore_marrige_data, accept_restore_marrige_data,
    close_marriage_data, top_exp_data
    )

from datetime import datetime, timedelta

from asyncmy.cursors import Cursor

from core.utils.db_api.repo_biowar import RequestsRepoBiowar
from core.utils.db_api.repo_chat_manage import RequestsRepoChatManage

from core.data.icons import Marryico
from core.data import texttriggers as trg
from core.data.texttriggers import deep_links
from core.data.icons import LabIco, Marryico
from core import func
from core.keyboards.inline.marriage import *
from core.data.tricks.tricks_chat_manage import tricks_cm

async def top_marriages_sms_inline(call: types.CallbackQuery, db: Cursor, repo_cm: RequestsRepoChatManage, repo_biowar: RequestsRepoBiowar, callback_data: top_sms_data):
    
    chat_id = call.message.chat.id
    id = callback_data.id

    if not call.from_user.id == id:
        await call.answer(tricks_cm['marry']['not_user_button'])
        return

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
    await call.message.edit_text(text, reply_markup=top_buttons(status=3, id=id))

async def top_marriages_time_inline(call: types.CallbackQuery, db: Cursor, repo_cm: RequestsRepoChatManage, repo_biowar: RequestsRepoBiowar, callback_data: top_marriages_data):
    
    chat_id = call.message.chat.id
    id = callback_data.id

    if not call.from_user.id == id:
        await call.answer(tricks_cm['marry']['not_user_button'])
        return

    marry_chat_members = func.go_get_top_marriage(chat_id, 1)

    if not marry_chat_members:
        await msg.answer(tricks_cm['marry']['chat_marry_not_found'])
        return

    marriages_message = "\n".join(
        f"{index}. <a href='{deep_links['mention']}{info['husband_id']}'>{info['full_name1']}</a> + "
        f"<a href='{deep_links['mention']}{info['wife_id']}'>{info['full_name2']}</a> — "
        f"{info['duration_formatted']}" 
        for index, info in enumerate(marry_chat_members, 1)
    )

    text = tricks_cm['marry']['chat_marriages'].format(marriages_message)
    await call.message.edit_text(text, reply_markup=top_buttons(status=1, id=id))

async def top_marriages_exp_inline(call: types.CallbackQuery, db: Cursor, repo_cm: RequestsRepoChatManage, repo_biowar: RequestsRepoBiowar, callback_data: top_exp_data):
   
    chat_id = call.message.chat.id
    id = callback_data.id

    if not call.from_user.id == id:
        await call.answer(tricks_cm['marry']['not_user_button'])
        return

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
    await call.message.edit_text(text, reply_markup=top_buttons(status=2, id=id))