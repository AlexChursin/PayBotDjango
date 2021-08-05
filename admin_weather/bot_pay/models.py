import os
from datetime import datetime

from django.db import models
import os

from django.db import models

from django.db import models


class TableTransactions(models.Model):
    telegram_id = models.TextField('телега', primary_key=True)
    transaction_id = models.TextField('транзакция', blank=True, null=True)
    wallet = models.TextField('кошелек', blank=True, null=True)


    def __str__(self):
        return self.telegram_id

    class Meta:
        managed = False
        db_table = 'table_transactions'
        verbose_name = 'транзакцию'
        verbose_name_plural = 'транзакции'


class TableUsers(models.Model):
    telegram_id = models.TextField('телега', primary_key=True)
    user_language = models.TextField('язык', blank=True, null=True)
    hash = models.TextField('токен', blank=True, null=True)
    last_trans = models.TextField('последняя транзакция', blank=True, null=True)
    last_wallet = models.TextField('последний кошелек', blank=True, null=True)
    limits = models.IntegerField('запуски', blank=True, null=True)
    completed = models.IntegerField('состояние бота', blank=True, null=True)
    created = models.DateTimeField('создано', blank=True, null=True, auto_now_add=True, editable=True)
    updated = models.DateTimeField('обновлено', blank=True, null=True, auto_now=True,  editable=True)


    def __str__(self):
        return self.telegram_id

    class Meta:
        managed = False
        db_table = 'table_users'
        verbose_name = 'пользователя'
        verbose_name_plural = 'пользователи'

