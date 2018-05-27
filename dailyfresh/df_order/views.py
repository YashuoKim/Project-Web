#coding=utf-8
from django.shortcuts import render,redirect
from df_user import user_decorator
from df_user.models import UserInfo
from df_cart.models import CartInfo
from django.db import transaction
from models import *
from datetime import datetime
from decimal import Decimal
from django.http import JsonResponse
# Create your views here.

@user_decorator.login
def order(request):
    # 查询用户对象
    user = UserInfo.objects.get(id=request.session['user_id'])
    # 根据提交查询购物车信息
    get = request.GET
    cart_ids = get.getlist('cart_id')
    carts = []
    for item in cart_ids:
        carts.append(CartInfo.objects.get(id=int(item)))
    # 构造传递到模板中的数据
    content = {
        'title':'提交订单',
        'page_name':1,
        'carts':carts,
        'user':user,
        'cart_ids':','.join(cart_ids)
    }
    return render(request, 'df_order/order.html',content)

#1 创建订单对象 2 判断商品的库存 3 创建详单对象4 修改商品库存 5 删除购物车
#事务：一旦操作失败则全部回退
@transaction.atomic()
@user_decorator.login
def order_handle(request):
    # 保存一个事物点
    tran_id = transaction.savepoint()
    try:
        # 接收购物车编号
        post = request.POST
        cart_ids = post.getlist('id[]')
        total = post.get('total')
        address= post.get('address')
        #创建订单对象
        order = OrderInfo()
        now = datetime.now()
        uid = request.session['user_id']
        order.oid = '%s%d'%(now.strftime('%Y%m%d%H%M%S'), uid)
        order.user_id = uid
        order.odate = now
        order.ototal = Decimal(total)
        order.oaddress = address
        order.save()
        #print "*******"
        #print cart_ids
        #遍历购物车中提交信息，创建详单对象
        for id1 in cart_ids:
            #查询购物车信息
            cart = CartInfo.objects.get(id=id1)
            #判断商品库存
            goods = cart.goods
            if goods.gstore>=cart.count:#如果库存大于购买数量
                #减少商品库存
                goods.gstore = goods.gstore-cart.count
                print goods.gstore
                print "----------"
                goods.save()
                #完善详细信息
                detail = OrderDetailInfo()
                #调试用print "0000-----0000" order.id是错的，为oid
                detail.order_id = order.oid
                #print "2222-----2222"
                detail.goods_id = goods.id
                detail.price = goods.gprice
                detail.count = cart.count
                detail.save()
                #删除购物车数据
                cart.delete()
            else:#如果库存小于购买数量
                transaction.savepoint_rollback(tran_id)
                return JsonResponse({'status': 2})
        transaction.savepoint_commit(tran_id)
    except Exception as e:
        print '============%s'%e
        transaction.savepoint_rollback(tran_id)
    # 返回json供前台提示成功
    return  JsonResponse({'status': 1})

@user_decorator.login
def pay(request, oid):
    order = OrderInfo.objects.get(oid=oid)
    order.oIsPay = True
    order.opay = 1
    order.save()
    content = {'order':order}
    return render(request, 'df_order/pay.html', content)
