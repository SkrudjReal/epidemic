from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.utils.callbackdata import (
    about_marriage_data, accept_marriage_data, reject_marriage_data, 
    accept_MarriageDevorce_data, reject_MarriageDevorce_data,
    reject_restore_marrige_data, accept_restore_marrige_data,
    close_marriage_data, top_marriages_data, top_exp_data, top_sms_data,
    MyMarriageInfo, MarriageHeart
    )

from core.data.tricks.tricks_chat_manage import tricks_cm

def accept_marriage_action(ask_id: int, get_id: int):
    kb = InlineKeyboardBuilder()
    
    kb.button(text=tricks_cm['marry']['confirm_accept_button'], callback_data=accept_marriage_data(skill = 'accept_marriage_', ask_id = ask_id, get_id = get_id))
    kb.button(text=tricks_cm['marry']['nocomfirm_accept_button'], callback_data=reject_marriage_data(skill = 'reject_marriage_', ask_id = ask_id, get_id = get_id))
   
    kb.adjust(2)
    return kb.as_markup()

def show_about_marriage(husband_id: int, wife_id: int):
    kb = InlineKeyboardBuilder()
    kb.button(text=tricks_cm['marry']['about_marry_button'], callback_data=about_marriage_data(skill = 'about_marriage_', husband_id = husband_id, wife_id = wife_id))
    kb.adjust(1)
    return kb.as_markup()

def devorce_marriage_action(husband_id: int, wife_id: int, id: int):
    kb = InlineKeyboardBuilder()

    kb.button(text=tricks_cm['marry']['nodevorce_marry_button'], callback_data=reject_MarriageDevorce_data(skill = 'reject_devorce_', husband_id = husband_id, wife_id = wife_id, id = id))
    kb.button(text=tricks_cm['marry']['devorce_marry_button'], callback_data=accept_MarriageDevorce_data(skill = 'accept_devorce_', husband_id = husband_id, wife_id = wife_id, id = id))
    kb.adjust(2)

    return kb.as_markup()

def restore_marriage_action(ask_id: int, get_id: int):
    kb = InlineKeyboardBuilder()
    
    kb.button(text=tricks_cm['marry']['confirm_comeback_button'], callback_data=accept_restore_marrige_data(skill = 'accept_restore_', ask_id = ask_id, get_id = get_id))
    kb.button(text=tricks_cm['marry']['nocomfirm_comeback_button'], callback_data=reject_restore_marrige_data(skill = 'reject_restore_', ask_id = ask_id, get_id = get_id))
   
    kb.adjust(2)
    return kb.as_markup()

def close_action(id: int):
    kb = InlineKeyboardBuilder()

    kb.button(text=tricks_cm['marry']['close_button'], callback_data=close_marriage_data(skill = 'close_mar_action_', id = id))
    
    kb.adjust(1)
    return kb.as_markup()

def top_buttons(status: int, id: int):
    kb = InlineKeyboardBuilder()

    if status == 1:

        kb.button(text=tricks_cm['marry']['marriage_sms_top_button'], callback_data=top_sms_data(skill = 'top_sms_', status = status, id = id))
        kb.button(text=tricks_cm['marry']['marriage_exp_top_button'], callback_data=top_exp_data(skill = 'top_exp_', status = status, id = id))
        
        kb.adjust(1)
        return kb.as_markup(resize_keyboard=True)

    elif status == 2:

        kb.button(text=tricks_cm['marry']['marriage_sms_top_button'], callback_data=top_sms_data(skill = 'top_sms_', status = status, id = id))
        kb.button(text=tricks_cm['marry']['marriages_button'], callback_data=top_marriages_data(skill = 'top_marriages_', status = status, id = id))
      
        kb.adjust(1)
        return kb.as_markup(resize_keyboard=True)
    
    elif status == 3:
        
        kb.button(text=tricks_cm['marry']['marriages_button'], callback_data=top_marriages_data(skill = 'top_marriages_', status = status, id = id))
        kb.button(text=tricks_cm['marry']['marriage_exp_top_button'], callback_data=top_exp_data(skill = 'top_exp_', status = status, id = id))

        kb.adjust(1)
        return kb.as_markup(resize_keyboard=True)

def my_marriage_info(id: int):
    
    kb = InlineKeyboardBuilder()
    
    kb.button(text='Составить стих', callback_data=MyMarriageInfo(id=id, action='стих'))
   
    kb.adjust(1)
    return kb.as_markup()

def heart():
    
    kb = InlineKeyboardBuilder()
    
    kb.button(text='❤️', callback_data=MarriageHeart(action='heart'))
   
    kb.adjust(1)
    return kb.as_markup()