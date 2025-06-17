from django.db import models

# Create your models here.
class login_table(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    type=models.CharField(max_length=100)

class expert_table(models.Model):
    LOGIN=models.ForeignKey(login_table,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    gender=models.CharField(max_length=10)
    dob=models.DateField()
    image=models.FileField()
    phoneno=models.BigIntegerField()
    email=models.CharField(max_length=100)
    qualification=models.CharField(max_length=50)

class user_table(models.Model):
    LOGIN = models.ForeignKey(login_table, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    image = models.FileField()
    place=models.CharField(max_length=100)
    post=models.CharField(max_length=100)
    pin=models.BigIntegerField()
    phoneno = models.BigIntegerField()
    email = models.CharField(max_length=100)

class feedback_table(models.Model):
    USER=models.ForeignKey(user_table, on_delete=models.CASCADE)
    EXPERT=models.ForeignKey(expert_table, on_delete=models.CASCADE)
    feedback=models.CharField(max_length=200)
    rating=models.FloatField()
    date=models.DateField()

class complaint_table(models.Model):
    USER = models.ForeignKey(user_table, on_delete=models.CASCADE)
    complaint=models.CharField(max_length=600)
    date=models.DateField()
    reply=models.CharField(max_length=600)

class chat_table(models.Model):
    FROM_ID = models.ForeignKey(login_table, on_delete=models.CASCADE,related_name="kk")
    TO_ID = models.ForeignKey(login_table, on_delete=models.CASCADE,related_name="hh")
    message=models.CharField(max_length=600)
    date=models.DateField()
    status=models.CharField(max_length=30)

class studymaterials_table(models.Model):
    EXPERT=models.ForeignKey(expert_table, on_delete=models.CASCADE)
    type=models.CharField(max_length=50)
    file=models.FileField()
    details=models.CharField(max_length=200)
    date=models.DateField()

class work_table(models.Model):
    EXPERT = models.ForeignKey(expert_table, on_delete=models.CASCADE)
    USER = models.ForeignKey(user_table, on_delete=models.CASCADE)
    date=models.DateField()
    work=models.CharField(max_length=50)
    details=models.CharField(max_length=200)
    response=models.CharField(max_length=600)

class score_table(models.Model):
    USER = models.ForeignKey(user_table, on_delete=models.CASCADE)
    type=models.CharField(max_length=100)
    score=models.FloatField()

class AQscore_table(models.Model):
    A1 = models.IntegerField()
    A2 = models.IntegerField()
    A3 = models.IntegerField()
    A4 = models.IntegerField()
    A5 = models.IntegerField()
    A6 = models.IntegerField()
    A7 = models.IntegerField()
    A8 = models.IntegerField()
    A9 = models.IntegerField()
    A10 = models.IntegerField()
    totalscore=models.IntegerField()

class assignstudy_table(models.Model):
    USER = models.ForeignKey(user_table, on_delete=models.CASCADE)
    SM = models.ForeignKey(studymaterials_table, on_delete=models.CASCADE)
    date = models.DateField()

class sm_type_table(models.Model):
    type = models.CharField(max_length=20)
    file = models.CharField(max_length=100)

# class video_frame(models.Model):
#     USER = models.ForeignKey(user_table, on_delete=models.CASCADE)
#     type = models.CharField(max_length=20)
#     score=models.FloatField()

class video_frame(models.Model):
    USER = models.ForeignKey(user_table, on_delete=models.CASCADE)
    type = models.ForeignKey(sm_type_table,on_delete=models.CASCADE)
    score=models.FloatField()



