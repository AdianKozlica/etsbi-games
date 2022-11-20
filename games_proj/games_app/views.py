from django.shortcuts import render,redirect,reverse
from datetime import datetime,timedelta,timezone
from django.http import HttpResponse
from django.db.models import Count
from . import models
from . import forms

def index(request):
	if request.method != "GET":
		return HttpResponse(b"Invalid request method!\n",status=400)

	games = models.Game.objects.annotate(num_views=Count("watch")).order_by("-num_views")

	return render(request,"index.html",{"games":games})


def game(request,pk):
	if request.method != "GET":
		return HttpResponse(b"Invalid request method!\n",status=400)

	try:
		game = models.Game.objects.get(pk=pk)

	except Exception:
		return redirect(reverse(index) + "?error=game_not_found")

	apk = game.apk

	return render(request,"game.html",{"apk":apk,"pk":pk})


def register_view(request,pk):
	if request.method != "POST":
		return HttpResponse(b"Invalid request method!\n",status=400)

	try:
		game = models.Game.objects.get(pk=pk)

	except Exception:
		return HttpResponse(b"Game not found\n",status=404)

	form = forms.GameForm(request.POST)

	if not form.is_valid():
		return HttpResponse(b"Invalid form data",status=422)

	fingerprint = form.cleaned_data.get("fingerprint")

	watch_obj = game.watch_set.filter(fingerprint=fingerprint).last()
	current_time = datetime.now(timezone.utc)

	if watch_obj:
		difference = (current_time - watch_obj.date_viewed).total_seconds()

		if difference <= 30:
			return HttpResponse(b"",status=400)

	models.Watch.objects.create(game=game,fingerprint=fingerprint,date_viewed=current_time)

	return HttpResponse(b"Viewed")
