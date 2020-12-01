from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class authority_db(models.Model):
    user=models.OneToOneField(User,null=True,on_delete=models.SET_NULL)
    DESIGNATION=(
        ('Club secretary','Club secretary'),
        ('Club Office In-charge','Club Office In-charge'),
        ('Security In-charge','Security In-charge'),
        ('Guard In-charge','Guard In-charge'),
    )
    designation=models.CharField(max_length=200,null=True,choices=DESIGNATION)
    CLUB=(
        ('Computer Science Society','Computer Science Society'),
        ('Art and Photography Club','Art and Photography Club'),
        ('Dramatics Club','Dramatics Club'),
        ('Not Valid','Not Valid'),
    )
    club=models.CharField(max_length=200,null=True,choices=CLUB)
    def __str__(self):
        return self.user.username

class room_db(models.Model):
    room_number=models.CharField(max_length=200,primary_key=True)
    department=models.CharField(max_length=200,blank=True,null=True)
    def __str__(self):
        return self.room_number


class request_db(models.Model):
    request_id=models.IntegerField(default=0,primary_key=True)
    authority=models.ForeignKey(User,null=True,on_delete=models.DO_NOTHING)
    room=models.ForeignKey(room_db,on_delete=models.DO_NOTHING)
    date=models.DateField(null=True)
    SLOT=(
        ('4-5','4-5'),
        ('5-6','5-6'),
        ('6-7','6-7'),
        ('7-8','7-8'),
    )
    slot=models.CharField(max_length=200,null=True,choices=SLOT)

    STATUS=(
        ('-1','-1'),
        ('0','0'),
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
    )
    status=models.CharField(max_length=200,null=True,choices=STATUS)
    def __str__(self):
        return str(self.request_id)
