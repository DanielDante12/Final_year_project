from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission


# class CustomUser(AbstractUser):
#     groups = models.ManyToManyField(Group, related_name='customuser_groups')
#     user_permissions = models.ManyToManyField(
#         Permission, related_name='customuser_permissions')
#     FARMER = 'farmer'
#     COMMUNICATION_OFFICER = 'comm_officer'
#     ADMIN = 'admin'

#     ROLE_CHOICES = [
#         (FARMER, 'Farmer'),
#         (COMMUNICATION_OFFICER, 'Communication Officer'),
#         (ADMIN, 'Admin'),
#     ]

#     role = models.CharField(
#         max_length=20, choices=ROLE_CHOICES, default=FARMER)
#     isApproved = models.BooleanField(blank=True, null=True)

#     def __str__(self):
#         return self.username


class User(AbstractUser):  
    username = models.CharField(null=True, unique=True, max_length=100)
    email = models.EmailField(unique=True)
    OTP = models.CharField(max_length=100, null=True, blank=True)
    FARMER = 'farmer'
    photo = models.FileField(upload_to="static/uploads/photos", null=True, blank=True)
    is_approved = models.BooleanField(default = False)
    contact = models.CharField(max_length=15, default="no contact")
    COMMUNICATION_OFFICER = 'comm_officer'
    
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (FARMER, 'Farmer'),
        (COMMUNICATION_OFFICER, 'Communication Officer'),
        (ADMIN, 'Admin'),
    ]

    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default=FARMER)
    
    REQUIRED_FIELDS = []
    
    USERNAME_FIELD = "username"


class AgriculturalOrganization(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    contact = models.CharField(max_length=15, default="+256771183868")
    Licence = models.FileField(upload_to="static/uploads/licences", null = True, blank=True)
    communicationOfficer = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='communication_officer', default=1)
    status=models.CharField(max_length=20, default='pending')

    def __str__(self):
        return self.name

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otps', default=1)
    organization = models.ForeignKey(AgriculturalOrganization, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created= models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)
    
    def __str__(self):
        return f'OTP for {self.user}'

class Pest(models.Model):
    information=models.ForeignKey(Information, on_delete=models.CASCADE, related_name='information')
    name = models.CharField(max_length=50)
    description = models.TextField()
    preferredHabitat = models.TextField()
    commonDamage = models.TextField()
    lifecycle = models.TextField()
    image = models.FileField()
    # pestControl = models.ForeignKey(
    #     Information, on_delete=models.CASCADE, related_name='pest_control')

    def __str__(self):
        return self.name

  
class Crop(models.Model):
    type = models.CharField(max_length=50)
    variety = models.CharField(max_length=100)
    pests = models.ManyToManyField(Pest, related_name='pest')

    def __str__(self):
        
        return self.type 
class Information(models.Model):
    # viewers = models.ManyToManyField(User, related_name='viewers')
    description = models.TextField()
    instructions = models.TextField()
    tutorial = models.FileField(upload_to="static/uploads/tutorials", null = True)
    category = models.CharField(max_length=40)
    # frequency = models.CharField(null=True, blank=True, max_length=50)
    # controltiming = models.CharField(null=True, blank=True, max_length=50)
    crop=models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='crop')
    
    communicationOfficer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='organization_communication_officer')

    def __str__(self):
        return self.description
    
 
class Equipment(models.Model):
    information=models.ForeignKey(Information, on_delete=models.CASCADE, related_name='information')
    # technique = models.ForeignKey(
    #     PostHarvestTechnique, on_delete=models.CASCADE, related_name='post_harvest_technique')
    name = models.CharField(max_length=50)
    description = models.TextField()
    instruction = models.TextField()
    image = models.FileField()

    def __str__(self):
        return self.name    


# class PostHarvestTechnique(models.Model):
#     name = models.CharField(max_length=50)
#     crop = models.ForeignKey(
#         Crop, on_delete=models.CASCADE, related_name='crop')

#     def __str__(self):
#         return self.name



class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created = models.DateTimeField(auto_now_add=True)
    image=models.FileField(upload_to='static/upload/posts', null=True, blank=True)

    def __str__(self):
        return self.title
    
    
class Notification(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    creator=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post=models.ForeignKey(Post, on_delete=models.CASCADE,null=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    created = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    # subject = models.CharField(max_length=200)
    body = models.TextField()
    sent = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.body[0:20]
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'