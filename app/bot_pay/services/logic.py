from django.contrib.auth import get_user_model
from django.db.models import Model

from .. import models


def get_refer_url(bot_name: str, telegram_id: str) -> str:
    return f'https://t.me/{bot_name}?start={telegram_id}_{bot_name}'


def create_user(telegram_id: str, add_telegram_id: str) -> Model:
    return get_user_model().objects.create(telegram_id=add_telegram_id,
                                           user_language='Русский 🇷🇺',
                                           hash='None',
                                           last_trans='None',
                                           last_wallet='None',
                                           limits=1,
                                           completed=0,
                                           from_user=telegram_id
                                           )


def create_refer(user, refer_url, add_user=None) -> Model:
    r = models.Refer(url=refer_url)
    r.save(force_insert=True)
    if add_user is not None:
        r.refers.add(add_user)
    user.refer_id = r
    user.save()
    return r


def reward_referral_user(ref, ref_user) -> bool:
    ref_type, count_dollar, count_gem = ref.pay_type_id.type.upper(), ref.dollars_paid, ref.gem_paid
    count_must_pay = (len(ref.refers.all()) - (count_dollar + count_gem))
    if ref_type == 'GEM':
        if count_must_pay > 0:
            ref.gem_paid += count_must_pay
            ref_user.limits += count_must_pay
            ref.save()
            ref_user.save()
            return True
    return False

