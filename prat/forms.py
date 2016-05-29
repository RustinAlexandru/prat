from django.contrib.auth.models import User
from django.forms import Form, ModelForm, CharField, PasswordInput, \
    ImageField, EmailField, ValidationError, DateField, \
    SelectDateWidget, ChoiceField

from prat.models import Task, Category, UserGroup


class UserRegisterForm(Form):
    username = CharField(max_length=30)
    password = CharField(widget=PasswordInput)
    email = EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).count():
            raise ValidationError('Email already in use!')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).count():
            raise ValidationError('Username taken, pick another one!')
        return username


class EditProfileForm(Form):
    username = CharField(max_length=30, required = False)
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

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).count():
            raise ValidationError('Username taken, pick another one!')
        return username


class CreateTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'category']
        error_messages = {
            'category': {
                'required': ("You need to pick a category! "),
            },
        }

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise ValidationError('You need to pick a category!')
        return category


class EditTaskForm(Form):
    name = CharField(max_length=100, required = False)
    category = ChoiceField(
        choices=((cat.pk, cat.name) for cat in Category.objects.all()),
        required = False
        )


class CreateGroupForm(ModelForm):
    class Meta:
        model = UserGroup
        fields = ['name', 'description']
        error_messages = {
        }
