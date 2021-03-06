from django.test import TestCase
from django.test import Client

import random
import json

from .views import MD5
class EncryptTestCase(TestCase):
    def testMD5(self):
        self.assertEqual(MD5(''), 'd41d8cd98f00b204e9800998ecf8427e')
        self.assertEqual(MD5('a'), '0cc175b9c0f1b6a831c399e269772661')
        self.assertEqual(MD5('abc'), '900150983cd24fb0d6963f7d28e17f72')
        self.assertEqual(MD5('abcdefghijklmnopqrstuvwxyz'), 
            'c3fcd3d76192e4007dfb496cca67e13b')
        self.assertEqual(MD5('123456789012345678901234567890123456789012'\
            '34567890123456789012345678901234567890'),
            '57edf4a22be3c955ac49da2e2107b67a')
        self.assertEqual(MD5('message digest'), 'f96b697d7cb7938d525a2f31aaf161d0')


from .views import articleList
class ViewTestCase(TestCase):
    setup_done = False
    def test_return_code(self):
        response = self.client.get('/api/v1/hello/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/v1/articlelist', \
            {'page': '1', 'limit': '10'})
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/v1/articledetail', \
            {'id':'5a02e30be6c80c1c9ecdaea7'})
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/v1/updateUpvote', \
            {'id':'', 'userID':''})
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/api/v1/usercheck', \
            {'email':'', 'password':''})
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/v1/userlist', \
            {'name': '', 'selfname': '', 'limit': ''})
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/v1/user', \
            {'id': ''})
        self.assertEqual(response.status_code, 200)
        
        response = self.client.post('/api/v1/reguser', \
            {'email': '', 'password': '', 'nickname': '', \
             'name': '',  'sex': '',      'usertype': '', \
             'birthday': '', 'introduction': '', 'age':'',
             'phone':''})
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/v1/userlistbyid', \
            {'id': ''})
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/api/v1/changeNickname', \
            {'id': '', 'newName': ''})
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/api/v1/userlistbyid', \
            {'id': ''})
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/api/v1/changePhone', \
            {'id': '', 'newPhone':''})
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/api/v1/changeName', \
            {'id': '', 'newName': ''})
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/api/v1/changeSex', \
            {'id': '', 'newSex':''})
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/api/v1/changePassword', \
            {'id': '', 'oldPassword':'', 'newPassword':''})
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/api/v1/changeBirthday', \
            {'id': '', 'newBirthday':''})
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/api/v1/addMedicalRecord', \
            {'id': '', 'date':'', 'doctor': '', 'content':''})
        self.assertEqual(response.status_code, 200)





    def setUp(self):
        if self.setup_done:
            return
        self.setup_done = True

        
        ''' 
        first testing user reg for rest tests;
        '''
        response = self.client.post('/api/v1/reguser', \
            {'email': 'admin@mypre.cn', 'password': '123456', 'nickname': 'lanbing', \
             'name': 'lanbing_h',  'sex': '1',      'usertype': '1', \
             'birthday': '1999-11-20', 'introduction': 'new lanbing huangzhe', 'age':'11',
             'phone':'123'})
        self.assertEqual(response.status_code, 200)




        # register repeat user test
        response = self.client.post('/api/v1/reguser', \
            {'email': 'admin@mypre.cn', 'password': '123456', 'nickname': 'lanbing', \
             'name': 'lanbing_h',  'sex': '1',      'usertype': '1', \
             'birthday': '1999-11-20', 'introduction': 'new lanbing huangzhe', 'age':'11',
             'phone':'123'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('false',response.content)

    def test_user_passwd(self):
        # user passwd test
        response = self.client.post('/api/v1/usercheck', \
            {'email':'admin@mypre.cn', 'password':'123456'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('true',response.content)

        json_data = json.loads(response.content)

        self.user_id = json_data['data']['_id']

    def test_user_detail(self):
        self.test_user_passwd()
        response = self.client.get('/api/v1/user', \
            {'id': self.user_id})
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)
        self.assertIn('name',response.content)
        self.assertIn('phone', response.content)
        self.assertIn('labels', response.content)
        self.assertIn('_id', json_data)

    def test_article_list(self):
        for pagei in xrange(1, 5):
            response = self.client.get('/api/v1/articlelist', \
                {'page': pagei, 'limit': '10'})
            self.assertEqual(response.status_code, 200)
            json_data = json.loads(response.content)
            self.assertEqual(len(json_data), 10)
            self.article_list = json_data

    def test_article_detail(self):
        self.test_user_passwd()
        self.test_article_list()
        self.test_user_passwd()
        response = self.client.get('/api/v1/articledetail', \
            {'id': self.article_list[0]['_id'], 'userID': self.user_id})
        self.assertEqual(response.status_code, 200)
        # self.article_detail = json.loads()
        self.assertIn('href', response.content)




    def test_article_upvote(self):
        self.test_user_passwd()
        self.test_article_list()
        response = self.client.get('/api/v1/updateUpvote', \
            {'id': self.article_list[0]['_id'], 'userID': self.user_id})
        self.assertEqual(response.status_code, 200)


    def test_userlist(self):
        response = self.client.get('/api/v1/userlist', \
            {'name': 'l', 'selfname': '', 'limit': ''})
        self.assertEqual(response.status_code, 200)
        # self.assertIn('_id', response.content)

        response = self.client.get('/api/v1/userlist', \
            {'name': 'asdfsdf', 'selfname': '', 'limit': '30'})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_id', response.content)


    def test_change_phone(self):
        self.test_user_passwd()
        response = self.client.post('/api/v1/changePhone', \
            {'id': self.user_id, 'newPhone':'456', 'password':MD5('123456')})
        self.assertEqual(response.status_code, 200)
        self.assertIn('true', response.content)

        response = self.client.post('/api/v1/changePhone', \
            {'id': self.user_id, 'newPhone':'456', 'password':MD5('!!!')})
        self.assertEqual(response.status_code, 200)
        self.assertIn('false', response.content)

    def test_change_name(self):
        self.test_user_passwd()
        response = self.client.post('/api/v1/changeName', \
            {'id': self.user_id, 'newName': 'lanbing new Name', 'password':MD5('123456')})
        self.assertEqual(response.status_code, 200)
        self.assertIn('true', response.content)

        response = self.client.post('/api/v1/changeName', \
            {'id': self.user_id, 'newName': 'lanbing new Name', 'password':'123'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('false', response.content)


    def test_change_sex(self):
        self.test_user_passwd()
        response = self.client.post('/api/v1/changeSex', \
            {'id': self.user_id, 'newSex':'1', 'password':MD5('123456')})
        self.assertEqual(response.status_code, 200)
        self.assertIn('true', response.content)

        response = self.client.post('/api/v1/changeSex', \
            {'id': self.user_id, 'newSex':'1', 'password':'sdf'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('false', response.content)

        response = self.client.post('/api/v1/changeSex', \
            {'id': self.user_id, 'newSex':'1'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('false', response.content)

    def test_change_passwd(self):
        self.test_user_passwd()
        response = self.client.post('/api/v1/changePassword', \
            {'id': self.user_id, 'oldPassword':'123456', 'newPassword':'123456'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('true', response.content)

    def test_change_birthday(self):
        self.test_user_passwd()
        response = self.client.post('/api/v1/changeBirthday', \
            {'id': self.user_id, 'newBirthday': '1999-10-10', 'password':MD5('123456')})
        self.assertEqual(response.status_code, 200)
        self.assertIn('true', response.content)

    def test_change_nickname(self):
        self.test_user_passwd()
        response = self.client.post('/api/v1/changeNickname', \
            {'id': self.user_id, 'newName': 'lanbing\' new nickname!!!', 'password':MD5('123456')})
        self.assertEqual(response.status_code, 200)
        self.assertIn('true', response.content)


    def test_add_medical_record(self):
        self.test_user_passwd()
        response = self.client.post('/api/v1/addMedicalRecord', \
            {'id': self.user_id, 'date':'21312423', \
            'doctor': 'JiangYiShen', 'content':'I\'m not sick!!!', \
            'password':'123456'})
        self.assertEqual(response.status_code, 200)

        self.assertIn('true', response.content)


