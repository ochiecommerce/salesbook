import random
import string
from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from contacts.models import Phonebook
from contacts.views import User

random_name = lambda length:''.join([random.choice(string.ascii_lowercase) for i in range(length)])
random_sentence = lambda length:' '.join([random_name(6) for i in range(length)])

def random_phonebooks(user):
    for i in range(100):
        pb=Phonebook(name=random_name(7),description=random_sentence(5),creator=user)
        pb.save()

class Command(BaseCommand):
    help = 'inflate demo data contacts database'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('-u',)
        parser.add_argument('-p')

    def handle(self, *args: Any, **options: Any) -> str | None:
        user=User(username=options['u'],password=options['p'])
        user.save()
        random_phonebooks(user)