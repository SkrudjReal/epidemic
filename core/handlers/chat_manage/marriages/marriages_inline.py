from aiogram import F, types, Router, Bot
from aiogram.types import Message

from core.utils.callbackdata import (
    about_marriage_data, accept_marriage_data, reject_marriage_data, 
    accept_MarriageDevorce_data, reject_MarriageDevorce_data,
    reject_restore_marrige_data, accept_restore_marrige_data,
    close_marriage_data, top_exp_data
    )
from core.utils.genai import gpt_thinks

from redis import Redis
from datetime import datetime, timedelta

from asyncmy.cursors import Cursor

from core.utils.db_api.repo_biowar import RequestsRepoBiowar
from core.utils.db_api.repo_chat_manage import RequestsRepoChatManage

from core.data.icons import Marryico
from core.data import texttriggers as trg
from core.data.texttriggers import deep_links
from core import func
from core.keyboards.inline.marriage import *
from core.data.tricks.tricks_chat_manage import tricks_cm
from core.data.tricks.tricks_biowar import Const
from core.data.tricks.tricks_genai import tricks_genai

import random


async def accept_marriage(call: types.CallbackQuery, redis: Redis, repo_cm: RequestsRepoChatManage, repo_biowar: RequestsRepoBiowar, callback_data: accept_marriage_data):
    
    chat_id = call.message.chat.id
    time_created = datetime.utcnow().timestamp()

    ask_id = callback_data.ask_id
    get_id = callback_data.get_id

    asker, geter = await func.entity_partners_create(ask_id, get_id, repo_cm, repo_biowar)

    ask_check = await repo_cm.get_marry(chat_id, ask_id)
    get_check = await repo_cm.get_marry(chat_id, get_id)

    if not ask_check and not get_check:
        if call.from_user.id == get_id:
            
            sticker = await redis.get(f'epidemic_marry_sticker:{ask_id}_{get_id}')
            
            marry_count = await repo_cm.get_marriages_count(chat_id)
            await repo_cm.add_marry(chat_id, ask_id, get_id, time_created, marry_count + 1, sticker)
            await repo_cm.del_marry_backup(chat_id, ask_id)

            text = tricks_cm['marry']['accept_marry'].format(geter['partner2_entity'], asker['partner1_entity'], geter['partner2_entity'])
            await call.message.edit_text(text)
            return
            
        await call.answer(tricks_cm['marry']['not_user_button'])
        return

    user_in_marry_txt = tricks_cm['marry']['marry_user_another']
    await call.message.edit_text(user_in_marry_txt)

async def refuse_marriage(call: types.CallbackQuery, db: Cursor, repo_cm: RequestsRepoChatManage, repo_biowar: RequestsRepoBiowar, callback_data: reject_marriage_data):
    
    ask_id = callback_data.ask_id  
    get_id = callback_data.get_id

    asker, geter = await func.entity_partners_create(ask_id, get_id, repo_cm, repo_biowar)

    if call.from_user.id == get_id:
        await call.message.edit_text(tricks_cm['marry']['noaccept_marry'].format(asker['partner1_entity'], geter['partner2_entity']))
        return
    
    await call.answer(tricks_cm['marry']['not_user_button'])

async def accept_devorce(call: types.CallbackQuery, db: Cursor, repo_cm: RequestsRepoChatManage, repo_biowar: RequestsRepoBiowar, callback_data: accept_MarriageDevorce_data):

    chat_id = call.message.chat.id
    id = call.from_user.id

    delete = int((datetime.utcnow() + timedelta(days=tricks_cm['max']['time']['del_marriage_delay'])).timestamp())
    
    if not call.from_user.id == id:
        await call.answer(tricks_cm['marry']['not_user_button'])
        return
    
    husband_id = callback_data.husband_id
    wife_id = callback_data.wife_id
    
    marriage = func.go_get_user_marriage(chat_id, 1, id)
    marry_id = await repo_cm.get_marriages_count(chat_id)

    if not marriage:
        await call.answer(tricks_cm['marry']['marriage_not_found'])
        return

    marriage = marriage[0]

    husband, wife = await func.entity_partners_create(husband_id, wife_id, repo_cm, repo_biowar)
    # time_existed = func.calculate_marriage(marriage)

    ai_text = gpt_thinks(tricks_genai['prompts']['marriages']['marry_divorce'])

    text = tricks_cm['marry']['marry_devorce'].format(
        husband['partner1_entity'], wife['partner2_entity'],
        marriage['time_created_formatted'],
        marriage['duration_formatted'],
        ai_text
    )

    await repo_cm.del_marry(chat_id, husband_id, wife_id, marry_id, marriage['time_created'], delete, marriage['sms_in_marriage'])
    await call.message.edit_text(text)

async def refuse_devorce(call: types.CallbackQuery, db: Cursor, repo_cm: RequestsRepoChatManage, repo_biowar: RequestsRepoBiowar, callback_data: reject_MarriageDevorce_data):

    husband_id = callback_data.husband_id
    wife_id = callback_data.wife_id
    id = callback_data.id
    
    if not call.from_user.id == id:
        await call.answer(tricks_cm['marry']['not_user_button'])
        return
    
    husband, wife = await func.entity_partners_create(husband_id, wife_id, repo_cm, repo_biowar)

    await call.message.edit_text(tricks_cm['marry']['nomarry_devorce'].format(husband['partner1_entity'], wife['partner2_entity']))

async def restore_marriage_accept(call: types.CallbackQuery, redis: Redis, repo_cm: RequestsRepoChatManage, repo_biowar: RequestsRepoBiowar, callback_data: accept_restore_marrige_data):
    chat_id = call.message.chat.id
    ask_id = callback_data.ask_id
    get_id = callback_data.get_id

    asker, geter = await func.entity_partners_create(ask_id, get_id, repo_cm, repo_biowar)

    ask_check = await repo_cm.get_marry(chat_id, ask_id)
    get_check = await repo_cm.get_marry(chat_id, get_id)

    if not ask_check and not get_check:
        if call.from_user.id == get_id:
            users_backup = await repo_cm.get_marry_backup(chat_id, ask_id, get_id)

            if not users_backup:
                await call.message.edit_text(tricks_cm['marry']['comback_not_found'].format(asker['partner1_entity'], geter['partner2_entity']))
                return
            
            time_created = users_backup['time_created']
            sms_in_marriage = users_backup['sms_in_marriage']

            sticker = await redis.get(f'epidemic_marry_sticker:{ask_id}_{get_id}')

            await repo_cm.del_marry_backup(chat_id, ask_id)
            await repo_cm.del_marry_backup(chat_id, get_id)
            marry_count = await repo_cm.get_marriages_count(chat_id)
            await repo_cm.restore_marriage(chat_id, ask_id, get_id, time_created, marry_count + 1, sms_in_marriage, sticker)

            text = tricks_cm['marry']['accept_marry_restore'].format(geter['partner2_entity'], asker['partner1_entity'], geter['partner2_entity'])
            await call.message.edit_text(text)
            return

        await call.answer(tricks_cm['marry']['not_user_button'])
        return

    user_in_marry_txt = tricks_cm['marry']['marry_user_another']
    await call.message.edit_text(user_in_marry_txt)

async def restore_marriage_refuse(call: types.CallbackQuery, db: Cursor, repo_cm: RequestsRepoChatManage, repo_biowar: RequestsRepoBiowar, callback_data: reject_restore_marrige_data):
    ask_id = callback_data.ask_id
    get_id = callback_data.get_id

    if not call.from_user.id == get_id:
        await call.answer(tricks_cm['marry']['not_user_button'])
        return

    asker, geter = await func.entity_partners_create(ask_id, get_id, repo_cm, repo_biowar)

    if call.from_user.id == get_id:
        await call.message.edit_text(tricks_cm['marry']['noaccept_marry_restore'].format(asker['partner1_entity'], geter['partner2_entity']))
        return

async def close_marriage_info(call: types.callback_query, callback_data: close_marriage_data):
    
    id = callback_data.id
    
    if not call.from_user.id == id:
        await call.answer(tricks_cm['marry']['not_user_button'])
        return

    await call.message.delete()


async def my_marriage_make_poem(call: types.callback_query, callback_data: MyMarriageInfo, repo_cm: RequestsRepoChatManage, repo_biowar: RequestsRepoBiowar, redis: Redis):
    
    id = callback_data.id
    
    next_time_poem = await redis.get(f'marriage_poem_time:{id}')
    marriage = await repo_cm.get_marry(call.message.chat.id, id)
    husband, wife = await func.entity_partners_create(marriage['husband_id'], marriage['wife_id'], repo_cm, repo_biowar)
    
    # errors
    if not call.from_user.id == id:
        return await call.answer(tricks_cm['marry']['not_user_button'])
    if next_time_poem and datetime.fromtimestamp(float(next_time_poem)) > datetime.utcnow():
        next_time_poem = func.diff_convert_timestamp_to_human(float(next_time_poem))
        return await call.answer(tricks_cm['marry']['next_time_poem'].format(next_time_poem))

    next_time_poem = (datetime.utcnow() + timedelta(hours=12)).timestamp()

    poem_text = gpt_thinks(tricks_genai['prompts']['marriages']['make_poem'])
    poem_text = f'<blockquote>💞 {poem_text}</blockquote>\n🩷— {husband["partner1_entity"]} —&gt💞&lt— {wife['partner2_entity']} —🩷'
    await redis.set(f'marriage_poem_time:{id}', next_time_poem)
    
    await call.message.answer(poem_text, reply_markup=heart())
    await call.answer()

async def marriage_heart(call: types.callback_query, callback_data: MarriageHeart):
    
    heart = random.choice(Const.HEARTS)
    
    await call.answer(heart)