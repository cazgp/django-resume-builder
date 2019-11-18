from bs4 import BeautifulSoup

from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django.urls import reverse

from .models import Resume
from . import views


class QuestionModelTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='moo', email='moo@moo.com', password='moo')

    def test_resumes_appear_in_alphabetical_order(self):
        resumes = Resume.objects.bulk_create([
            Resume(name='zebra', user=self.user),
            Resume(name='alpha', user=self.user),
        ])

        request = self.factory.get(reverse('resume'))
        request.user = self.user

        response = views.resumes(request)
        soup = BeautifulSoup(response.content, "html.parser")
        resume_items = soup.find_all("div", class_="row resume-item")

        expected = ["alpha", "zebra"]
        actual = [
            x.find("div", class_="font-weight-bold").get_text()
            for x in resume_items]

        self.assertEqual(actual, expected)
