from django.urls import path
from . import views
from .views import SignupView
urlpatterns=[
    path("", views.post),
    path('signup/',SignupView.as_view(), name='signup' ),
    path('addinfor/',views.addInformation, name='addInformation' ),
    path('verify-code/', views.verify_code, name='verify_code'),
    path('updateOrganization/<int:pk>', views.updateOrganization, name='update_organization'),
    path('viewInformation/<int:pk>', views.viewInformation, name='view_information'),
    path('organizations/', views.view_all_organizations, name='view_all_orgizations'),
    path('approveOrganization/<str:pk>',views.approve_organization, name='approve_organization'),
    path('notifications/', views.list_notifications, name='list_notifications'),
    path('createnotifications/', views.create_notification, name='create_notification'),
    path('sendmessages/', views.send_message, name='send_message'),
    path('messages/', views.list_messages, name='list_messages'),
    path('createPost/', views.create_post, name="create_post"),
    path('getPost/<str:pk>', views.getPost, name="view_post"),
    path('posts/<int:post_id>/addcomment/', views.create_comment, name='add_comment'),
    path('posts/<int:post_id>/viewcomment/', views.view_comment, name='view_comment'),
]