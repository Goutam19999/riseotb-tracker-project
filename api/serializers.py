from django.contrib.auth.models import Group, User
from rest_framework import serializers

from scmtracker.models import ModerationStream, PostModeration



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups','first_name','last_name']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class UserdataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModerationStream
        fields = "__all__"

class AgreementSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostModeration
        fields = [
            "id",
            "title",
            "content",          
            "status",
            #read only
            "created_by",
            "participants",
            "effective_date",
            "expiry_date",
        ]
        extra_kwargs = {
            "created_by": {"read_only" : True},
            "participants": {"read_only" : True},
            "effective_date": {"read_only" : True},
            "expiry_date": {"read_only" : True},
        }

    def validate(self,data):
        data["created_by"] = self.context["request"].user
        return data
    
# class PostPublishSerializer(serializers.Serializer):
#     id = serializers.IntegerField()   

