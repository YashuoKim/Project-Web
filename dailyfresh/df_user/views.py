#coding=utf-8
from django.shortcuts import render, redirect
from models import *
from hashlib import sha1
from django.http import JsonResponse,HttpResponseRedirect
from . import user_decorator
from df_goods.models import GoodsInfo
from df_order.models import OrderInfo
from django.core.paginator import Paginator
from df_cart.models import *

def register(request):
    return render(request, 'df_user/register.html')

def register_handle(request):
    #接收用户输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    #判断两次密码
    if upwd != upwd2:
        return redirect('/user/register/')
    #密码加密
    s1 = sha1()
    s1.update(upwd)
    upwd3 = s1.hexdigest()
    #创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()
    #注册成功，转到登录界面

    return redirect('/user/login/')

def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})

def login(request):
    uname = request.COOKIES.get('uname', '')
    content = {'title':'用户登录', 'error_name':0, 'error_pwd':0, 'uname':uname}
    return render(request, 'df_user/login.html', content)

def login_handle(request):
    #接收请求消息
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu', 0)
    #根据用户名查询对象
    users = UserInfo.objects.filter(uname=uname)
    #print uname
    #判断：如果未查到则用户名错，如果查到则判断密码是否正确，正确则转到用户中心
    if len(users)==1:
        s1=sha1()
        s1.update(upwd)
        if s1.hexdigest()==users[0].upwd:
            url = request.COOKIES.get('url', '/index/')
            red = HttpResponseRedirect(url)
            #记住用户名
            if jizhu!=0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red
        else:
            content = {'title':'用户登录', 'error_name':0, 'error_pwd':1, 'uname':uname, 'upwd':upwd}
            return render(request, 'df_user/login.html', content)
    else:
        content = {'title':'用户登录', 'error_name':1, 'error_pwd':0, 'uname':uname, 'upwd':upwd}
        return render(request, 'df_user/login.html', content)

def logout(request):
    request.session.flush()
    return redirect('/index/')

@user_decorator.login
def info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
    #最近浏览
    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_ids1 =goods_ids.split(',')
    goods_list = []
    if len(goods_ids):
        for goods_id in goods_ids1:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))

    content ={'title':'用户中心','page_name':1,
              'user_email':user_email, 'goods_list':goods_list,
              'user_name':request.session['user_name']}
    return render(request, 'df_user/user_center_info.html', content)

@user_decorator.login
def order(request):
    content ={'title':'用户中心', 'page_name':1}
    return render(request, 'df_user/user_center_order.html', content)

@user_decorator.login
def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.ureceiver = post.get('ureceiver')
        user.uaddress = post.get('uaddress')
        user.upostcode = post.get('upostcode')
        user.uphone = post.get('uphone')
        user.save()
    content = {'title':'用户中心', 'user':user, 'page_name':1}
    return render(request, 'df_user/user_center_site.html', content)

@user_decorator.login
def user_center_order(request, pageid):
    """
        此页面用户展示用户提交的订单，由购物车页面下单后转调过来，也可以从个人信息页面查看
        根据用户订单是否支付、下单顺序进行排序
     """
    uid = request.session.get('user_id')
    # 订单信息，根据是否支付、下单顺序进行排序
    orderinfos = OrderInfo.objects.filter(user_id=uid).order_by('opay', '-oid')

    # 分页
    # 获取orderinfos list  以两个为一页的 list
    paginator = Paginator(orderinfos, 2)
    # 获取 上面集合的第 pageid 个 值
    orderlist = paginator.page(int(pageid))


    # 构造上下文
    content = {'page_name': 1, 'title': '全部订单',
               'order': 1, 'orderlist': orderlist,
               'paginator':paginator}

    return render(request, 'df_user/user_center_order.html', content)