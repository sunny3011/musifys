from django.contrib import admin

from songapp.views import channel
from.models import Watchlater
from .models import Song,History,Channel,LikedSong

# Register your models here.

admin.site.register(Song)

admin.site.register( Watchlater)

admin.site.register(History)
admin.site.register(Channel)
admin.site.register(LikedSong)
