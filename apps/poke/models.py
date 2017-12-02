from __future__ import unicode_literals
from ..login.models import User
from django.db import models

# Create your models here.
class PokeManager(models.Manager):
    def Poke(self, id, uId):
        try:
            userToPoke = User.objects.get(id=id)
            currentUser = User.objects.get(id=uId)
            Poke.objects.create(poker=currentUser, pokee=userToPoke)
        except:
            print "No user with this id {}".format(id)

class Poke(models.Model):
    poker = models.ForeignKey(User, related_name="pokes_made")
    pokee = models.ForeignKey(User, related_name="pokes_received")
    created_at = models.DateTimeField(auto_now_add=True)
    objects = PokeManager()
