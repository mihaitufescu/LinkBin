from django.db import models

class User(models.Model):
    id_user = models.AutoField(primary_key=True)
    username = models.CharField(max_length=25,unique=True)
    password = models.CharField(max_length=128)
    bio = models.TextField()
    profile_photo_path = models.TextField()
    link_count = models.IntegerField()
    background = models.CharField(max_length=25)

class Link(models.Model):
    id_link = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.TextField()
    index = models.IntegerField()

class Card(models.Model):
    id_card = models.AutoField(primary_key=True)
    key = models.TextField()

class Ownership(models.Model):
    id_ownership = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_card = models.ForeignKey(Card, on_delete=models.CASCADE)
