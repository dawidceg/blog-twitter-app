from django import forms
from .models import Comment
from accounts.models import Profile


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_pic", "background_pic"]
        exclude = ['user']                              # exclude user field
