
from django import forms
from .models import CommentModel


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        exclude = ["post"]  #list the fields that should be excluded in form edition
        labels = {
            "user-name" : "Your Name",
            "user_email" : "Your Email",
            "text" : "Your Comment"
        }