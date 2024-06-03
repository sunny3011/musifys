from django.urls import path
from .import views
urlpatterns = [
  path('',views.index,name="index"),
  path('songs/',views.songs,name="songs"),
  path('songs/songpost/<int:id>',views.songpost,name="songpost"),
  path('songs/signup/',views.signup,name="signup"),
  path('songs/login/',views. loginuser,name="loginuser"),
  path('songs/logout/',views.logoutuser,name="logoutuser"),
 
  path('songs/watchlater/',views.watchlater,name="watchlater"),
  path('songs/history/', views.history, name='history'),
  path('songs/marathi/', views.marathidemo, name='marathi'),
  path('songs/hindi/', views.hindidemo, name='hindi'),
  path('songs/english/', views.englishdemo, name='english'),
  path('searchResults', views.searchResults, name='searchResults'),
  path('newrelease/', views.newrelease, name='newrelease'),
  path('old/', views.oldsong, name='oldsong'),
  path('likesong/', views.likesong, name = "likesong"),
  path('songs/c/<str:channel>', views.channel, name='channel'),
  path('songs/upload', views.upload, name='upload'),

]

