from django.db import models
from user.models import User
from djongo import models

class Contact(models.Model):
    # To retrieve contacts for a specific user, filter the contacts collection by the user's identifier.
    belong_to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts")

    # the is_user field will be NULL for contacts who aren't users. For contacts who are also users, 
    # this field will contain a reference to their user id
    is_user = models.OneToOneField(User, on_delete=models.SET_NULL, related_name="user_contacts", null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, null=True, blank=True)
    dob = models.DateField(null=True)
    address = models.CharField(max_length = 100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField()
    tags = models.JSONField(blank=True, null=True, default=list)
    avatar = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    # set first name and last name as "toString"
    def __str__(self):
        return f"{self.first_name} {self.last_name}"