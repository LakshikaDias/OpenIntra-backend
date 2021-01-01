import json
from django.test import tag
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.viewsets import reverse
from usermgt.models import User


def createUser(key=1):
    username = 'testuser{}'.format(key)
    password = 'testuserpw{}'.format(key)
    email = 'testuser{}@email.com'.format(key)
    user = User.objects.create_user(username, email, password)
    return user


@tag('user')
class UserEndpointTests(APITestCase):
    def createUserAndLogin(self, username='testinguser', password='testinguserpw', email='testinguser@email.com'):
        user = User.objects.create_user(username, email, password)
        loginPostData = {
            'email': email,
            'password': password
        }
        url = reverse('login')
        response = self.client.post(url, loginPostData, format='json')
        jsonResponse = json.loads(response.content)
        accessToken = jsonResponse['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + accessToken)

    def tearDown(self):
        """Clear credentials at the end of each test case"""
        self.client.credentials()

    # GET user/
    def test_retrieveUsers(self):
        # Populate the database with sample data
        createUser(1)

        # Try without logging in. It should give a 401 error
        url = reverse('user-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Try after loggin in. This time it should be successful.
        self.createUserAndLogin()
        response = self.client.get(url, format='json')
        # 200 status code. Total users = 2. (Created user + logged in user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # GET user/xxx/
    def test_retrieveOneUser(self):
        # Populate the database with sample data
        user = createUser(1)

        # Unauthenticated request
        url = reverse('user-detail', args=[user.username])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authenticated request
        self.createUserAndLogin()
        response = self.client.get(url, format='json')
        # 200 status code and proper response content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], user.username)
        self.assertEqual(response.data['email'], user.email)

    # POST user/
    def test_createUser(self):
        # data to send to the server
        postData = {
            'username': 'XX_USERNAME_XX',
            'password': 'XX_PASSWORD_XX',
            'email': 'xx_email_xx@email.com'
        }

        # Unauthenticated request
        url = reverse('user-list')
        response = self.client.post(url, postData, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authenticated request
        self.createUserAndLogin()
        response = self.client.post(url, postData, format='json')
        # Retrieve created user from DB
        user = User.objects.filter(username=postData['username'])[0]
        # 201 status code, and the created user has correct values set.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.username, postData['username'])

    # PUT user/xxx/
    def test_updateUser(self):
        # sample data
        user = createUser(1)
        user.role = 'Engineer'
        user.department = 'QA Department'
        user.save()

        # data to send to the server
        putData = {
            'username': user.username,
            'email': user.email,
            'role': 'Manager',
            'department': 'Enterprise Applications Department'
        }

        # Unauthenticated request
        url = reverse('user-detail', args=[user.username])
        response = self.client.put(url, putData, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authenticated request
        self.createUserAndLogin()
        response = self.client.put(url, putData, format='json')
        # Get the updated user object
        userFromDb = User.objects.get(username=user.username)
        # Verify that userFromDb was updated
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(userFromDb.role, putData['role'])
        self.assertEqual(userFromDb.department, putData['department'])

    # DELETE user/xxx/
    def test_deleteUser(self):
        # sample data
        user1 = createUser(1)
        user2 = createUser(2)

        # Unauthenticated request
        url = reverse('user-detail', args=[user1.username])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authenticated request, should return 204
        self.createUserAndLogin()
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Get users from database. There should be 2 left.
        users = User.objects.all()
        self.assertEqual(users.count(), 2)
        # Verify that the correct one was deleted
        usernames = [user.username for user in users]
        self.assertNotIn(user1.username, usernames)
