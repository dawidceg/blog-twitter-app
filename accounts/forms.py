from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms



class UserCreateForm(UserCreationForm): # My Form usues django form UserCreateForm
    class Meta:
        fields = ("username", "email", "password1", "password2")  # Needed fields
        model = get_user_model()                                  # We refer to the user model
                                                                  # wtedy ta metoda zwróci nam aktualnego aktywnego użytkownia
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)                         # Adds labels to selected fields. We use the super function because of inheritance
        self.fields["username"].label = "Display name"
        self.fields["email"].label = "Email address"
