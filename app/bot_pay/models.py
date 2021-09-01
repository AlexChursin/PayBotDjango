from django.db import models


class TableTransactions(models.Model):
    """Модель транзакции"""
    telegram_id = models.TextField('телега', primary_key=True)
    transaction_id = models.TextField('транзакция', blank=True, null=True)
    wallet = models.TextField('кошелек', blank=True, null=True)

    def __str__(self):
        return self.telegram_id

    class Meta:
        db_table = 'table_transactions'
        verbose_name = 'транзакцию'
        verbose_name_plural = 'транзакции'


class PayType(models.Model):
    """Модель типов оплаты"""
    type = models.CharField('тип оплаты', max_length=150)
    desc = models.TextField('описание')

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'тип оплаты'
        verbose_name_plural = 'типы оплаты'


class Refer(models.Model):
    """Модель рефералки"""
    url = models.CharField('реферальная ссылка', max_length=100)
    refers = models.ManyToManyField('TableUsers', verbose_name='приглашенные гости')
    pay_type_id = models.ForeignKey(PayType, verbose_name='тип оплаты', on_delete=models.DO_NOTHING, default=1)
    dollars_paid = models.IntegerField('выплачено dollar', blank=True, default=0, null=True)
    gem_paid = models.IntegerField('выплачено gem', blank=True, default=0, null=True)
    other_field = models.CharField('доп. поле', max_length=50, blank=True, null=True)

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = 'реферальную систему'
        verbose_name_plural = 'реф система'


class TableUsers(models.Model):
    """Модель пользователя"""
    telegram_id = models.TextField('телега', primary_key=True)
    user_language = models.TextField('язык', blank=True, null=True)
    hash = models.TextField('токен', blank=True, null=True)
    last_trans = models.TextField('последняя транзакция', blank=True, null=True)
    last_wallet = models.TextField('последний кошелек', blank=True, null=True)
    limits = models.IntegerField('запуски', blank=True, null=True)
    completed = models.IntegerField('состояние бота', blank=True, null=True)
    refer_id = models.ForeignKey(Refer, verbose_name='реферальная программа', on_delete=models.CASCADE, null=True,
                                 blank=True)
    from_refer = models.ForeignKey('TableUsers', verbose_name='от какойго id пришел (реферала)', on_delete=models.DO_NOTHING,
                                   null=True,
                                   blank=True)

    def __str__(self):
        return self.telegram_id

    class Meta:
        db_table = 'table_users'
        verbose_name = 'пользователя'
        verbose_name_plural = 'пользователи'
