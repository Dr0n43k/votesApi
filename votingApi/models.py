import os
from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.utils.safestring import mark_safe
from djangoProject import settings


def path_and_rename(instance, filename):
    upload_to = ''
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(instance.fullname, ext)
    return os.path.join(upload_to, filename)


class Person(models.Model):
    fullname = models.CharField(max_length=100)
    photo = models.ImageField(upload_to=path_and_rename)
    age = models.IntegerField()
    biography = models.TextField()

    def __str__(self):
        return self.fullname

    def img_preview(self):
        return mark_safe(f'<img src = "{self.photo.url}" />')


@receiver(post_delete, sender=Person)
def delete_file_hook(sender, instance, using, **kwargs):
    full_file = os.path.join(settings.BASE_DIR, str(instance.photo))
    if os.path.exists(full_file):
        os.remove(full_file)


class Voting(models.Model):
    title = models.CharField(max_length=30)
    start = models.DateTimeField()
    stop = models.DateTimeField()
    max_votes = models.IntegerField(default=0)
    persons = models.ManyToManyField(Person)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class PersonVotes(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE)
    votes = models.IntegerField()

    def __str__(self):
        return f"{self.person.fullname}_{self.voting.title}"


@receiver(post_save, sender=Voting)
def create_person_votes(sender, instance, **kwargs):
    for i in instance.persons.all():
        if PersonVotes.objects.filter(person=i, voting=instance):
            continue
        PersonVotes.objects.create(
            person=i,
            voting=instance,
            votes=0
        )