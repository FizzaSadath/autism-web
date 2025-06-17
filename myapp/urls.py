from django.contrib import admin
from django.urls import path, include

from myapp import views

urlpatterns = [
     path('',views.public_prediction,name='public_prediction'),
     path('admin_dashboard',views.admin_dashboard,name='admin_dashboard'),
     path('admin_manageexpert',views.admin_manageexpert,name='admin_manageexpert'),
     path('admin_addexpert',views.admin_addexpert,name='admin_addexpert'),
     # path( 'admin_viewcomplaints',views.admin_viewcomplaints,name= 'admin_viewcomplaints'),
     # path('admin_viewfeedback',views.admin_viewfeedback,name='admin_feedback'),
     path('admin_viewuser',views.admin_viewuser,name='admin_viewuser'),
     path('expert_viewuser',views.expert_viewuser,name='expert_viewuser'),
     path('expert_dashboard',views.expert_dashboard,name='expert_dashboard'),
     path('expert_addwork',views.expert_addwork,name='expert_addwork'),
     path('expert_addwork_post',views.expert_addwork_post,name='expert_addwork_post'),
     path('expert_chat',views.expert_chat,name='expert_chat'),
     path('expert_studymaterials',views.expert_studymaterials,name='expert_studymaterials'),
     path('expert_viewfeedback',views.expert_viewfeedback,name='expert_viewfeedback'),
     path('expert_workmanage',views.expert_workmanage,name='expert_workmanage'),
     path('expert_addstudy', views.expert_addstudy, name='expert_addstudy'),
     path('expert_addstudy_post', views.expert_addstudy_post, name='expert_addstudy_post'),
     path('expert_deletestudy/<int:id>', views.expert_deletestudy, name='expert_deletestudy'),
     path('expert_assignstudy/<int:id>', views.expert_assignstudy, name='expert_assignstudy'),
     path('expert_assignstudy_post',views.expert_assignstudy_post,name='expert_assignstudy_post'),
     path('expert_viewstudy/<int:id>',views.expert_viewstudy,name='expert_viewstudy'),
     path('admin_send_reply/<int:id>',views.admin_send_reply,name='admin_send_reply'),
     path('login_post',views.login_post,name='login_post'),
     path('admin_addexpert_post',views.admin_addexpert_post,name='admin_addexpert_post'),
     path('admin_Editexpert/<int:id>',views.admin_Editexpert,name='admin_Editexpert'),
     path('admin_editexpert_post',views.admin_editexpert_post,name='admin_editexpert_post'),
     path('admin_Deleteexpert/<int:id>', views.admin_Deleteexpert, name='admin_Deleteexpert'),
     path('public_prediction',views.public_prediction,name='public_prediction'),
     path('public_prediction_post', views.public_prediction_post, name='public_prediction_post'),
     path('chatwithuser', views.chatwithuser, name='chatwithuser'),
     path('chatview', views.chatview, name='chatview'),
     path('coun_msg/<int:id>', views.coun_msg, name='coun_msg'),
     path('coun_insert_chat/<str:msg>/<int:id>', views.coun_insert_chat, name='coun_insert_chat'),
     path('logout', views.logout, name='logout'),
     #-------------------------------------------------------------------------------------------------------

     path('android_login', views.android_login, name='android_login'),
     path('android_adduser_post', views.android_adduser_post, name='android_adduser_post'),
     path('user_sendcomplaint', views.user_sendcomplaint, name='user_sendcomplaint'),
     path('user_viewcomplaints', views.user_viewcomplaints, name='user_viewcomplaints'),
     path('user_viewstudymaterials', views.user_viewstudymaterials, name='user_viewstudymaterials'),
     path('user_viewexpert', views.user_viewexpert, name='user_viewexpert'),
     path('admin_viewcomplaints', views.admin_viewcomplaints, name='admin_viewcomplaints'),
     path('user_viewwork', views.user_viewwork, name='user_viewwork'),
     path('user_sendfeedback', views.user_sendfeedback, name='user_sendfeedback'),
     path('user_workresponse', views.user_workresponse, name='user_workresponse'),
     path('viewchat', views.viewchat, name='viewchat'),
     path('sendchat', views.sendchat, name='sendchat'),
     path('get_score/<int:id>', views.get_score, name='get_score'),
    path("chat/", views.chat, name="chatbot_api")

]
