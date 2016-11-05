from django.conf import settings
from django.contrib.auth.models import User
from .models import Instructor
import logging
import urllib.request
import json

# Get an instance of a logger
logger = logging.getLogger('django')

class GSigninBackend(object):
   
    def authenticate(self, token=None):
        CLIENT_ID = "410381470-aviccs0f691gm6eqin9k9opo3ko5sji6.apps.googleusercontent.com"
        validation_url = "https://www.googleapis.com/oauth2/v3/tokeninfo?id_token="
        data = json.loads(urllib.request.urlopen(validation_url + token).read().decode('utf-8'))
        if data['aud'] == CLIENT_ID:
            if data['iss'] in ['accounts.google.com', 'https://accounts.google.com']:
                logger.info(data)
                try:
                    user = User.objects.get(username=data['email'])
                except User.DoesNotExist:
                    user = User(first_name=data['given_name'], last_name=data['family_name'], username=data['email'])
                    instructor = Instructor()
                    user.save()
                    instructor.user_id = user.id
                    instructor.save()
                return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None