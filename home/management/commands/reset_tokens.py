from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Reset all tokens that are older than 2 hours'

    def handle(self, *args, **kwargs):
        cutoff = timezone.now() - timedelta(hours=2)
        tokens = Token.objects.filter(created__lt=cutoff)
        count, _ = tokens.delete()
        self.stdout.write(f'Deleted {count} old tokens.')
