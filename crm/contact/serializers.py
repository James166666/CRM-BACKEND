from rest_framework import serializers
from contact.models import Contact
from django.core.files.base import ContentFile
from .models import User
import base64
import six
import uuid

class Base64ImageField(serializers.ImageField):
    """
    A Django Rest Framework Field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.
    """

    def to_internal_value(self, data):
        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension
    
    def to_representation(self, value):
        if not value or not value.path:
            return None

        with open(value.path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')




class ContactSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(max_length=None, use_url=True, required=False, allow_null=True)
    tags = serializers.ListField(child=serializers.CharField(max_length=100), required=False, allow_null=True)
    dob = serializers.DateField(required=False, allow_null=True)

    
    class Meta:
        model=Contact
        fields=('id', 'belong_to_user', 'is_user', 'first_name', 'last_name', 'gender', 'dob', 'address', 'city',
                'state', 'postcode', 'phone', 'email', 'tags', 'avatar')
        read_only_fields = ['belong_to_user']
    
    def create(self, validated_data):
        contact = Contact(
            email=validated_data['email'],
            belong_to_user=validated_data['belong_to_user'],
            is_user=validated_data.get('is_user'),
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            dob=validated_data.get('dob'),
            address=validated_data.get('address'),
            city=validated_data.get('city'),
            state=validated_data.get('state'),
            postcode=validated_data.get('postcode'),
            phone=validated_data.get('phone'),
            gender=validated_data.get('gender'),
            tags=validated_data.get('tags', []),
            avatar=validated_data.get('avatar')
        )
        contact.save()
        return contact