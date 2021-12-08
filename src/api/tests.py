# Django Libraries
from django.test import TestCase
from django.urls import reverse

# Rest Framework Libraries
from rest_framework.test import APITestCase
from rest_framework import status

# App Modules
from core.models import CoreConfig
from isssys.models import IssSys

# Python Libraries
import json
import string
import random

# IssBot Test Cases start here

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class UserTestCase(APITestCase):
    """
    We will test multiple senarios that can be used for our Restful APIs.
    """

    def create_user(self):
        username = id_generator()
        password = id_generator(size=15)
        email = username + '@isstech.io'
        payload = {
            'username': username,
            'password1': password,
            'password2': password,
            'email': email,}
        response = self.client.post(reverse('api:rest_register'), payload, format='json')
        return(response)

    def verify_token(self,token):
        payload = {
            'token': token
        }
        response = self.client.post(reverse('api:token_verify'), payload, format='json')
        return(response)

    def test_create_new_user(self):
        """
        We will register a new user/device
        """
        response = self.create_user()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_verify_token(self):
        """
        We test if we can verify a token
        """
        user = self.create_user()
        token = user.data['access_token']
        response = self.verify_token(token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_refresh_token(self):
        """
        We test if refresh function is working as expected
        """
        user = self.create_user()
        token = user.data['refresh_token']
        payload = {
            'refresh': token
        }
        response = self.client.post(reverse('api:token_refresh'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CoreConfigTest(APITestCase):
    """
    We will test our Core Configuration for all our devices.
    """

    def create_user(self):
        username = id_generator()
        password = id_generator(size=15)
        email = username + '@isstech.io'
        payload = {
            'username': username,
            'password1': password,
            'password2': password,
            'email': email,}
        response = self.client.post(reverse('api:rest_register'), payload, format='json')
        return(response)

    def test_create_device_information(self):
        """
        We are testing to create data via RestAPI and verify the data has been created
        """
        hostname = self.create_user()
        token = hostname.data['access_token']
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
            }
        payload = {
            'hostname': hostname.data['user']['username'],
            'fqdn': hostname.data['user']['username'] + '@isstech.io',
            'ipv4': '1.2.3.4'
        }

        url = '/api/v1/core/'

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        post = self.client.post(url, payload, format='json')
        self.assertEqual(post.status_code, status.HTTP_201_CREATED)

        get = self.client.get(url)
        self.assertEqual(get.status_code, status.HTTP_200_OK)

        queryset = CoreConfig.objects.all()
        self.assertTrue(queryset, 1)

class IssSysTest(APITestCase):
    """
    We will test our IssSys Model together with CoreConfig module.
    This will simulate number of updates for a Device
    """


    def create_user(self):
        username = id_generator()
        password = id_generator(size=15)
        email = username + '@isstech.io'
        payload = {
            'username': username,
            'password1': password,
            'password2': password,
            'email': email,}
        response = self.client.post(reverse('api:rest_register'), payload, format='json')
        return(response)

    def create_device_information(self):
        hostname = self.create_user()
        token = hostname.data['access_token']
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
            }
        payload = {
            'hostname': hostname.data['user']['username'],
            'fqdn': hostname.data['user']['username'] + '@isstech.io',
            'ipv4': '1.2.3.4'
        }
        #print(reverse('api:core'))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        self.client.post('/api/v1/core/', payload, format='json')
        response = self.client.get('/api/v1/core/')
        return(json.loads(json.dumps(response.data)), token)

    def test_create_updates(self):
        """
        We will simulate number of updates
        """
        ### Get host information ###
        host, token = self.create_device_information()

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
            }

        payload={'isssys_version': '0.1',
                'total_updates': '15',
                'security_updates': '0',
                'priority1_updates': '3',
                'priority2_updates': '2',
                'priority3_updates': '2',
                'priority4_updates': '5',
                'priority5_updates': '3',
                'host_id': host[0]['id']}

        url = '/api/v1/isssys/'

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        post = self.client.post(url, payload, format='json')
        self.assertEqual(post.status_code, status.HTTP_201_CREATED)

        get = self.client.get(url)
        self.assertEqual(get.status_code, status.HTTP_200_OK)

        queryset = IssSys.objects.all()
        self.assertTrue(queryset, 1)
