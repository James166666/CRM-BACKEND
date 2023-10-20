"""
URL configuration for crm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from contact import views
from user import user_views
from django.conf import settings
from django.conf.urls.static import static
from user.user_views import Login, ResetPassword, Logout, UserProfileUpdate, RetrieveUserByPK, CreateUser, RetrieveLoggedInUser, ResetPasswordWithoutOld
from contact.views import ContactListView, ContactDetailView
from trello.views import TaskCreateView, ColumnCreateView
from event.views import EventCreateView, EventRetrieveUpdateDestroyView
from notes.views import NoteView

urlpatterns = [
    path('login/', Login.as_view(), name='user_login'),
    path('user/resetpassword/', ResetPassword.as_view(), name='reset-password'),
    path('user/resetpasswordWithoutOld/', ResetPasswordWithoutOld.as_view(), name='reset-password-without-old'),
    path('logout/', Logout.as_view(), name='logout'),
    path('user/profile/', UserProfileUpdate.as_view(), name='update-profile'),
    path('user/<int:pk>/', RetrieveUserByPK.as_view(), name='retrieve-user'),
    path('user/', CreateUser.as_view(), name='create-user'),
    path('user/me/', RetrieveLoggedInUser.as_view(), name='retrieve-logged-in-user'),
    path('contacts/', ContactListView.as_view(), name='contact-list'),
    path('contacts/<int:pk>/', ContactDetailView.as_view(), name='contact-detail'),
    path('trello/column/', ColumnCreateView.as_view(), name='trello-column'),
    path('trello/task/', TaskCreateView.as_view(), name='trello-task'),
    path('event/', EventCreateView.as_view(), name='event'),
    path('event/<int:pk>/', EventRetrieveUpdateDestroyView.as_view(), name='event-update'),
    path('note/', NoteView.as_view(), name='user-note'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
