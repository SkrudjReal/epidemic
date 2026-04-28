from aiogram.types import Message
from asyncmy.cursors import Cursor
from aiogram import Bot
from datetime import datetime, timedelta
from humanize import intcomma

from core.utils.db_api.repo_biowar import RequestsRepoBiowar
from core.utils.db_api.repo_chat_manage import RequestsRepoChatManage

from core.data.tricks.tricks_chat_manage import tricks_cm
from core.data.tricks.stickers import stickers
from core import func

import random
import asyncio

async def shiper(msg: Message, bot: Bot, db: Cursor, repo_cm: RequestsRepoChatManage, repo_biowar: RequestsRepoBiowar):
    
    chat_id = msg.chat.id
    time = datetime.utcnow().timestamp()
    check = await repo_cm.get_shipper_check(chat_id)

    if check is not None:
        if check["time_shiped"] != 0 and check["time_shiped"] > datetime.utcnow().timestamp():

            alredy_partner1_id = check['partner1_id']
            alredy_partner2_id = check['partner2_id']

            alredy1 = await repo_biowar.get_user(alredy_partner1_id)
            alredy2 = await repo_biowar.get_user(alredy_partner2_id)

            partner1_entity = func.entity_create_consider_username(alredy1)
            partner2_entity = func.entity_create_consider_username(alredy2)
            
            time_shipped = func.diff_convert_timestamp_to_human(check["time_shiped"])
            
            text = tricks_cm['shiper']['para_alredy_chosed'].format(partner1_entity, partner2_entity, time_shipped)
            
            return await msg.answer(text, disable_web_page_preview=True)

    mem = await repo_cm.get_shipper(chat_id)

    if len(mem) >= 2:
        next_ship_time = (datetime.utcnow() + timedelta(hours=4)).timestamp()
        partner1_id = mem[0]['user_id']
        partner2_id = mem[1]['user_id']

        partner1_entity = func.entity_create_consider_username(mem[0])
        partner2_entity = func.entity_create_consider_username(mem[1])
        
        if partner1_id == partner2_id or not partner2_id:
            return await msg.answer(tricks_cm['shiper']['error_found'])
        
        chat_users = await repo_biowar.get_chat_users_count(chat_id)
        
        stickers_set = await bot.get_sticker_set(stickers['epilove_set'])
        
        text = tricks_cm['shiper']['para_chosed'].format(partner1_entity, partner2_entity)
        sticker = random.choice(stickers_set.stickers).file_id
        
        if chat_users >= 8:
            await repo_biowar.create_valentinka_column(msg.from_user.id)
            await repo_biowar.update_epilove_count(msg.from_user.id)
            await repo_biowar.update_bag_primogem(partner1_id, 15, '+')
            await repo_biowar.update_bag_primogem(partner2_id, 15, '+')
        
        await msg.answer_sticker(sticker)
        await asyncio.sleep(0.1)
        await msg.answer(text, disable_web_page_preview=True)
        await repo_cm.add_ship(chat_id, partner1_id, partner2_id, next_ship_time)
    else:
        await msg.answer(tricks_cm['shiper']['error_found'])