from django.forms import Form, CharField, Textarea, PasswordInput, ImageField,\
            EmailField, ValidationError, ChoiceField, DateField, SelectDateWidget
from django.contrib.auth.models import User

class EditProfileForm(Form):
    first_name = CharField (max_length = 50, required = False)
    last_name  = CharField (max_length = 50, required = False)
    email      = EmailField (required = False)
    birthday   = DateField (
            required = False,
            widget = SelectDateWidget(
                empty_label = ("Choose Year", "Choose Month", "Choose Day"),
            )
    )
    gender    = ChoiceField (choices = (('M', 'Male'), ('F', 'Female')), required = False)
    avatar    = ImageField (required = False)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).count():
            raise ValidationError('Email already in use!')
        return email
