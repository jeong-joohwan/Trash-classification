from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.db import connection
import json
from .models import UserInfo


# Create your views here.
def index(request):
   


    return render(request, 'WebMain/index.html')

def ceologin(request):
    response_data = {}

    if request.method == "GET":
        return render(request, 'WebMain/ceologin.html')

    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        response_data = {}
        # myuser = UserInfo.objects.get(user_id=username)
        if not (username and password):

            response_data['error'] = "아이디와 비밀번호를 모두 입력해주세요."
            return render(request, 'WebMain/ceologin.html', response_data)
        else:

            if UserInfo.objects.filter(user_id=username):
                myuser = UserInfo.objects.get(user_id=username)
            else:
                response_data['error'] = "등록된 아이디가 아닙니다."
                return render(request, 'WebMain/ceologin.html', response_data)
            if myuser.user_type == 'admin':
                response_data['error'] = "CEO 아이디가 아닙니다."
                return render(request, 'WebMain/ceologin.html', response_data)
            
            if myuser:
                #db에서 꺼내는 명령. Post로 받아온 username으로 , db의 username을 꺼내온다.
                if password == myuser.user_pw:

                    #if check_password(password,myuser.user_pw) :
                    #request.session['user'] = myuser.id

                    #세션도 딕셔너리 변수 사용과 똑같이 사용하면 된다.
                    #세션 user라는 key에 방금 로그인한 id를 저장한것.
                    return redirect('/table')

                else:
                    response_data['error'] = "비밀번호를 틀렸습니다."

                    return render(request, 'WebMain/ceologin.html', response_data)
            elif len(myuser) < 1:
                response_data['error'] = "입력하신 정보가 틀렸습니다."
                return render(request, 'WebMain/ceologin.html', response_data)


def adminlogin(request):
    response_data = {}

    if request.method == "GET":
        return render(request, 'WebMain/adminlogin.html')

    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        response_data = {}
        # myuser = UserInfo.objects.get(user_id=username)
        if not (username and password):

            response_data['error'] = "아이디와 비밀번호를 모두 입력해주세요."
            return render(request, 'WebMain/adminlogin.html', response_data)
        else:
            if UserInfo.objects.filter(user_id=username):
                myuser = UserInfo.objects.get(user_id=username)
            else:
                response_data['error'] = "등록된 아이디가 아닙니다."
                return render(request, 'WebMain/ceologin.html', response_data)
            if myuser.user_type == 'CEO':
                response_data['error'] = "관리자 아이디가 아닙니다."
                return render(request, 'WebMain/ceologin.html', response_data)
            if myuser:
                #db에서 꺼내는 명령. Post로 받아온 username으로 , db의 username을 꺼내온다.
                if password == myuser.user_pw:

                    #if check_password(password,myuser.user_pw) :
                    #request.session['user'] = myuser.id

                    #세션도 딕셔너리 변수 사용과 똑같이 사용하면 된다.
                    #세션 user라는 key에 방금 로그인한 id를 저장한것.
                    return redirect('/control2')

                else:
                    response_data['error'] = "비밀번호를 틀렸습니다."

                    return render(request, 'WebMain/adminlogin.html', response_data)
            elif len(myuser) < 1:
                response_data['error'] = "입력하신 정보가 틀렸습니다."
                return render(request, 'WebMain/adminlogin.html', response_data)



def control(request):
    return render(request, 'WebMain/control.html')
def control2(request):
    return render(request, 'WebMain/control2.html')    

def user(request):
    usertype=''
    name=''
    email=''
    password=''
    location=''
    carnumber=''
    userid=''
    carweight=''
    if request.method =='POST':
        usertype=request.POST.get('usertype')
        name=request.POST.get('name')
        email=request.POST.get('email')
        userid=request.POST.get('userid')
        password=request.POST.get('password')
        location=request.POST.get('location')
        carnumber=request.POST.get('carnumber')
        carweight=request.POST.get('carweight')
    cursor=connection.cursor()
    strSql= "INSERT IGNORE INTO user_info(user_car_number,user_type,user_name,user_email,user_id,user_pw,user_region,user_car_weight) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}') ".format(carnumber,usertype,name,email,userid,password,location,carweight)
    cursor.execute(strSql)
    cursor.fetchall()
    connection.commit()
    connection.close()
    return render(request,'WebMain/user.html')
def user2(request):
    usertype=''
    name=''
    email=''
    password=''
    location=''
    carnumber=''
    userid=''
    carweight=''
    if request.method =='POST':
        usertype=request.POST.get('usertype')
        name=request.POST.get('name')
        email=request.POST.get('email')
        userid=request.POST.get('userid')
        password=request.POST.get('password')
        location=request.POST.get('location')
        carnumber=request.POST.get('carnumber')
        carweight=request.POST.get('carweight')
    cursor=connection.cursor()
    strSql= "INSERT IGNORE INTO user_info(user_car_number,user_type,user_name,user_email,user_id,user_pw,user_region,user_car_weight) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}') ".format(carnumber,usertype,name,email,userid,password,location,carweight)
    cursor.execute(strSql)
    cursor.fetchall()
    connection.commit()
    connection.close()
    return render(request,'WebMain/user2.html')    

def table(request):
    trash=''
    date=''
    date2=''
    answer={}
    
    if request.method =='POST':
        date=request.POST.get('choices-date')
        date2=request.POST.get('choices-date2')
        trash=request.POST.get('choices-trash')
    answer['종류']=trash
    answer['시작일']=date
    answer['종료일']=date2    
    cursor=connection.cursor()    
    strSql="SELECT trash_region,round(sum(trash_weight),2) as trash_weight,trash_name,create_date from trash WHERE trash_name='{0}' AND DATE_FORMAT(create_date,'%Y-%m-%d') BETWEEN '{1}' AND '{2}' GROUP BY trash_region ORDER BY trash_region".format(trash,date,date2)  
    
    result=cursor.execute(strSql)
    datas=cursor.fetchall()
    
    connection.commit()
    connection.close()
    books=[]
   
    for data in datas:
        row = {"trash_region":data[0],"trash_weight":data[1],"trash_name":data[2],"create_date":data[3]}
        books.append(row)
     
   
    resultStr ={ "books" : books }

    result = json.dumps(resultStr)
    
    return render(request, 'WebMain/table.html', {'result':result,'books':books,'answer':answer})


def ajaxTest(request):
    cursor = connection.cursor()
    strSql = "SELECT trash_region,trash_name,round(trash_weight,2)as trash_weight,create_date FROM trash order by trash_id DESC limit 0,15"
    cursor.execute(strSql)
       
    connection.commit()
    connection.close()
    
    return HttpResponse(json.dumps(dictfetchall(cursor),ensure_ascii=False), content_type="application/json")

def dictfetchall(cursor):  
     columns = [col[0] for col in cursor.description]   
     return [ dict(zip(columns, row)) for row in cursor.fetchall()  ]




def ajaxTest2(request):
    cursor=connection.cursor()
    strSql="SELECT t.trash_name,ROUND(t.trash_weight,2)AS trash_weight FROM trash t,trash_car tc WHERE t.user_car_number=(SELECT tc.user_car_number FROM trash_car ORDER BY tc.index DESC LIMIT 1) AND create_date>SUBDATE(NOW(),INTERVAL 12 HOUR) "
    cursor.execute(strSql)
       
    connection.commit()
    connection.close()
    
    return HttpResponse(json.dumps(dictfetchall(cursor),ensure_ascii=False), content_type="application/json")

def ajaxTest3(request):
    cursor=connection.cursor()
    strSql="SELECT u.user_car_number,u.user_email,u.user_region,u.user_name FROM trash_car t,user_info u WHERE (SELECT t.user_car_number FROM trash_car ORDER BY t.index DESC LIMIT 1)=u.user_car_number ORDER BY t.index DESC LIMIT 1"    
    cursor.execute(strSql)

    connection.commit()
    connection.close()
    
    return HttpResponse(json.dumps(dictfetchall(cursor),ensure_ascii=False), content_type="application/json")