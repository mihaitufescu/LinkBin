from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models


# Formular inregistrare

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True,label='Adresa de mail')
	username = forms.CharField(required=True, label='Numele de utilizator')
	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		custom_user = models.User()
		custom_user.username = user.username
		custom_user.password = user.password
		custom_user.link_count = 0
		custom_user.bio = 'Nu este nimic aici momentan'
		custom_user.background = 'default'
		custom_user.save()
		return user

#admin : LinkBin123