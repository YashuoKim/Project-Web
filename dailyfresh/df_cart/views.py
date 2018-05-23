#coding=utf-8
from django.shortcuts import render
from django.http import JsonResponse
from df_user import user_decorator
from models import CartInfo

@user_decorator.login
def cart(request):
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid)
    content = {'title':'购物车',
               'page_name':1,
               'carts':carts}
    return render(request, 'df_cart/cart.html', content)
