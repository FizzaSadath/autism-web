from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from  datetime import datetime
# Create your views here.
from myapp.models import *
from .prediction_cnn import predict_single_image
import joblib
import numpy as np
import json
from .app_chat import executor, ChatState
from django.views.decorators.csrf import csrf_exempt


def login(request):
    return render(request,'index.html')


@csrf_exempt
def chat(request):
    if request.method == "POST":
        try:
            # ✅ Extract JSON data from request.body
            data = json.loads(request.body)
            user_message = data.get("message", "")

            if not user_message:
                return JsonResponse({"error": "No message provided"}, status=400)

            # ✅ Create ChatState instance
            state = ChatState(message=user_message)

            # ✅ Generate response using LLM
            result = executor.invoke(state.model_dump())

            return JsonResponse({"response": result})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def login_post(request):
    username=request.POST['username']
    password=request.POST['password']
    ob=login_table.objects.filter(username=username,password=password)
    if ob.exists():
        ob1=login_table.objects.get(username=username,password=password)
        if ob1.type=='admin':
            return HttpResponse('''<script>alert('Admin Login sucessfully');window.location='admin_dashboard';</script>''')
        elif ob1.type=='expert':
            request.session["lid"]=ob1.id
            return HttpResponse(
                '''<script>alert('Expert Login sucessfully');window.location='expert_dashboard';</script>''')
        else:
            return HttpResponse('''<script>alert('Invalid Username or Password');window.location='/';</script>''')
    else:
        return HttpResponse('''<script>alert('User doesnt exist');window.location='/';</script>''')

def admin_dashboard(request):
    return render(request,'Admin/index.html')


def admin_manageexpert(request):
    ob=expert_table.objects.all()
    return render(request,'Admin/manageexpert.html',{"data":ob})

def admin_Editexpert(request,id):
    request.session["expertid"]=id
    ob=expert_table.objects.get(id=id)
    return render(request,'Admin/editExpert.html',{'data':ob})

def admin_editexpert_post(request):
    name=request.POST['name']
    gender=request.POST['gender']
    dob=request.POST['dob']

    phoneno=request.POST['phoneno']
    email=request.POST['email']
    qualification=request.POST['qualification']

    if 'image' in request.FILES:
        image = request.FILES['image']

        fs=FileSystemStorage()
        fp=fs.save(image.name,image)



        obb=expert_table.objects.get(id=request.session["expertid"])
        obb.name=name
        obb.gender=gender
        obb.phoneno=phoneno
        obb.dob=dob
        obb.email=email
        obb.qualification=qualification
        obb.image=fp
        obb.save()
    else:
        obb = expert_table.objects.get(id=request.session["expertid"])
        obb.name = name
        obb.gender = gender
        obb.phoneno = phoneno
        obb.dob = dob
        obb.email = email
        obb.qualification = qualification
        obb.save()

    return HttpResponse('''<script>alert('Expert saved succesfully');window.location='admin_manageexpert';</script>''')

def admin_Deleteexpert(request,id):
        request.session["id"]=id
        ob = expert_table.objects.get(LOGIN_id=id)
        od=login_table.objects.get(id=id)
        od.delete()
        ob.delete()
        return HttpResponse('''<script>alert('Expert deleted succesfully');window.location='/admin_manageexpert';</script>''')


def admin_addexpert(request):
    return render(request,'Admin/addexpert.html')



def admin_addexpert_post(request):
    name=request.POST['name']
    gender=request.POST['gender']
    dob=request.POST['dob']
    image=request.FILES['image']
    phoneno=request.POST['phoneno']
    email=request.POST['email']
    qualification=request.POST['qualification']
    username = request.POST['username']
    password = request.POST['password']

    fs=FileSystemStorage()
    fp=fs.save(image.name,image)

    ob=login_table()
    ob.username=username
    ob.password=password
    ob.type="expert"
    ob.save()

    obb=expert_table()
    obb.name=name
    obb.gender=gender
    obb.phoneno=phoneno
    obb.dob=dob
    obb.email=email
    obb.qualification=qualification
    obb.image=fp
    obb.LOGIN=ob
    obb.save()
    return HttpResponse('''<script>alert('Expert saved succesfully');window.location='admin_manageexpert';</script>''')
















"===================================web chat with user==================="



def chatwithuser(request):
    ob = user_table.objects.all()
    return render(request,"fur_chat.html",{'val':ob})




def chatview(request):
    ob = user_table.objects.all()
    d=[]
    for i in ob:
        r={"name":i.name,'photo':i.image.url,'email':i.email,'loginid':i.LOGIN.id}
        d.append(r)
    return JsonResponse(d, safe=False)




def coun_insert_chat(request,msg,id):
    print("===",msg,id)
    ob=chat_table()
    ob.FROM_ID=login_table.objects.get(id=request.session['lid'])
    ob.TO_ID=login_table.objects.get(id=id)
    ob.message=msg
    ob.status='pending'
    ob.date=datetime.now().strftime("%Y-%m-%d")
    ob.save()

    return JsonResponse({"task":"ok"})
    # refresh messages chatlist



def coun_msg(request,id):

    ob1=chat_table.objects.filter(FROM_ID__id=id,TO_ID__id=request.session['lid'])
    ob2=chat_table.objects.filter(FROM_ID__id=request.session['lid'],TO_ID__id=id)
    combined_chat = ob1.union(ob2)
    combined_chat=combined_chat.order_by('id')
    res=[]
    for i in combined_chat:
        res.append({"from_id":i.FROM_ID.id,"msg":i.message,"date":i.date,"chat_id":i.id})

    obu=user_table.objects.get(LOGIN__id=id)


    return JsonResponse({"data":res,"name":obu.name,"photo":obu.image.url,"user_lid":obu.LOGIN.id})












def admin_viewuser(request):
    ob = user_table.objects.all()
    return render(request,'Admin/viewuser.html',{'data': ob})

def expert_dashboard(request):
    # od=login_table.objects.get(id=request.session["lid"])
    ob=expert_table.objects.get(LOGIN_id=request.session["lid"])

    return render(request,'Expert/dashboard.html',{'data':ob})

def expert_addwork(request):
    users=user_table.objects.all()
     # Get all experts
    return render(request, 'Expert/addwork.html', {'users': users})

def expert_chat(request):
    return render(request,'Expert/chat.html')

def expert_studymaterials(request):

    ob=studymaterials_table.objects.filter(EXPERT__LOGIN__id=request.session["lid"])
    return render(request,'Expert/studymaterials.html',{'data':ob})

def expert_addstudy_post(request):
    ft=request.POST['fileType']
    fi=request.FILES['fileUpload']
    des=request.POST['fileDescription']
    ob=studymaterials_table()
    ob.EXPERT=expert_table.objects.get(LOGIN__id=request.session['lid'])
    ob.type=ft
    ob.file=fi
    ob.details=des
    ob.date=datetime.today()
    ob.save()

    return redirect("/expert_studymaterials")

def expert_deletestudy(request,id):
        ob = studymaterials_table.objects.get(id=id)
        ob.delete()
        return HttpResponse(
            '''<script>alert('studymaterial deleted succesfully');window.location='/expert_studymaterials';</script>''')
def expert_assignstudy(request,id):
    request.session['mid']=id
    ob = user_table.objects.all()
    return render(request, 'Expert/assignstudy.html', {'data': ob})
def expert_assignstudy_post(request):
    id=request.session['mid']
    sid=request.POST.getlist('id')
    for i in sid:
        ob=assignstudy_table()
        ob.USER_id=i
        ob.SM_id=id
        ob.date=datetime.today()
        ob.save()
    ob = user_table.objects.all()
    #return render(request, 'Expert/assignstudy.html', {'data': ob})
    return HttpResponse('''<script>alert('assigned succesfully');window.location='/expert_studymaterials';</script>''')

def expert_viewstudy(request,id):
    ob=assignstudy_table.objects.filter(SM__EXPERT__LOGIN_id=request.session["lid"],SM_id=id)
    return render(request,'Expert/viewstudy.html',{'data':ob})

def expert_viewfeedback(request):
    ob=feedback_table.objects.filter(EXPERT__LOGIN_id=request.session["lid"])
    return render(request,'Expert/viewfeedback.html',{'data': ob})

def expert_workmanage(request):
    ob= work_table.objects.filter(EXPERT__LOGIN_id=request.session["lid"])
    return render(request, 'Expert/workmanage.html', {'data': ob})

def expert_addstudy(request):
    return render(request, 'Expert/addstudy.html')


# Load the saved model

def public_prediction(request):
    ob = expert_table.objects.all()
    return render(request,'public/child.html', {'data': ob})
def public_prediction_post(request):
    A1=request.POST['A1']
    A2=request.POST['A2']
    A3 = request.POST['A3']
    A4 = request.POST['A4']
    A5 = request.POST['A5']
    A6 = request.POST['A6']
    A7 = request.POST['A7']
    A8 = request.POST['A8']
    A9 = request.POST['A9']
    A10= request.POST['A10']
    totalscore=int(int(A1)+int(A2)+int(A3)+int(A4)+int(A5)+int(A6)+int(A7)+int(A8)+int(A9)+int(A10))
    age=request.POST['age']
    gender=request.POST['gender']
    jaundice=request.POST['jaundice']
    family_history = request.POST['family_history']
    image = request.FILES['image']
    fs=FileSystemStorage()
    fn=fs.save(image.name,image)
    clf = joblib.load('rf_model.pkl')
    lst=[]
    try:
        feature_1 = int(A1)
        feature_2 = int(A2)
        feature_3 = int(A3)
        feature_4 = int(A4)
        feature_5 = int(A5)
        feature_6 = int(A6)
        feature_7 = int(A7)
        feature_8 = int(A8)
        feature_9 = int(A9)
        feature_10 = int(A10)
        feature_11 = int(age)
        feature_12 = int(totalscore)

        # Categorical inputs
        print("\nChoose from the options below:")
        print("Sex: 0 - Male, 1 - Female")
        sex = int(gender)

        print("Jaundice: 0 - No, 1 - Yes")
        jaundice = int(jaundice)

        print("Family member with ASD: 0 - No, 1 - Yes")
        family_asd = int(family_history)

        # Combine all features into a list
        lst = [
            feature_1, feature_2, feature_3, feature_4, feature_5,
            feature_6, feature_7, feature_8, feature_9, feature_10,
            feature_11, feature_12, sex, jaundice, family_asd
        ]
        print(lst)
        print(lst)
        print(lst)
        print("-=====================")
        print("-=====================")
        print("-=====================")
        res1 = clf.predict_proba([lst])
        print(res1,"=====================")
        print(res1,"=====================")
        print(res1,"=====================")
        print(res1,"=====================")
    except Exception as e:
        print(e)
        print("Invalid input. Please enter integers only!")
        lst=[]
        res1="invalid"
    res=predict_single_image(r"C:\Users\Fathima\PycharmProjects\autism\media/"+fn)
    print(res,"=========================",res1)
    #Here res result is dl 1-no 0-yes
    #res1 is the ml result 1-yes 0-no
    print(res,"=========================",res1)
    print(res,"=========================",res1)
    print(res[2][0],res1[0])
    # Weighted Voting: Assign different weights (e.g., CNN = 0.7, RF = 0.3)
    cnn_weight = 0.7
    rf_weight = 0.3

    combined_proba_weighted = (cnn_weight * res[2][0] + rf_weight *  res1[0][::-1])
    final_prediction_weighted = np.argmax(combined_proba_weighted)

    print(f"Weighted Combined Probabilities: {combined_proba_weighted}")
    print(f"Final Weighted Prediction: {final_prediction_weighted}")
    result="Not Autistic"
    prob=combined_proba_weighted[final_prediction_weighted]
    if final_prediction_weighted==0:
        result="Autistic"

    return render(request,"public/result.html",{"res":result,"pro":prob})




def android_login(request):
    username=request.POST['username']
    password=request.POST['password']
    ob=login_table.objects.filter(username=username,password=password,type='user')
    if ob.exists():
        ob1=login_table.objects.get(username=username,password=password)
        obb=user_table.objects.get(LOGIN__id=ob1.id)
        print({"task":"valid","lid":ob1.id,"img":obb.image.url[1:],"name":obb.name})
        return JsonResponse({"task":"valid","lid":ob1.id,"img":obb.image.url[1:],"name":obb.name,"dob":obb.dob,"gender":obb.gender,"place":obb.place,"post":obb.post,"pin":obb.pin,"phoneno":obb.phoneno,"email":obb.email})
    else:
        return JsonResponse({"task":"invalid"})
def android_adduser_post(request):
    name=request.POST['name']
    gender=request.POST['gender']
    dob=request.POST['dob']
    image=request.FILES['photo']
    phoneno=request.POST['phoneno']
    email=request.POST['email']
    post=request.POST['post']
    pin=request.POST['pin']
    place = request.POST['place']

    username = request.POST['username']
    password = request.POST['password']

    fs=FileSystemStorage()
    fp=fs.save(image.name,image)

    ob=login_table()
    ob.username=username
    ob.password=password
    ob.type="user"
    ob.save()

    obb=user_table()
    obb.name=name
    obb.gender=gender
    obb.phoneno=phoneno
    obb.dob=dob
    obb.place=place
    obb.email=email
    obb.post=post
    obb.pin=pin
    obb.image=fp
    obb.LOGIN=ob

    obb.save()
    return JsonResponse({"task":"valid"})

def logout(request):
    return render(request,"index.html")


def user_sendfeedback(request):
    feedback = request.POST['feedback']
    rating = request.POST['rating']
    lid = request.POST['lid']
    eid=request.POST['eid']
    lob = feedback_table()
    lob.USER = user_table.objects.get(LOGIN__id=lid)
    lob.EXPERT = expert_table.objects.get(LOGIN__id=eid)
    lob.feedback = feedback
    lob.rating = rating
    lob.date = datetime.today()
    lob.save()
    return JsonResponse({'task': 'ok'})


def admin_sendreply(request):
    reply = request.POST['reply']
    lid = request.POST['lid']
    lob = complaint_table()
    lob.USER = user_table.objects.get(LOGIN__id=lid)
    lob.reply = reply
    lob.save()
    return JsonResponse({'task': 'ok'})



def user_sendcomplaint(request):
    complaint = request.POST['complaint']
    lid = request.POST['lid']
    lob = complaint_table()
    lob.USER = user_table.objects.get(LOGIN__id=lid)
    lob.reply='pending...'
    lob.complaint = complaint
    lob.date = datetime.today()
    lob.save()
    return JsonResponse({'task': 'ok'})

def user_viewcomplaints(request):
    lid = request.POST['lid']
    ob = complaint_table.objects.filter(USER__LOGIN__id=lid)
    print(ob, "HHHHHHHHHHHHHHH")
    mdata = []
    for i in ob:
        data = {'complaint': i.complaint,'date': str(i.date),'reply': i.reply, 'id': i.id}
        mdata.append(data)
        print(mdata)
    return JsonResponse({"status": "ok", "data": mdata})





def user_viewfeedback(request):
    ob = feedback_table.objects.all()
    print(ob, "HHHHHHHHHHHHHHH")
    mdata = []
    for i in ob:
        data = {'feedback': i.feedback, 'uname': i.USER.name, 'date': str(i.date), 'id': i.id}
        mdata.append(data)
        print(mdata)
    return JsonResponse({"status": "ok", "data": mdata})


def user_viewstudymaterials(request):
    lid=request.POST['lid']
    print(request.POST,"lllllllllllllllllllllllll")
    ob=assignstudy_table.objects.filter(USER__LOGIN_id=lid)
    print(ob,"hhhhh")
    mdata = []
    for i in ob:
        data = {'file': request.build_absolute_uri(i.SM.file.url),'expert':i.SM.EXPERT.name,'details':i.SM.details,'type':i.SM.type,'date':i.SM.date, 'id': i.id}
        mdata.append(data)
        print(mdata)
    return JsonResponse({"status": "ok", "data": mdata})




def user_viewwork(request):
    lid=request.POST['lid']
    ob = work_table.objects.filter(USER__LOGIN__id=lid)
    print(ob, "hhhhh")
    mdata = []
    for i in ob:
        data = {'work': i.work, 'details':i.details,'expert':i.EXPERT.name,'date':i.date, 'id': i.id}
        mdata.append(data)
        print(mdata)
    return JsonResponse({"task": "ok", "data": mdata})

def user_viewexpert(request):
    ob=expert_table.objects.all()
    mdata = []
    for i in ob:
        data = {'name': i.name, 'qualification':i.qualification,'id': i.id,"eid":i.LOGIN.id}
        mdata.append(data)
        print(mdata)
    return JsonResponse({'task': 'ok',"data": mdata })

def admin_viewcomplaints(request):
    ob=complaint_table.objects.all()
    return render(request,"Admin/viewcomplaints.html",{'data':ob})


def admin_send_reply(request,id):
    reply=request.POST['reply']
    ob=complaint_table.objects.get(id=id)
    ob.reply=reply
    ob.save()
    return HttpResponse(
        '''<script>alert('Replied successfully');window.location='/admin_viewcomplaints';</script>''')

def expert_addwork_post(request):
    # ft=request.POST['fileType']
    # fi=request.FILES['fileUpload']
    des=request.POST['details']
    user=request.POST['USER']
    work=request.POST['work']
    ob=work_table()
    ob.EXPERT=expert_table.objects.get(LOGIN__id=request.session['lid'])
    ob.USER=user_table.objects.get(id=user)
    ob.details=des
    ob.work=work

    ob.date=datetime.today()
    ob.save()

    return HttpResponse(
        '''<script>alert('submitted successfully');window.location='/expert_workmanage';</script>''')

def user_viewworks(request):
    lid=request.POST['lid']
    print(request.POST,"lllllllllllllllllllllllll")
    ob=work_table.objects.filter(USER__LOGIN_id=lid)
    print(ob,"hhhhh")
    mdata = []
    for i in ob:
        data = {'expert': i.EXPERT.name,'date':i.date,'work':i.work,'type':i.details,'id': i.id}
        mdata.append(data)
        print(mdata)
    return JsonResponse({"status": "ok", "data": mdata})

# def user_workresponse(request):
#     response = request.POST['response']
#     lid = request.POST['lid']
#     eid=request.POST['eid']
#     lob = work_table()
#     lob.USER = user_table.objects.get(LOGIN__id=lid)
#     lob.EXPERT = expert_table.objects.get(LOGIN__id=eid)
#     lob.response = response
#     lob.save()
#     return JsonResponse({'task': 'ok'})


def user_workresponse(request):
    print(request.POST,"kkk")
    response = request.POST['status']
    lid = request.POST['lid']
    wid=request.POST['expert_name']
    lob = work_table.objects.get(id=wid)
    lob.response = response
    lob.save()
    return JsonResponse({'task': 'ok'})




def viewchat(request):
    print(request.POST)
    fromid = request.POST['from_id']
    toid=request.POST['to_id']
    ob1 = chat_table.objects.filter(FROM_ID__id=fromid, TO_ID__id=toid)
    ob2 = chat_table.objects.filter(FROM_ID__id=toid, TO_ID__id=fromid)
    combined_chat = ob1.union(ob2)
    combined_chat = combined_chat.order_by('id')
    res = []
    for i in combined_chat:
        res.append({'msg': i.message, 'fromid': i.FROM_ID.id, 'toid': i.TO_ID.id, 'date':i.date})
    print(res,"===============================++++++++++++++++++++++++++++++++++========================")
    return JsonResponse({"status": "ok", "data": res})


def sendchat(request):
    print(request.POST)
    msg=request.POST['message']
    fromid=request.POST['fromid']
    toid=request.POST['toid']
    ob=chat_table()
    ob.message=msg
    ob.FROM_ID=login_table.objects.get(id=fromid)
    ob.TO_ID=login_table.objects.get(id=toid)
    ob.date=datetime.now().date()
    ob.save()
    return JsonResponse({"status": "ok"})




def expert_viewuser(request):
    ob = user_table.objects.all()
    res=[]
    for i in ob:
        r=video_frame.objects.filter(USER__id=i.id).order_by("-id")
        try:
            i.j=[r[0],r[1],r[2]]
        except:
            i.j=[]
        res.append(i)
    return render(request,'Expert/viewuser.html',{'data': res})

def get_score(request,id):
    request.session['sid']=id
    ob=video_frame.objects.get(USER__id= request.session['sid'])
    return render(request,'Expert/viewuser.html',{'data': ob})




