from aiogram import Router,F
from aiogram.filters import Command
from aiogram.enums import ChatType

from core.data import texttriggers as trg
from core.utils.callbackdata import DonateList, DonateListCrypto, PetsGlobalListChoose
from core.filters import IsAdminFilter

from .donate import (
    donate, donate_inline, donate_send,
    donate_crypto, donate_successful_payment, donate_on_pre_checkout_query,
    paysupport, donate_refund, donate_send_crypto,
)
from .bag import (
    get_bag, send_currency, convert_stellar_jade_to_primo, convert_stellar_jade_to_bio_resource,
    convert_primogem_to_bio_resource
)
from .promo_code import promo_code_use, promo_code_show
from .krutki import krutka, garant_choice, my_pets_garant_choose

donate_router = Router()

# Donate
donate_router.message.register(donate, Command('donate'))
donate_router.callback_query.register(donate_crypto, DonateList.filter(F.action == 'donate_crypto_menu'))
donate_router.callback_query.register(donate_inline, DonateListCrypto.filter(F.action == 'donate_main_menu'))
donate_router.callback_query.register(donate_send, DonateList.filter(F.action == 'donate'))
donate_router.callback_query.register(donate_send_crypto, DonateListCrypto.filter(F.action == 'donate_crypto'))
donate_router.pre_checkout_query.register(donate_on_pre_checkout_query)
donate_router.message.register(donate_successful_payment, F.successful_payment)
donate_router.message.register(paysupport, Command('paysupport'), F.chat.type == ChatType.PRIVATE)
donate_router.message.register(donate_refund, Command('refund'), F.chat.type == ChatType.PRIVATE)

# Bag
donate_router.message.register(get_bag, F.text.regexp(trg.get_bag, mode='fullmatch'))
donate_router.message.register(send_currency, F.text.regexp(trg.re_bag_send_currency, mode='fullmatch'))
donate_router.message.register(convert_stellar_jade_to_primo, F.text.lower().startswith("эписвап "))
donate_router.message.register(convert_stellar_jade_to_bio_resource, F.text.lower().startswith("нефритсвап "))
donate_router.message.register(convert_primogem_to_bio_resource, F.text.lower().startswith("примосвап "))

# Promo codes
donate_router.message.register(promo_code_use, F.text.regexp(trg.re_promo_code_use, mode='fullmatch'))
donate_router.message.register(promo_code_show, F.text.regexp(trg.re_show_promo_codes, mode='fullmatch'), IsAdminFilter())

# Krutki
donate_router.message.register(krutka, F.text.regexp(trg.re_krutka, mode='fullmatch'))
donate_router.message.register(garant_choice, F.text.regexp(trg.re_krutka_garant_choice, mode='fullmatch'))
donate_router.callback_query.register(my_pets_garant_choose, PetsGlobalListChoose.filter(F.action == 'g_pet_choose'))
