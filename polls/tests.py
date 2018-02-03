# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import mock

from django import test
from django.contrib.auth import models as auth_models

from . import models


class ViewTests(test.TestCase):

    def setUp(self):
        self.group1 = auth_models.Group(name='group1')
        self.group1.save()
        self.user1 = auth_models.User.objects.create_user(username='user1')
        self.user1.groups.add(self.group1)
        self.user1.save()
        self.group2 = auth_models.Group(name='group2')
        self.group2.save()
        self.user2 = auth_models.User.objects.create_user(username='user2')
        self.user2.groups.add(self.group2)
        self.user2.save()
        self.user3 = auth_models.User.objects.create_user(username='user3')
        self.user3.groups.add(self.group2)
        self.user3.save()

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()
        self.user3.delete()
        self.group1.delete()
        self.group2.delete()

    def test_user_redirected_to_login_root_no_auth(self):
        response = self.client.get('/polls/')
        self.assertRedirects(response, '/polls/login?next=/polls/',
                             status_code=302, target_status_code=301)

    def test_user_redirected_to_login_results_no_auth(self):
        response = self.client.get('/polls/results/')
        self.assertRedirects(response, '/polls/login?next=/polls/results/',
                             status_code=302, target_status_code=301)

    def test_user_redirected_to_home_auth(self):
        self.client.force_login(self.user1)
        response = self.client.get('/polls/login/')
        self.assertRedirects(response, '/polls',
                             status_code=302, target_status_code=301)

    def test_user_redirected_to_login_logout(self):
        self.client.force_login(self.user1)
        self.assertIn('_auth_user_id', self.client.session)
        response = self.client.get('/polls/')
        self.assertEqual(200, response.status_code)
        self.client.logout()
        self.assertNotIn('_auth_user_id', self.client.session)
        response = self.client.get('/polls/')
        self.assertRedirects(response, '/polls/login?next=/polls/',
                             status_code=302, target_status_code=301)

    def test_user_redirected_to_login_logout_page(self):
        self.client.force_login(self.user1)
        self.assertIn('_auth_user_id', self.client.session)
        response = self.client.get('/polls/')
        self.assertEqual(200, response.status_code)
        response = self.client.get('/polls/logout/')
        self.assertRedirects(response, '/polls/login',
                             status_code=302, target_status_code=301)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_user_one_daily_response(self):
        self.client.force_login(self.user1)
        response = self.client.get('/polls/')
        self.assertEqual(200, response.status_code)
        models.Choice.objects.create(value=5, user=self.user1)
        response = self.client.get('/polls/')
        self.assertRedirects(response, '/polls/results',
                             status_code=302, target_status_code=301)

    def test_user_one_daily_response_logout(self):
        self.client.force_login(self.user1)
        response = self.client.get('/polls/')
        self.assertEqual(200, response.status_code)
        models.Choice.objects.create(value=5, user=self.user1)
        self.client.logout()
        self.client.force_login(self.user1)
        response = self.client.get('/polls/')
        self.assertRedirects(response, '/polls/results',
                             status_code=302, target_status_code=301)

    def test_user_response_isolated(self):
        self.client.force_login(self.user1)
        response = self.client.get('/polls/')
        self.assertEqual(200, response.status_code)
        models.Choice.objects.create(value=5, user=self.user1)
        self.client.logout()
        self.client.force_login(self.user2)
        response = self.client.get('/polls/')
        self.assertEqual(200, response.status_code)

    def test_user_next_day_fine(self):
        self.client.force_login(self.user1)
        response = self.client.get('/polls/')
        self.assertEqual(200, response.status_code)
        prev_day = datetime.datetime.utcnow() - datetime.timedelta(days=1)
        with mock.patch('django.utils.timezone.now', return_value=prev_day):
            models.Choice.objects.create(timestamp=prev_day.date(), value=5,
                                         user=self.user1)
        response = self.client.get('/polls/')
        self.assertEqual(200, response.status_code)

    def test_user_no_response_no_redirect(self):
        self.client.force_login(self.user1)
        response = self.client.get('/polls/')
        self.assertEqual(200, response.status_code)
        response = self.client.get('/polls/')
        self.assertEqual(200, response.status_code)
