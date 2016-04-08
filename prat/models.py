
from django.db import models
from django.contrib.auth.models import User
import pytz
from timezone_field import TimeZoneField


class UserProfile(models.Model):
    """model class for a user profile, 1-to-1 relationship with User model, stores additional information about a user (timezone, language, display name, etc)
    """

    user = models.OneToOneField(User)
    # https://github.com/mfogel/django-timezone-field
    timezone = TimeZoneField()
    achievements = models.ManyToManyField(Achievement)


class Task(models.Model):
    """model class for a task, M-to-1 relationship with UserProfile model, 1-to-1 with UserGroup model, 1-to-M with UserTaskActivy model, M-to-1 with Category model, M-to-1 with UserTaskEvidence model,
        a task is set and completed by a user
    """

    task_name = models.TextField()
    task_category = models.ForeignKey(Category)
    user_task_evidence = models.ForeignKey(UserTaskEvidence)


class PredefinedTask(models.Model):
    """model class for predefined tasks, M-to-1 relationship with Category model,
        a set of predefined tasks (ex: workout, floss, take vitamins)
    """
    predefined_task_category = models.ForeignKey(Category)


class UserGroup(models.Model):
    """model class for a group of users, M-to-M relationship with UserProfile model,
        1-to-M with Comment model,
        a group of users shares a task
    """

    group_name = models.TextField()
    group_members_count = models.IntegerField()
    task = models.OneToOneField(Task)
    users = models.ManyToManyField(UserProfile)


class UserTaskEvidence(models.Model):
    """model class for a user-task evidence, 1-to-M relationship with Task model,
    associative entity keeps a total of points, experience, progress for each user's task
    """


class UserGroupComment(models.Model):
    """model class for a comment on a group chat, M-to-1 relationship with UserGroup model, M-to-1 with User
    each group has multiple comments
    """

    text = models.TextField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    user_group = models.ForeignKey(UserGroup)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return u'{} @ {}'.format(self.author, self.date_added)


class Theme(models.Model):
    """model class for a theme, 1-to-M relationship with UserThemes model,
       a theme is a set of preferences (ex: chain appearance, colours, etc)
    """

    theme_name = models.CharField()


class UserThemes(models.Model):
    """model class for user-themes, M-to-1 relationship with Theme model,
    M-to-1 with user,
    associative entity, each user has multiples themes he can pick
    """

    theme = models.ForeignKey(Theme)
    user = models.ForeignKey(User)


class Achievement(models.Model):
    """model class for an achievement, M-to-M relationship with UserProfile model,
    an achievement is earned by a user (ex: )
    """

    achievement_name = models.CharField()


class Category(models.Model):
    """model class for a category, 1-to-M relationship with PredefinedTask model, 1-to-M with Task model,
    a classification of tasks (ex: health, study, etc)
    """

    category_name = models.CharField()


class UserTaskActivy(models.Model):
    """model class for a user-task activity, M-to-1 relationship with Task model,
    tracks daily progress for a user's task
    """

    task = models.ForeignKey(Task)
