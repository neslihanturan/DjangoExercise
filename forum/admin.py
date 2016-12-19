from django.contrib import admin
from .models import Post
from solo.admin import SingletonModelAdmin

admin.site.register(Post)


# Register your models here.
