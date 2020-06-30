from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib import auth
from django.utils import timezone


User = settings.AUTH_USER_MODEL

class Follow(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    follow_user = models.ForeignKey(User, related_name='follow_user', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #user.profile

    background_pic = models.ImageField(default='default_background.jpg', upload_to='profile_pics',blank=True)
    profile_pic = models.ImageField(default='default.png', upload_to='profile_pics',blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


    @property                                                                # Using property we get a list of followers
    def followers_list(self):
        return Follow.objects.filter(follow_user=self.user)

    @property                                                               # Using property we get a number of following
    def following(self):
        return Follow.objects.filter(user=self.user).count()


#  Django signals to automatically create a user profile when a user object is created
def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        profile, is_created = Profile.objects.get_or_create(user = instance)

post_save.connect(post_save_user_receiver, sender=User)
