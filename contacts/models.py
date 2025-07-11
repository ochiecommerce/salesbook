from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    name = models.CharField(max_length=64)
    admin = models.ForeignKey(User,on_delete=models.CASCADE)


class Contact(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("contacted", "Contacted"),
        ("converted", "Converted"),
        ("not_interested", "Not Interested"),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=16, unique=True)
    id_number = models.IntegerField(null=True)
    employment_number = models.IntegerField(null=True)
    employer_name = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    ability = models.FloatField(default=0.0)
    duration_of_contract = models.IntegerField(default=120)

    def __str__(self):
        return f"{self.name} ({self.phone})"

    @property
    def latest_log(self):
        if (size := len(self.interactions.all())) > 0:  # type: ignore
            return self.interactions.all()[size - 1].feedback_title  # type: ignore
        return ""


class InteractionLog(models.Model):
    feedback_title_choices = [
        ("not_available", "Not Available"),
        ("not_picking", "Not Picking"),
        ("hanged_up", "Hanged Up"),
        ("do_not_call", "Do Not Call"),
        ("not_interested", "Not Interested"),
        ("retired", "Retired"),
        ("call_later", "Call Later"),
        ("prospective", "Prospective"),
    ]
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, related_name="interactions"
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # type: ignore
    feedback_title = models.CharField(
        max_length=64, choices=feedback_title_choices, default="not_available"
    )
    notes = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interaction with {self.contact.name} by {self.user.username}"  # type: ignore


class Invite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="invites"
    )
    company = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="invites")

class Membership(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="memberships"
    )
    company = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="memberships")