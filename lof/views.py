from django.shortcuts import render

# Create your views here.
from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponse
import json
import base64
import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# from django_redis import get_redis_connection
import hashlib
import json
import requests
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from .models import Student,Event


def test(request):
    return HttpResponse('ok')


# @api_view(['POST'])

def wechatlogin(request):
    #前端发送code到后端,后端发送网络请求到微信服务器换取openid
    appid = 'wxb3a8c258fd1798f6'
    secret = 'd10e2068511e6e478013b5eaeae4267e'
    print(1)
    js_code = request.GET['code']
    print(js_code)
    url = 'https://api.weixin.qq.com/sns/jscode2session' + '?appid=' + appid + '&secret=' + secret + '&js_code=' + js_code + '&grant_type=authorization_code'
    response = json.loads(requests.get(url).content)  # 将json数据包转成字典
    print(response)
    if 'errcode' in response:
        # 有错误码
        return HttpResponse(json.dumps(response),content_type='application/json; charset=utf-8')
    # 登录成功
    openid = response['openid']
    session_key = response['session_key']
    if not openid:
        return HttpResponse(json.dumps(response), content_type='application/json; charset=utf-8')

    # 判断用户是否第一次登录
    try:
        user = Student.objects.get(openid=openid)
    except Exception:
        # 微信用户第一次登陆,新建用户
        user = Student.objects.create(openid=openid)
        print("ok")
        return HttpResponse(json.dumps(response),content_type='application/json; charset=utf-8')
    return HttpResponse(json.dumps(response),content_type='application/json; charset=utf-8')

def updateinfo(request):
    try:
        openid = request.GET['openid']
        truename = request.GET['truename']
        college = request.GET['college']
        cardNumber = request.GET['cardNumber']
        phoneNumber = request.GET['phoneNumber']
        qqNumber = request.GET['qqNumber']
        email = request.GET['email']
        user = Student.objects.get(openid=openid)
        if truename !='' and user.truename!=truename:
            user.truename=truename
        if college !='' and user.college!=college:
            user.college=college
        if cardNumber !='' and user.cardNumber!=cardNumber:
            user.cardNumber=cardNumber
        if qqNumber !='' and user.qqNumber!=qqNumber:
            user.qqNumber=qqNumber
        if phoneNumber !='' and user.phoneNumber != phoneNumber:
            user.phoneNumber = phoneNumber
        if email !='' and user.email!=email:
            user.email=email
        user.save()
        return HttpResponse(json.dumps({'msg':'修改成功'}),status=200)
    except Exception:
        return HttpResponse(json.dumps({'msg':'修改失败'}),status=404)

def searchinfo(request):
    res = {'data': {},'status': 500}
    try:
        openid = request.GET['openid']
        user = Student.objects.get(openid=openid)
        data={
              'truename': user.truename,
              'college': user.college,
              'cardNumber':user.cardNumber,
              'phoneNumber':user.phoneNumber,
              'qqNumber':user.qqNumber,
              'email':user.email
              }
        res['status'] = 200
        res['data'] = data
        return HttpResponse(json.dumps(res),content_type='application/json; charset=utf-8')
    except Exception:
        res['status']=404
        return HttpResponse(json.dumps(res),content_type='application/json; charset=utf-8')

class Test(APIView):
    def get(self, request):
        a = request.GET['a']
        res = {
            'success': True,
            'data': 'a'
        }
        return Response(res)

class SEND(APIView):
    count=0
    def post(self, request):
       try:
           if request.method == 'POST':
               re = json.loads(request.body)
               print(re)
               urls = ''
               photolist = ['photo1', 'photo2', 'photo3', 'photo4', 'photo5', 'photo6']
               for i in photolist:
                   if re[i] != '':
                       SEND.count += 1
                       img = re[i].split(',')[1]
                       img = bytes(img, encoding='utf-8')
                       data = base64.b64decode(img)
                       url = "photo/" + str(SEND.count) + ".jpg"
                       filename = os.path.join(settings.STATICFILES_DIRS[0], url)
                       print(filename)
                       with open(filename, 'wb') as f:
                           f.write(data)
                       ones = '/static/' + url
                       ones += ';'
                       print(ones)
                       urls += ones
                       print(urls)
               Event.objects.create(openid=re['openid'],
                                    truename=re['truename'],
                                    text=re['text'],
                                    photo=urls[:-1],
                                    date=re['date'],
                                    time=re['time'],
                                    phoneNumber=re['phoneNumber'],
                                    qqNumber=re['qqNumber'],
                                    status=re['status'],
                                    type=re['type'],
                                    iscard=re['iscard'])
               return Response({"msg": "发送成功", "code": "200"})
       except Exception:
           print(Exception)
           return Response({"msg": "发送失败", "code": "404"})

@api_view(['GET'])
def getevent(request):
    page=int(request.GET['page'])
    result = Event.objects.filter(id__gt=(page-1)*5).filter(id__lte=page*5)
    comments = []
    for one in result:
        com = {}
        com['id'] = one.id
        com['truename'] = one.truename
        com['photo']=devide(one.photo)
        com['date'] = one.date
        com['time'] = one.time
        com['phoneNumber'] = one.phoneNumber
        com['qqNumber'] = one.qqNumber
        com['status'] = one.status
        com['text'] = one.text
        com['type'] = one.type
        # print(one.id,one.name,one.message,one.date,one.time,one.emotion)
        comments.append(com)
    return Response(comments)

def devide(photo):
    m = photo.split(';')
    print(m)
    com=[]
    for i in range(len(m)):
        com.append(str(m[i]))
    print(com)
    return com
def mylost(request):
    pass

def myfind(request):
    pass

def changeStatus(request):
    pass

def searchevent(request):
    pass
