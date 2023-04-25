from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/', blank=True)

    def __repr__(self):
        return 'Image(%s, %s)' % (self.user, self.photo)

    def __str__(self):
        return f'Profile for user {self.user.username}'


class Image(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    context = models.CharField(max_length=255, blank=False, null=False)
    image = models.ImageField(upload_to='images/', null=True, max_length=255)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    is_done = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.user = User
        self.save()

    def __repr__(self):
        return 'Image(%s, %s)' % (self.title, self.image)

    def __str__ (self):
        return self.title


class UnderImage(models.Model):
    context = models.CharField(max_length=255, blank=False, null=False)
    image_task = models.ForeignKey('Image', on_delete=models.CASCADE, null=False)
    is_done = models.BooleanField(default=False)

    def __repr__(self):
        return 'UnderImage(%s, %s)' % (self.context, self.image_task)

    def __str__ (self):
        return self.context, self.user
