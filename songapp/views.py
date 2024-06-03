
import random
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Case, When
from django.shortcuts import render, redirect

from songapp.models import Song, Watchlater, History, LikedSong, Channel


# Create your views here.
def searchResults(request):
    if request.method == "POST":
        data = request.POST["data"]
        # print(data)
        allSongs = Song.objects.all()
        songsFound = allSongs.filter(name__icontains=data)
        moviesFound = allSongs.filter(movie__icontains=data)
        singerFound = allSongs.filter(singer1__icontains=data)
        songsFound = list(set(list(songsFound) + list(singerFound) + list(moviesFound)))[:6]

        return render(request, 'songapp/searchResults.html', {'songsFound': songsFound})
    else:
        return redirect("/")


def history(request):
    if request.method == "POST":
        user = request.user
        music_id = request.POST['music_id']
        history = History(user=user, music_id=music_id)
        history.save()

        return redirect(f"/songs/songpost/{music_id}")

    history = History.objects.filter(user=request.user)
    ids = []
    for i in history:
        ids.append(i.music_id)

    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    song = Song.objects.filter(song_id__in=ids).order_by(preserved)

    return render(request, "songapp/history.html", {"history": song})


def watchlater(request):
    if request.method == "POST":
        user = request.user
        video_id = request.POST['video_id']

        watch = Watchlater.objects.filter(user=user)

        for i in watch:
            if video_id == i.video_id:
                message = "Your Video is Already Added"
                break
        else:
            watchlater = Watchlater(user=user, video_id=video_id)
            watchlater.save()
            message = "Your Video is Succesfully Added"

        song = Song.objects.filter(song_id=video_id).first()
        songall = Song.objects.all()[:5]

        return render(request, f"songapp/songpost.html/", {'song': song, "message": message, 'songall': songall})

    wl = Watchlater.objects.filter(user=request.user)
    ids = []
    for i in wl:
        ids.append(i.video_id)

    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    song = Song.objects.filter(song_id__in=ids).order_by(preserved)
    return render(request, "songapp/watchlater.html", {'song': song})


def index(request):
    allsong = list(Song.objects.all()[:7])

    ids = []
    for i in allsong:
        ids.append(i.song_id)

    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    song = Song.objects.filter(song_id__in=ids).order_by(preserved)
    random.shuffle(allsong)
    like = list(LikedSong.objects.all()[:7])
    marathi = list(Song.objects.filter(language='marathi')[:7])
    random.shuffle(marathi)
    hindi = list(Song.objects.filter(language='Hindi')[:7])
    random.shuffle(hindi)
    english = list(Song.objects.filter(language='English')[:7])
    random.shuffle(english)
    old = list(Song.objects.filter(type='old')[:7])
    random.shuffle(old)
    newreleases = list(Song.objects.filter(type='new')[:7])
    random.shuffle(newreleases)
   
 
    return render(request, "index.html",
                  {'song': song, 'marathi': marathi, 'hindi': hindi, 'english': english, 'newRealeases': newreleases,
                   'old': old})


def newrelease(request):
    allsong = list(Song.objects.all()[:7])
    sameMovie = []
    newRealeases = []
    for i in allsong:
        if int(i.year) >= 2021:
            if i.genre == 'Album' or (i.genre not in sameMovie):
                newRealeases.append(i)
                sameMovie.append(i.genre)
    random.shuffle(newRealeases)
    newRealeases = newRealeases[:15]
    # print(newRealeases)
    del sameMovie
    return render(request, "songapp/newrelease.html", {'newRealeases': newRealeases})


def oldsong(request):
    songs = Song.objects.filter()
    return render(request, "songapp/oldsong.html", {'old': songs})


def likesong(request):
    if request.method == "POST":
        user = request.user
        music_id = request.POST['music_id1']

        watch = LikedSong.objects.filter(user=user)

        for i in watch:
            if music_id == i.music_id:
                break
        else:
            watchlater = LikedSong(user=user, music_id=music_id)
            watchlater.save()
        song = Song.objects.filter(song_id=music_id).first()
        songall = Song.objects.all()[:5]
        return render(request, f"songapp/songpost.html/", {'song': song, 'songall': songall})
    wl = LikedSong.objects.filter(user=request.user)
    ids = []
    for i in wl:
        ids.append(i.music_id)

    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    song = Song.objects.filter(song_id__in=ids).order_by(preserved)
    return render(request, "songapp/likedsong.html", {'song': song})


def channel(request, channel):
    chan = Channel.objects.filter(name=channel).first()
    video_ids = str(chan.music).split(" ")[1:]

    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(video_ids)])
    song = Song.objects.filter(song_id__in=video_ids).order_by(preserved)

    return render(request, "songapp/channel.html", {"channel": chan, "song": song})


def upload(request):
    if request.method == "POST":
        name = request.POST['name']
        singer1 = request.POST['singer']
        tag = request.POST['tag']
        image = request.POST['image']
        movie = request.POST['movie']
        credit = request.POST['credit']
        song1 = request.FILES['file']

        song_model = Song(name=name, singer1=singer1, tags=tag, image=image, movie=movie, credit=credit, song=song1)
        song_model.save()

        music_id = song_model.song_id
        channel_find = Channel.objects.filter(name=str(request.user))
        print(channel_find)

        for i in channel_find:
            i.music += f" {music_id}"
            i.save()

    return render(request, "songapp/upload.html")


def songs(request):
    song = Song.objects.all().order_by('song_id')[::-1]
    random.shuffle(song)
    return render(request, 'songapp/songs.html', {'song': song})


def songpost(request, id):
    song = Song.objects.filter(song_id=id).first()
    songall = Song.objects.all()[:5]
    return render(request, 'songapp/songpost.html', {'song': song, 'songall': songall})


def signup(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']

        # check for error
        if len(username) > 10:
            messages.error(request, "user must be under 10 character...")
            return redirect('signup')

        # check for only data enter digit and aiphabeats
        if not username.isalnum():
            messages.error(request, "username  must only digit and alphabeats...")
            return redirect('signup')

        # commpaired password
        if pass1 != pass2:
            messages.error(request, "password do not match...")
            return redirect('signup')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.save()
        messages.info(request, "your musify account has been successfully created ..")
        return redirect('index')
    else:
        return render(request, 'songapp/signup.html')


def loginuser(request):
    if request.method == 'POST':

        loginuser = request.POST['loginuser']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginuser, password=loginpassword)

        if user is not None:
            login(request, user)
            channel = Channel(name=user)
            channel.save()
            messages.success(request, "u r successfully logged in....")
            return redirect('songs')
        else:
            messages.success(request, "invalid credientials....")
            return redirect('loginuser')
    return render(request, 'songapp/login.html')


def logoutuser(request):
    logout(request)
    return redirect('index')




def marathidemo(request):
    marathi = list(Song.objects.filter(language='marathi'))
    random.shuffle(marathi)
    return render(request, "songapp/marathi.html", {'marathi': marathi})


def hindidemo(request):
    hindi = list(Song.objects.filter(language='Hindi')[:7])
    random.shuffle(hindi)
    return render(request, "songapp/hindi.html", {'hindi1': hindi})


def englishdemo(request):
    english = list(Song.objects.filter(language='English')[:7])
    random.shuffle(english)
    return render(request, "songapp/english.html", {'english1': english})
