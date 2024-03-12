from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

class hospital_details(models.Model):
    # SIZE_CHOICES=[
    #     ('small','Small'),
    #     ('medium','Medium'),
    #     ('large','Large'),
    # ]
    hospital_id=models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    org_name=models.CharField(max_length=280, default=None, null=True)
    org_state=models.CharField(max_length=280, default=None, null=True) 
    size=models.CharField(max_length=10,default=None, null=True)
    threshold=models.IntegerField(default=0,null=True)

    # def save(self,*args, **kwargs):
    #     if self.size=='small':
    #         self.threshold=5
    #     elif self.size=='medium':
    #         self.threshold=10
    #     elif self.size=='large':
    #         self.threshold=15
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.org_name
     
class blood_details(models.Model):
    hospital=models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    threshold=models.ForeignKey(hospital_details, on_delete=models.CASCADE, default=None, null=True)
    blood_type = models.CharField(max_length=128)
    amount=models.IntegerField()
    # days=models.DateField(blank=True, default=None)
    days=models.IntegerField(default=0)
    
    def __str__(self):
        return self.blood_type
    
# class bloodrequest(models.Model):
#     sender=models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
#     receiver=models.ForeignKey(User,on_delete=models.CASCADE,related_name='receiver')

class notification(models.Model):
    hospital=models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    blood_type=models.CharField(max_length=256)
    reason=models.CharField(max_length=256, null=True)
    def __str__(self):
        return self.blood_type   



class FriendList(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
    friends=models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="friends")
    def __str__(self):
        return self.user.username
    def add_friend(self,account):
        '''
        add a new friend
        '''
        if not account in self.friends.all():
            self.friends.add(account)
            self.save()
    def remove_friend(self,account):
        '''
        remove a friend
        '''
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self,removee):
        '''
        initiate the action of unfriending someone
        '''
        remover_friends_list=self #person terminating the friendship

        #remove friend from remover friend list
        remover_friends_list.remove_friend(removee)
        #remove friend from removee friend list
        friends_list= FriendList.objects.get(user=removee)
        friends_list.remove_friend(self.user)

    def is_mutual_friend(self,friend):
        '''
        is this a friend?
        '''
        if friend in self.friends.all():
            return True
        return False

class FriendRequest(models.Model):
    '''
    a friend request consists of two main parts:
    1. sender:
    2. receiver:
    '''
    sender=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
    receiver=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name="receiver")
    is_accepted=models.BooleanField(blank=True, null=False, default=True)
    def __str__(self):
        self.sender.username

    def accept(self):
        '''
        accept a request
        update
        '''  
        receiver_friend_list=FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list=FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_accepted=False
                self.save()

    def decline(self):
        '''
        decline a fried request
        set is_accepted field to false
        '''
        self.is_accepted=False
        self.save()
    
    def cancel(self):
        '''
        cancel a request
        set is_accepted to false
        '''
        self.is_accepted=False
        self.save()

class UserLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None,null=True)
    country = models.CharField(max_length=100, default=None)
    # countryCode=models.CharField(max_length=100, default=None)
    # region = models.CharField(max_length=100, default=None)
    # regionName = models.CharField(max_length=100, default=None)
    city = models.CharField(max_length=100, default=None)
    # zip=models.IntegerField( default=None)
    lat=models.FloatField(default=None)
    lon=models.FloatField(default=None)
    # timezone=models.CharField(max_length=300, default=None)
    # isp=models.CharField(max_length=300, default=None)
    # org=models.CharField(max_length=300, default=None)
    query=models.TextField( default=None)
    # location=models.PointField()

class distance_list(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=None,null=True)
    donating_hospital=models.CharField(max_length=657)
    distance=models.FloatField(max_length=957)

class eligible_hospitals(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=None,null=True)
    donating_hospital=models.CharField(max_length=954)
    amount=models.IntegerField()
    distance=models.FloatField(max_length=469)
    blood_type=models.CharField(max_length=358, null=True, default=None)