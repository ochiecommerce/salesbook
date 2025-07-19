from django.db import models
from django.contrib.auth.models import User


class Phonebook(models.Model):
    creator = models.ForeignKey(User,on_delete=models.CASCADE,related_name='my_phonebooks',null=True)
    name = models.CharField(max_length=63)
    description = models.CharField(max_length=255, null=True)

    @property
    def contact_count(self):
        return len(self.contacts.all())
    

class ReadPermission(models.Model):
    user = models.ForeignKey(User,related_name='read_permissions',on_delete=models.CASCADE)
    phonebook = models.ForeignKey(Phonebook,related_name='read_permissions',on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = (('user','phonebook'),)

class WritePermission(models.Model):
    user = models.ForeignKey(User,related_name='write_permissions',on_delete=models.CASCADE)
    phonebook = models.ForeignKey(Phonebook,related_name='write_permissions',on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user','phonebook'),)

class AlterPermission(models.Model):
    user = models.ForeignKey(User,related_name='alter_permissions',on_delete=models.CASCADE)
    phonebook = models.ForeignKey(Phonebook,related_name='alter_permissions',on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user','phonebook'),)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=16, unique=True)
    phonebook = models.ForeignKey(Phonebook,on_delete=models.CASCADE,related_name='contacts',null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    @property
    def tags(self):
        return Tag.objects.filter(tagged_app='contacts',tagged_id=self.phone)

    def __str__(self):
        return f"{self.name} ({self.phone})"

    @property
    def latest_log(self):
        if (size := len(self.notes.all())) > 0:  # type: ignore
            return self.notes.all()[size - 1].feedback_title  # type: ignore
        return ""
    
class Reminder(models.Model):
    title = models.CharField(max_length=255)
    due = models.DateTimeField()
    creator = models.ForeignKey(User,related_name='reminders',on_delete=models.CASCADE)

class Tag(models.Model):
    tagger_app = models.CharField(max_length=63)
    tagged_app = models.CharField(max_length=63)
    tagger_id = models.CharField(max_length=63)
    tagged_id= models.CharField(max_length=63)
    
class Column(models.Model):
    name = models.CharField(max_length=255)
    phonebook = models.ForeignKey(Phonebook, related_name='columns', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('name','phonebook'))

class Attribute(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE,related_name='attributes')
    column = models.ForeignKey(Column,on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    class Meta:
        unique_together = (('contact','column'))

class Note(models.Model):
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, related_name="notes",null=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')  # type: ignore
    note = models.TextField()
    title = models.CharField(max_length=96)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interaction with {self.contact.name} by {self.user.username}"  # type: ignore

