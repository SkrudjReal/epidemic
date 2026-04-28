from aiogram.types import Message
from asyncmy.cursors import Cursor
from aiogram import Bot
from datetime import datetime, timedelta
from humanize import intcomma

from redis import Redis

from core.data.icons import LabIco
from core.data.tricks.stickers import stickers
from core.data.tricks.tricks_chat_manage import tricks_cm

from core.utils.db_api.repo_biowar import RequestsRepoBiowar
from core.utils.db_api.repo_chat_manage import RequestsRepoChatManage
from core.data.texttriggers import deep_links
from core.keyboards.inline.marriage import *
from core import func

import random
import asyncio


async def marriage_proposal(msg: Message, bot: Bot, redis: Redis, repo_cm: RequestsRepoChatManage, repo_biowar: RequestsRepoBiowar):
    
    check = func.check_reply_or_tag(msg)
    
    if not check:
        return

    ask_id = msg.from_user.id
    get_id = func.reply_or_tag_geeter(msg)
    chat_id = msg.chat.id

    asker, geter = await func.entity_partners_create(ask_id, get_id, repo_cm, repo_biowar)
    
    if not asker or not geter:

        user_not_found = tricks_cm['marry']['user_not_found']
        await msg.answer(user_not_found)
        return

    if msg.from_user.id == get_id:
        await msg.answer(tricks_cm['marry']['user_marry_user'].format(geter['partner2_entity']))
        return

    ask_check = await repo_cm.get_marry(chat_id, ask_id)
    get_check = await repo_cm.get_marry(chat_id, get_id)

    if not ask_check and not get_check:
        
        stickers_set = await bot.get_sticker_set(stickers['marriages_proposal_set'])
        sticker = random.choice(stickers_set.stickers).file_id
        await redis.set(f'epidemic_marry_sticker:{ask_id}_{get_id}', sticker)
        
        ask_text = tricks_cm['marry']['marry_ask'].format(geter['partner2_entity'], asker['partner1_entity'])

        await msg.answer_sticker(sticker)
        await asyncio.sleep(1)
        await msg.answer(ask_text, reply_markup = accept_marriage_action(ask_id=ask_id, get_id=get_id))
        return
    
    user_in_marry_txt = tricks_cm['marry']['marry_user_another']
    await msg.answer(user_in_marry_txt)


async def show_user_marriage(msg: Message, bot: Bot, db: Cursor, repo_cm: RequestsRepoChatManage, repo_biowar: RequestsRepoBiowar):
    chat_id = msg.chat.id
    id = msg.from_user.id

    marriage = func.go_get_user_marriage(chat_id, 1, id) 

    if not marriage:
        await msg.answer(tricks_cm['marry']['marriage_not_found'])
        return

    marriage = marriage[0] 

    text = tricks_cm['marry']['marriage_info'].format(
        f"<a href='{deep_links['mention']}{marriage['husband_id']}'>{marriage['full_name1']}</a>",
        f"<a href='{deep_links['mention']}{marriage['wife_id']}'>{marriage['full_name2']}</a>",
        marriage['time_created_formatted'], 
        marriage['duration_formatted'],
        marriage['current_anniversary']
    )
    
    await msg.answer_sticker(marriage['marry_sticker'])
    await asyncio.sleep(0.1)
    await msg.answer(text, reply_markup=my_marriage_info(id))

async def devorce_marriage(msg: Message, bot: Bot, db: Cursor, repo_cm: RequestsRepoChatManage, repo_biowar: RequestsRepoBiowar):

    chat_id = msg.chat.id
    id = msg.from_user.id

    marriage = await repo_cm.get_marry(chat_id, id)

    if not marriage:
        await msg.answer(tricks_cm['marry']['marriage_not_found'])
        return

    text = tricks_cm['marry']['devorce_button']
    await msg.answer(text, reply_markup = devorce_marriage_action(husband_id = marriage['husband_id'], wife_id = marriage['wife_id'], id = id))

async def restore_marrige_proposal(msg: Message, bot: Bot, db: Cursor, repo_cm: RequestsRepoChatManage, repo_biowar: RequestsRepoBiowar):

    chat_id = msg.chat.id
    ask_id = msg.from_user.id
    get_id = func.reply_or_tag_geeter(msg)

    asker_check = await repo_cm.get_marry(chat_id, ask_id)
    geter_check = await repo_cm.get_marry(chat_id, get_id)

    if not asker_check and not geter_check:

        backup_check = await repo_cm.get_marry_backup(chat_id, ask_id, get_id)

        asker, geter = await func.entity_partners_create(ask_id, get_id, repo_cm, repo_biowar)

        if not backup_check:
            await msg.answer(tricks_cm['marry']['comback_not_found'].format(asker['partner1_entity'], geter['partner2_entity']))
            return

        await msg.answer(tricks_cm['marry']['marry_comeback_ask'].format(geter['partner2_entity'], asker['partner1_entity']), 
        reply_markup = restore_marriage_action(ask_id, get_id))
        return
    
    user_in_marry_txt = tricks_cm['marry']['marry_user_another']
    await msg.answer(user_in_marry_txt)

async def set_marriage_description(msg: Message, bot: Bot, db: Cursor, repo_cm: RequestsRepoChatManage, repo_biowar: RequestsRepoBiowar):
    
    chat_id = msg.chat.id
    id = msg.from_user.id

    marriage = await repo_cm.get_marry(chat_id, id)
    if not marriage:
        await msg.answer(tricks_cm['marry']['marriage_not_found'])
        return

    husband, wife = await func.entity_partners_create(marriage['husband_id'], marriage['wife_id'], repo_cm, repo_biowar)

    description_text = msg.html_text[14:]

    if description_text:
        description_text = description_text
    else:
        await msg.answer(tricks_cm['marry']['marriage_description_is_not_avallible'])
        return

    if len(description_text) > 140 or len(description_text) < 5:
        await msg.answer(tricks_cm['marry']['marriage_description_is_not_avallible_len'])
        return

    await repo_cm.add_marriage_description(chat_id=chat_id, husband_id=marriage['husband_id'], wife_id=marriage['wife_id'], description_text=description_text)

    text = tricks_cm['marry']['new_marriage_comment'].format(husband['partner1_entity'], wife['partner2_entity'], description_text)
    await msg.answer(text)

async def devorce_marriage_if_leave(msg: Message, bot: Bot, db: Cursor, repo_cm: RequestsRepoChatManage, repo_biowar: RequestsRepoBiowar):
    chat_id = msg.chat.id
    leaver_id = msg.from_user.id
    
    delete = int((datetime.utcnow() + timedelta(seconds=tricks_cm['max']['time']['del_marriage_delay'])).timestamp())
    marriage = await repo_cm.get_marry(chat_id, leaver_id)
    
    # errors
    if not marriage:
        return
    
    if marriage['wife_id'] == leaver_id:
        partner_id = marriage['husband_id']
    else:
        partner_id = marriage['wife_id']

    leaver = await repo_biowar.get_user(leaver_id)
    partner = await repo_biowar.get_user(partner_id)

    leaver_entity = func.entity_create_full_name(leaver['id'], leaver['full_name'])
    partner_entity = func.entity_create_full_name(partner['id'], partner['full_name'])
    marriage_time = func.calculate_marriage(marriage)

    await repo_cm.del_marry(chat_id, leaver_id, partner_id, marriage['marry_id'], marriage['time_created'], delete, marriage['sms_in_marriage'])
    await msg.answer(tricks_cm['marry']['devorce_if_one_left'].format(partner_entity, leaver_entity, marriage_time['duration_formatted']))
