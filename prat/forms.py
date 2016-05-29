from django.contrib.auth.models import User

from django.forms import (Form, ModelForm, CharField, PasswordInput,
    ImageField, EmailField, ValidationError, DateField,
    SelectDateWidget, ChoiceField, ModelChoiceField)

from prat.models import (Task, Category, Ong, UserGroup, UserGroupMembership,
    Theme, UserThemes)


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
        fields = ['name', 'category', 'ong']
        error_messages = {
            'category': {
                'required': ("You need to pick a category! "),
            },
            'ong': {
                'required': ("You need to pick an ONG to donate to! "),
            }
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
    ong = ChoiceField(
        choices=((ong.pk, ong.name) for ong in Ong.objects.all()),
        required = True
        )
    theme = ModelChoiceField(queryset=Theme.objects.all())

    def __init__(self, request, *args, **kwargs):
        self.request = request

        default_theme = Theme.objects.filter(name='Default').first()
        bought_themes = UserThemes.objects.filter(user=request.user)
        available_themes = []
        available_themes.append((default_theme.pk, default_theme.name))
        for bought_theme in bought_themes:
            theme = bought_theme.theme
            available_themes.append((theme.pk, theme.name))

        super(EditTaskForm, self).__init__(*args, **kwargs)
        self.fields['theme'] = ChoiceField(choices = available_themes)


class CreateGroupForm(ModelForm):
    class Meta:
        model = UserGroup
        fields = ['name', 'description']
        error_messages = {
        }


class JoinGroupForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(JoinGroupForm, self).__init__(*args, **kwargs)
        self.fields['user_group_task'].queryset = Task.objects.filter(
            owner=user)

    class Meta:
        model = UserGroupMembership
        fields = ['user_group_task']
        labels = {
            'user_group_task': "Select which one of your chains you'd like to add to this group."
        }
        error_messages = {
            'user_group_task': {
                'unique': ("You can't join with the same task! "),
            }
        }


class AddGroupCommentForm(Form):
    comment = CharField(max_length=500, required=True)


class ShowCategoryTopForm(Form):
    category = ChoiceField(
        choices=([(None, '')] + [(cat.pk, cat.name) for cat in Category.objects.all()]),
        required=True)
