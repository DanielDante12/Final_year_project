from rest_framework.serializers import ModelSerializer
from django.db import models
from .models import AgriculturalOrganization, Information, Notification, Message, Post, Comment, OTP

class AgriculturalOrganizationSerializer(ModelSerializer):
    class Meta:
        model = AgriculturalOrganization
        fields= "__all__"
        
class InfromationSerilizer(ModelSerializer):
    class Meta:
        model= Information
        fields= ['viwers','description','instructions','category','communicationOfficer']
        
class UpdateOrganizationSerializer(ModelSerializer):
    class Meta:
        model=AgriculturalOrganization
        fields= "__all__"
        
class ViewInformationSerializer(ModelSerializer):
    class Meta:
        model = Information
        fields = ['id', 'viewers', 'description', 'instructions', 'tutorial', 'category', 'frequency', 'controltiming', 'communicationOfficer']
class ViewAllOrganizationsSerializer(ModelSerializer):
    class Meta:
        model=AgriculturalOrganization
        fields="__all__"
        
class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'recipient', 'created', 'read']

class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'subject', 'body', 'sent', 'read']
        
class PostSerializer(ModelSerializer):
    class Meta:
        model=Post
        fields = ['id', 'title', 'content', 'author', 'created']
        read_only_fields = ['author', 'created']
        
class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created']
        read_only_fields = ['author', 'created']
        
class OTPValidationSerializer(ModelSerializer):
    class Meta:
        model=OTP
        fields=['otp_code']