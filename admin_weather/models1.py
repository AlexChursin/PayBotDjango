# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TableTransactions(models.Model):
    telegram_id = models.TextField()
    transaction_id = models.TextField(blank=True, null=True)
    wallet = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'table_transactions'


class TableUsers(models.Model):
    telegram_id = models.TextField()
    user_language = models.TextField(blank=True, null=True)
    hash = models.TextField(blank=True, null=True)
    last_trans = models.TextField(blank=True, null=True)
    last_wallet = models.TextField(blank=True, null=True)
    limits = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'table_users'
