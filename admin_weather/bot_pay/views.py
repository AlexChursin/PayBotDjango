from typing import Optional, List
from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404, get_list_or_404
from ninja import Router, Query
from ninja.orm import create_schema
from . import models
from http import HTTPStatus
from .schemas import Message, PatchUser
from .services.logic import get_refer_url, create_user, reward_referral_user

router = Router()


@sync_to_async
@router.get("/users/{telegram_id}/ref", response={HTTPStatus.MULTI_STATUS: create_schema(models.Refer, depth=1),
                                                  201: create_schema(models.Refer)})
def get_ref(request, telegram_id: str, bot_name: str = None, expand: bool = False):
    user = get_object_or_404(models.TableUsers.objects.select_related('refer_id'), telegram_id=telegram_id)
    if user.refer_id is not None:
        res = user.refer_id
    else:
        r = models.Refer(url=f'https://t.me/{bot_name}?start={telegram_id}_{bot_name}')
        r.save(force_insert=True)
        user.refer_id = r
        user.save()
        res = r
    if expand:
        return HTTPStatus.MULTI_STATUS, res
    else:
        return 201, res


p_types = models.PayType.objects.all()


@sync_to_async
@router.patch("/users/{telegram_id}/ref/type", response={HTTPStatus.OK: create_schema(models.TableUsers), 404: Message})
def change_ref_type(request, telegram_id: str, pay_type: str):
    user = get_object_or_404(models.TableUsers.objects.select_related('refer_id'), telegram_id=telegram_id)
    r = [t for t in p_types if pay_type.lower() == t.type.lower()]
    if len(r):
        user.refer_id.pay_type_id = r[0]
        user.refer_id.save()
    else:
        return HTTPStatus.NOT_FOUND, Message(detail='pay_type not found')
    return HTTPStatus.OK, user


@sync_to_async
@router.get("/ref_types", tags=['Pay types'], response=List[create_schema(models.PayType)])
def get_ref_type(request):
    return get_list_or_404(models.PayType)


@sync_to_async
@router.put("/users/{telegram_id}/ref/{ref_id}", response=Optional[create_schema(models.Refer)])
def put_ref(request, telegram_id: str, ref_id: str, ref: create_schema(models.Refer, exclude=['id'])):
    user = get_object_or_404(models.TableUsers, telegram_id=telegram_id)
    ref.save()
    return ref


# return user


@sync_to_async
@router.post("/users/{telegram_id}/ref/add", response={HTTPStatus.OK: create_schema(models.Refer, depth=1),
                                                       HTTPStatus.NOT_FOUND: Message,
                                                       HTTPStatus.CONFLICT: Message})
def new_ref(request, telegram_id: str, add_telegram_id: str, bot_name: str):
    user = get_object_or_404(models.TableUsers.objects, telegram_id=telegram_id)
    add_user = models.TableUsers.objects.filter(telegram_id=add_telegram_id).first()
    if add_user is not None:
        return HTTPStatus.CONFLICT, Message(detail='add_telegram_id already registered')
    if int(telegram_id) == int(add_telegram_id):
        return HTTPStatus.CONFLICT, Message(detail='telegram_id is add_telegram_id')
    if user is None:
        return HTTPStatus.NOT_FOUND, Message(detail='user not found')

    add_user = create_user(telegram_id, add_telegram_id)
    r = models.Refer(url=get_refer_url(bot_name, telegram_id))
    r.save(force_insert=True)
    r.refers.add(add_user)
    user.refer_id = r
    user.save()
    return r


@sync_to_async
@router.patch("/users/{telegram_id}", tags=['Users'],
              response={HTTPStatus.OK: create_schema(models.TableUsers), HTTPStatus.NOT_FOUND: Message})
def patch_user(request, telegram_id: str, user: PatchUser):
    db_user = get_object_or_404(models.TableUsers, telegram_id=telegram_id)
    for key, value in user.dict(exclude_none=True).items():
        setattr(db_user, key, value)
    db_user.save()
    return db_user


@sync_to_async
@router.patch("/users/{telegram_id}/reward_referral_user", tags=['Users'],
              response={HTTPStatus.OK: Message, HTTPStatus.NOT_MODIFIED: Message})
def reward_refer(request, telegram_id: str = Query(..., title='ID телеграмма')):
    user = get_object_or_404(models.TableUsers, telegram_id=telegram_id)
    if user.from_refer is not None:
        ref_user = get_object_or_404(models.TableUsers.objects.select_related('refer_id'), telegram_id=user.from_refer)
        ref = ref_user.refer_id
        if reward_referral_user(ref, ref_user):
            return HTTPStatus.OK, Message(detail='refer gem add')

    return HTTPStatus.NOT_MODIFIED, Message(detail='refer not found')


