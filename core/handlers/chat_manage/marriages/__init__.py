from aiogram import Router, F
from aiogram.filters.chat_member_updated import (
    ChatMemberUpdatedFilter, JOIN_TRANSITION, LEAVE_TRANSITION
)
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, Command
from aiogram.enums import ChatType
from core.utils.callbackdata import (
    about_marriage_data, accept_marriage_data, reject_marriage_data, 
    accept_MarriageDevorce_data, reject_MarriageDevorce_data,
    reject_restore_marrige_data, accept_restore_marrige_data,
    close_marriage_data, top_marriages_data, top_exp_data, top_sms_data,
    MyMarriageInfo, MarriageHeart
    )

from core.data import texttriggers as trg
from .shiper import shiper
from .marriages import ( 
    marriage_proposal, show_user_marriage, devorce_marriage,
    set_marriage_description, restore_marrige_proposal,
    devorce_marriage_if_leave
)

from .marriages_inline import ( accept_marriage, refuse_marriage, accept_devorce,
    refuse_devorce, restore_marriage_accept, restore_marriage_refuse,
    close_marriage_info, my_marriage_make_poem, marriage_heart
)

from .top_marriages  import top_marriages_exp, top_marriages_sms, top_marriages_time
from .top_marriages_inline import top_marriages_exp_inline, top_marriages_time_inline, top_marriages_sms_inline

marriages_router = Router()

# Marriages

marriages_router.message.register(marriage_proposal, F.text.regexp(trg.re_marry, mode='fullmatch') & (F.chat.type != 'private'))
marriages_router.message.register(top_marriages_time, F.text.regexp(trg.re_show_chat_marry, mode='fullmatch') & (F.chat.type != 'private'))

marriages_router.message.register(devorce_marriage, F.text.regexp(trg.re_marry_devorce, mode='fullmatch') & (F.chat.type != 'private'))
marriages_router.message.register(show_user_marriage, F.text.regexp(trg.re_show_marry, mode='fullmatch') & (F.chat.type != 'private'))

marriages_router.message.register(restore_marrige_proposal, F.text.regexp(trg.re_marry_restore, mode='fullmatch') & (F.chat.type != 'private'))
marriages_router.message.register(set_marriage_description, F.text.regexp(trg.re_marriage_comment, mode='fullmatch') & (F.chat.type != 'private'))

marriages_router.message.register(top_marriages_sms, F.text.regexp(trg.re_marriages_top_sms, mode='fullmatch') & (F.chat.type != 'private'))
marriages_router.message.register(top_marriages_exp, F.text.regexp(trg.re_marriages_top_exp, mode='fullmatch') & (F.chat.type != 'private'))

 # Marriages inline
marriages_router.callback_query.register(restore_marriage_accept, accept_restore_marrige_data.filter(F.skill.startswith('accept_restore_')))
marriages_router.callback_query.register(restore_marriage_refuse, reject_restore_marrige_data.filter(F.skill.startswith('reject_restore_')))

marriages_router.callback_query.register(accept_marriage, accept_marriage_data.filter(F.skill.startswith('accept_marriage_')))
marriages_router.callback_query.register(refuse_marriage, reject_marriage_data.filter(F.skill.startswith('reject_marriage_')))

marriages_router.callback_query.register(close_marriage_info, close_marriage_data.filter(F.skill.startswith('close_mar_action_')))

marriages_router.callback_query.register(accept_devorce, accept_MarriageDevorce_data.filter(F.skill.startswith('accept_devorce_')))
marriages_router.callback_query.register(refuse_devorce, reject_MarriageDevorce_data.filter(F.skill.startswith('reject_devorce_')))

marriages_router.callback_query.register(top_marriages_time_inline, top_marriages_data.filter(F.skill.startswith('top_marriages_')))
marriages_router.callback_query.register(top_marriages_exp_inline, top_exp_data.filter(F.skill.startswith('top_exp_')))
marriages_router.callback_query.register(top_marriages_sms_inline, top_sms_data.filter(F.skill.startswith('top_sms_')))

marriages_router.callback_query.register(my_marriage_make_poem, MyMarriageInfo.filter(F.action=='стих'))
marriages_router.callback_query.register(marriage_heart, MarriageHeart.filter(F.action=='heart'))

# Shiper
marriages_router.message.register(shiper,  F.text.regexp(trg.re_ship, mode='fullmatch'))