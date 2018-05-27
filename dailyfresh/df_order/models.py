#coding=utf-8
from django.db import models

class OrderInfo(models.Model):
    #订单编号
    oid = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey('df_user.UserInfo')
    odate = models.DateTimeField(auto_now=True)
    oIsPay = models.BooleanField(default=False)
    #订单总金额
    ototal = models.DecimalField(max_digits=8, decimal_places=2)
    oaddress = models.CharField(max_length=150,default='')
    opay = models.IntegerField(default=0)

class OrderDetailInfo(models.Model):
    goods = models.ForeignKey('df_goods.GoodsInfo')
    order = models.ForeignKey(OrderInfo)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    count = models.IntegerField()
