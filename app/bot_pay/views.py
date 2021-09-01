from typing import Optional, List
from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404, get_list_or_404
from ninja import Router, Query
from ninja.orm import create_schema
from . import models
from http import HTTPStatus
from .schemas import Message, PatchUser, ReferOut, UserOut, ReferOutPartial
from .services.logic import get_refer_url, create_user, reward_referral_user, create_refer

router = Router()


@sync_to_async
@router.get("/users/{telegram_id}/ref", response={HTTPStatus.CREATED: ReferOut,
                                                  HTTPStatus.PARTIAL_CONTENT: ReferOutPartial})
def get_ref(request, telegram_id: str, bot_name: str = None, expand: bool = False):
    user = get_object_or_404(models.TableUsers.objects.select_related('refer_id'), telegram_id=telegram_id)
    if user.refer_id is not None:
        refer = user.refer_id
    else:
        refer_url = get_refer_url(bot_name, telegram_id)
        refer = create_refer(user, refer_url)
    status = HTTPStatus.CREATED if expand else HTTPStatus.PARTIAL_CONTENT
    return status, refer


p_types = models.PayType.objects.all()


@sync_to_async
@router.patch("/users/{telegram_id}/ref/type", response={HTTPStatus.OK: UserOut, HTTPStatus.NOT_FOUND: Message})
def change_ref_type(request, telegram_id: str, pay_type: str):
    user = get_object_or_404(models.TableUsers.objects.select_related('refer_id'), telegram_id=telegram_id)
    r = list(filter(lambda x: pay_type.lower() == x.type.lower(), p_types))
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
@router.post("/users/{telegram_id}/ref/add", response={HTTPStatus.OK: ReferOut,
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
    refer_url = get_refer_url(bot_name, telegram_id)
    r = create_refer(user, refer_url, add_user)
    return r


@sync_to_async
@router.patch("/users/{telegram_id}", tags=['Users'],
              response={HTTPStatus.OK: UserOut, HTTPStatus.NOT_FOUND: Message})
def patch_user(request, telegram_id: str, user: PatchUser = Query(...)):
    db_user = get_object_or_404(models.TableUsers, telegram_id=telegram_id)
    for key, value in user.dict(exclude_none=True).items():
        setattr(db_user, key, value)
    db_user.save()
    return db_user


@sync_to_async
@router.patch("/users/{telegram_id}/reward_referral_user", tags=['Users'],
              response={HTTPStatus.OK: Message, HTTPStatus.NOT_MODIFIED: Message})
def reward_refer(request, telegram_id: str):
    user = get_object_or_404(models.TableUsers, telegram_id=telegram_id)
    if user.from_refer is not None:
        ref_user = get_object_or_404(models.TableUsers.objects.select_related('refer_id'), telegram_id=user.from_refer)
        ref = ref_user.refer_id
        if reward_referral_user(ref, ref_user):
            return HTTPStatus.OK, Message(detail='refer gem add')

    return HTTPStatus.NOT_MODIFIED, Message(detail='refer not found')
