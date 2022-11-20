from django import forms

class GameForm(forms.Form):
	fingerprint = forms.CharField()