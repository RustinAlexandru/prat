
from django.db import models
from django.contrib.auth.models import User

# More
import pytz
from timezone_field import TimeZoneField

class UserProfile(models.Model):
    """model class for a user profile, 1-to-1 relationship with User model,
       stores additional information about a user (timezone, language,
       display name, etc)
    """

    # Properties
    first_name = models.CharField(max_length = 100, blank = True, null = True)
    last_name  = models.CharField(max_length = 100, blank = True, null = True)
    birthday   = models.DateField(null = True, blank = True)
    gender = models.CharField(max_length = 1,
        choices = (
            ('M', 'Male'),
            ('F', 'Female')
        ), blank = True, null = True)
    avatar = models.ImageField(upload_to = 'images/avatars/',
        default = 'images/avatars/no_avatar.jpg', blank = True, null = True)

    # Relations
    user = models.OneToOneField(User, on_delete = models.CASCADE,
                    related_name = 'profile', verbose_name = 'user')


class Task(models.Model):
    """model class for a task, M-to-1 relationship with UserProfile model,
       1-to-1 with UserGroup model, 1-to-M with UserTaskActivity model,
       M-to-1 with Category model, M-to-1 with UserTaskEvidence model,
       a task is set and completed by a user
    """

    # Properties
    name = models.CharField(max_length = 100, null = False)
    sessions_record = models.IntegerField(default = 0, null = False)
    sessions_total = models.IntegerField(default = 0, null = False)
    experience_total = models.IntegerField(default = 0, null = False)
    experience_reward = models.IntegerField(default = 10, null = False)
    experience_sessions = models.IntegerField(default = 1, null = False)
    experience_multiplier = models.FloatField(default = 1.2, null = False)
    points_total = models.IntegerField(default = 0, null = False)
    points_reward = models.IntegerField(default = 1, null = False)
    points_sessions = models.IntegerField(default = 1, null = False)
    points_multiplier = models.FloatField(default = 1, null = False)
    last_update = models.DateTimeField(auto_now_add = True, null = False)
    # more to come

    # Relations
    category = models.ForeignKey('Category', verbose_name = 'category',
                    related_name = 'tasks', on_delete = models.CASCADE)
    owner = models.ForeignKey(User, verbose_name = 'owner',
                    related_name = 'tasks', on_delete = models.CASCADE)


class PredefinedTask(models.Model):
    """model class for predefined tasks, M-to-1 relationship with Category model,
       a set of predefined tasks (ex: workout, floss, take vitamins)
    """

    # Properties
    # later

    # Relations
    category = models.ForeignKey('Category', verbose_name = 'category',
                    related_name = 'predef_tasks', on_delete = models.CASCADE)


class UserGroup(models.Model):
    """model class for a group of users, M-to-M relationship with UserProfile
       model, 1-to-M with Comment model,
       a group of users shares a task
    """

    # Properties
    name = models.CharField(max_length = 100)


    # Relations
    task = models.OneToOneField('Task', related_name = 'group',
                    verbose_name = 'task', null = False)
    users = models.ManyToManyField(User) # might do a through model

class UserGroupComment(models.Model):
    """model class for a comment on a group chat, M-to-1 relationship with
       UserGroup model, M-to-1 with User
       each group has multiple comments
    """

    # Properties
    text = models.CharField(max_length = 200)
    date_added = models.DateTimeField(auto_now_add = True)


    # Relations
    group = models.ForeignKey('UserGroup', related_name = 'comments',
                    verbose_name = 'group', on_delete = models.CASCADE)
    user  = models.ForeignKey(User, related_name = 'comments',
                    verbose_name = 'user', on_delete = models.CASCADE)

    def __unicode__(self):
        return u'{} @ {}'.format(self.author, self.date_added)


class Theme(models.Model):
    """model class for a theme, 1-to-M relationship with UserThemes model,
       a theme is a set of preferences (ex: chain appearance, colours, etc)
    """

    # Properties
    name = models.CharField(max_length = 100)


class UserThemes(models.Model):
    """model class for user-themes, M-to-1 relationship with Theme model,
       M-to-1 with user,
       associative entity, each user has multiples themes he can pick
    """

    # Relations
    theme = models.ForeignKey('Theme', on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)


class Achievement(models.Model):
    """model class for an achievement, M-to-M relationship with UserProfile model,
       an achievement is earned by a user (ex: )
    """

    name = models.CharField(max_length = 100)


class Category(models.Model):
    """model class for a category, 1-to-M relationship with PredefinedTask model,
       1-to-M with Task model,
       a classification of tasks (ex: health, study, etc)
    """

    name = models.CharField(max_length = 100)


class UserTaskActivity(models.Model):
    """model class for a user-task activity, M-to-1 relationship with Task model,
       tracks daily progress for a user's task
    """

    # Properties
    date_created = models.DateTimeField(auto_now_add = True, null = False)
    experience_gained = models.IntegerField(default = 0, null = False)
    points_gained = models.IntegerField(default = 0, null = False)

    # Relations
    task = models.ForeignKey('Task', verbose_name = 'task',
                    on_delete = models.CASCADE)
    user = models.ForeignKey(User, verbose_name = 'user',
                    on_delete = models.CASCADE)
