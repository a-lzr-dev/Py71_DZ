from django import forms

from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['table', 'date', 'hour_start', 'hour_end']

# class CreateNoteForm(forms.ModelForm):
#     class Meta:
#         model = Note
#         fields = ['title', 'content', 'image']