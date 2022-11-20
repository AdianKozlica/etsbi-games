from django.core.management.base import BaseCommand
from games_app.models import Game
from django.conf import settings

class Command(BaseCommand):
	help = "Fills database with games"

	def handle(self, *args, **options):
		for name,path in settings.GAMES.items():
			Game.objects.get_or_create(name=name,apk=path)
