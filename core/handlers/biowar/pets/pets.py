from aiogram.types import Message, CallbackQuery
from asyncmy.cursors import Cursor
from aiogram import Bot

from redis import Redis

from core.utils.db_api.repo_biowar import RequestsRepoBiowar
from core.data.texttriggers import deep_links
from core.data.tricks.tricks_biowar import tricks_biowar
from core.data.icons import LabIco, OtherIco, PetIco
from core.data.tricks.stickers import stickers
from core.keyboards.inline.pets import pets_list_nav
from core.utils.callbackdata import PetsListChoose

from core import func

from humanize import intcomma
import asyncio

async def my_pet(msg: Message, bot: Bot, redis: Redis, repo_biowar: RequestsRepoBiowar):
    
    id = msg.from_user.id
    
    pet = await repo_biowar.get_my_pet(id)
    
    # errors
    if not pet:
        return await msg.answer(tricks_biowar['pet']['hasnt_pet'], disable_web_page_preview=True)
    
    pet_name = pet['pet_name'].lower()
    happy_emoji = func.pet_current_happy_emoji(pet['happy'])
    
    pet_info = tricks_biowar['pet']['pets_info'][pet_name]
    text = tricks_biowar['pet']['get_my_pet'].format(
        pet_info['emoji'], pet['pet_name'].title(), pet_info['element_emoji'],
        pet_info['element'], happy_emoji, pet['happy'],
        '<i>' + pet_info['skill'] + '</i>',
        '<blockquote><i>' + pet_info['description'] + '</i></blockquote>'
    )
    
    pet_msg = await msg.answer_sticker(stickers['pet'][pet_name])
    
    await redis.set(f'epidemic_pet_owner_msg:{msg.chat.id}:{pet_msg.message_id}', id)
    await asyncio.sleep(0.1)

    await msg.answer(text)

async def my_pets(msg: Message, redis: Redis, repo_biowar: RequestsRepoBiowar):

    user = msg.from_user
    pets = await repo_biowar.get_my_pets(user.id)

    text = tricks_biowar['pet']['get_my_pets']

    # errors
    if not pets:
        return await msg.answer(tricks_biowar['pet']['hasnt_pet'], disable_web_page_preview=True)

    await msg.answer(text, reply_markup=pets_list_nav(user.id, pets))

async def my_pets_choose(call: CallbackQuery, callback_data: PetsListChoose, repo_biowar: RequestsRepoBiowar):
    
    user = call.from_user
    pet = callback_data.pet.lower()
    pet_emoji = tricks_biowar['pet']['pets_info'][pet]['emoji']
    
    # errors
    if user.id != callback_data.user_id:
        return await call.answer('Не для тебя моя кнопочка росла')
    
    await repo_biowar.change_current_pet(user.id, pet)
    await call.answer(f'{pet_emoji} Вы изменили вашего питомца на {pet}')