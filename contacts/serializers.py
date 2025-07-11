from rest_framework import serializers
from .models import Contact, InteractionLog, Invite, Membership

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            "name",
            "id_number",
            "employment_number",
            "employer_name",
            "phone",
            "status",
        ]
        read_only_fields = ['created_at', 'updated_at']


class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InteractionLog
        fields = ['contact','user',]

class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = ['user','group']

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['user','group']

