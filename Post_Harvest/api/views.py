from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import AgriculturalOrganization, OTP, Information,Notification, Message, Post
from .serializers import AgriculturalOrganizationSerializer, InfromationSerilizer, UpdateOrganizationSerializer,ViewInformationSerializer, ViewAllOrganizationsSerializer,NotificationSerializer, MessageSerializer, PostSerializer
from django.core.mail import send_mail
import random
import logging

# endpoint that allows a communication officer to signup, submits organization information and genrates OTP which is stored in the db

logger = logging.getLogger(__name__)


class SignupView(APIView):
    def post(self, request):
        serializer = AgriculturalOrganizationSerializer(data=request.data)
        if serializer.is_valid():
            organization = serializer.save()

            # Generate OTP
            otp = str(random.randint(100000, 999999))

            # Save OTP to the database
            OTP.objects.create(
                organization=organization, otp=otp
            )

            try:
                # Send OTP via email
                send_mail(
                    'Your OTP Code',
                    f'Your OTP code is {otp}',
                    'ofwonodani12@gmail.com',
                    [organization.email],
                    fail_silently=False,
                )
            except Exception as e:
                logger.error(
                    f'Failed to send OTP email to {organization.email}: {e}')
                return Response({'error': 'Failed to send OTP email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'message': 'Organization registered successfully, OTP sent to email'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def addInformation(request):
    try:
        serializer = InfromationSerilizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Information added successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


api_view(['POST'])


def verify_code(request):
    if request.method == 'POST':
        # Assuming the code entered by the user is sent in the request data
        entered_code = request.POST.get('code', '')

        # Here you would typically retrieve the code sent to the user's email
        # from your database based on the user's email or a unique token
        stored_code = "123456"  # Example stored code for demonstration

        if entered_code == stored_code:
            # Code matches, verification successful
            return JsonResponse({'verified': True})
        else:
            # Code doesn't match, verification failed
            return JsonResponse({'verified': False}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


# Endpoint for updating Organization information
@api_view(['GET', 'PATCH'])


def updateOrganization(request, pk):
    try:
        organization = AgriculturalOrganization.objects.get(id=pk)
       
    except AgriculturalOrganization.DoesNotExist:
        return Response({'error': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == "PATCH":
        updated = UpdateOrganizationSerializer(
            organization, data=request.data, partial=True)
        if updated.is_valid():
            updated.save()
            return Response(updated.data, status=status.HTTP_202_ACCEPTED)
        return Response(updated.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "GET":
        serializer = AgriculturalOrganizationSerializer(organization)
        return Response(serializer.data, status=status.HTTP_200_OK)

    updated = UpdateOrganizationSerializer(organization)
    return Response(updated.data)


def post(req):
    return render(req, "api/index.html")

#endpoint for retrieving information on practicess

@api_view(["GET"])
def viewInformation(request, pk):
    try:
        information=Information.objects.get(id=pk)
    except Information.DoesNotExist:
        return Response({"errors": "Information not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer=ViewInformationSerializer(information)
    return Response(serializer.data,status=status.HTTP_200_OK)

    
#endpoint for admin to view all organizations
@api_view(["GET"])
@permission_classes([IsAdminUser])
def view_all_organizations(request):
    try:
        organizations=AgriculturalOrganization.objects.all()
    except AgriculturalOrganization.DoesNotExist:
        return Response({"errors": "Organization not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer=ViewAllOrganizationsSerializer(organizations, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

#enpoint for approving an organization by an admin
@api_view(["GET","PATCH"])
@permission_classes([IsAdminUser])
def approve_organization(request, pk):
    try:
        organization = AgriculturalOrganization.objects.get(id=pk)
    except AgriculturalOrganization.DoesNotExist:
        return Response({"error": "Organization not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if 'status' in request.data:
        organization.status = request.data['status']
        organization.save()
        if request.method=="PATCH":
             isApproved = AgriculturalOrganizationSerializer(organization)
             return Response(isApproved.data, status=status.HTTP_200_OK)
         
    else:
        return Response({"error": "Status not provided"}, status=status.HTTP_400_BAD_REQUEST)
    
#endpoint for creating aand retrieving notifications
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_notification(request):
    serializer = NotificationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_notifications(request):
    notifications = Notification.objects.filter(recipient=request.user)
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

#endpoint for sending and receiving messages

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(sender=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_messages(request):
    received_messages = Message.objects.filter(recipient=request.user)
    serializer = MessageSerializer(received_messages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


#endpoint for creating and retrieving posts
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    serializer=PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user)
        return Response({'message':"Post created successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getPost(request, pk):
    try:
        post=Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer= PostSerializer(post)
    return Response(serializer.data,status=status.HTTP_200_OK)
    

