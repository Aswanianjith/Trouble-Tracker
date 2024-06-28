from django.test import TestCase
from django.contrib.auth.models import User
from .models import Issue

class IssueTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_issue_creation(self):
        issue = Issue.objects.create(title='Test Issue', description='This is a test issue.', created_by=self.user)
        self.assertEqual(issue.title, 'Test Issue')
