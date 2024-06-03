
from django.db import models

from django.contrib.auth.models import User


yearOfRelease = (
    ('2022','2022'),
    ('2021','2021'),
    ('2020','2020'),
    ('2019','2019'),
    ('2018','2018'),
    ('2017','2017'),
    ('2016','2016'),
    ('2015', '2015'),
    ('2014', '2014'),
    ('2013', '2013'),
    ('2012', '2012'),
    ('2011', '2011'),
    ('2010', '2010'),
    ('2009', '2009'),
    ('2008', '2008'),
    ('2007', '2007'),
    ('2006', '2006'),
    ('2005', '2005'),
    ('2004','2004'),
    ('2003','2003'),
    ('2002','2002'),
    ('2001','2001'),
    ('2000','2000'),
    ('1995','1995'),
    ('1990','1990'),
    ('1985','1985'),
)

genre = (
    ('Album','Album'),
    ('Bollywood','Bollywood'),
    ('Hollywood','Hollywood'),
)

language = (
    ('Hindi','Hindi'),
    ('English','English'),
    ('marathi','marathi'),
    ('Haryanvi', 'Haryanvi'),
    ('Punjabi','Punjabi')
)


tags = (
    ('Classical','Classical'),
    ('Romantic','Romantic'),
    ('Pop','Pop'),
    ('Rock','Rock'),
    ('Devotional','Devotional'),
    ('Bhajan', 'Bhajan'),
    ('Dance','Dance'),
    ('Disco','Disco'),
    ('Ghazal','Ghazal'),
    ('Qawwali','Qawwali'),
)

productionHouse = (
    ('T-Series','T-Series'),
    ('Sony Music','Sony Music'),
    ('Zee Music Company','Zee Music Company'),
    ('Unknown','Unknown')
)


Typedata= (
    ('new','new'),
    ('old','old')
)



# Create your models here.
class Song(models.Model):
    song_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    tags = models.CharField(choices=tags, max_length=20, default='Classical')
    genre = models.CharField(choices=genre, max_length=20, default='Album')
    language = models.CharField(choices=language, max_length=20, default='Hindi')
    year = models.CharField(choices=yearOfRelease, max_length=20, default='2021')
    type = models.CharField(choices=Typedata, max_length=20, default='new')
  
    singer1 = models.CharField(max_length=200,default='')
    singer2 = models.CharField(max_length=200, default='')
    productionHouse = models.CharField(choices=productionHouse, max_length=20, default='Unknown')
    movie = models.CharField(max_length=500, default="")
    image=models.ImageField(upload_to='document')
    song=models.FileField(upload_to='document')
    credit=models.CharField(max_length=2000000,default="")
    singerimage=models.ImageField(upload_to='document',default="",blank=True)
    
    

    def __str__(self):
        return self.name
# Create your models here.

class LikedSong(models.Model):
    liked_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    music_id = models.CharField(max_length=10000000, default="")

    def __str__(self):
        return self.user.first_name
      
   



class Watchlater(models.Model):
    watch_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_id = models.CharField(max_length=10000000, default="")
    
    def __str__(self):
        return self.user
    

    
class History(models.Model):
    hist_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    music_id = models.CharField(max_length=10000000, default="")
    def __str__(self):
        return self.user
    
    
class Channel(models.Model):
    channel_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    music = models.CharField(max_length=100000000)





































