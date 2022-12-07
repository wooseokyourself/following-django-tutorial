from django.test import TestCase

# Create your tests here.

import datetime

from django.utils import timezone
from django.urls import reverse

from .models import Question, Choice

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose
        pub_date is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose
        pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        past_question = Question(pub_date=time)
        self.assertIs(past_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose 
        pub_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
    """
    Create a question with the given 'question_text' and published the 
     given number of 'days' offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

def create_question_with_choice(question_text, days, choice_text="default"): 
    time = timezone.now() + datetime.timedelta(days=days)
    question = Question.objects.create(question_text=question_text, pub_date=time)
    question.choice_set.create(choice_text=choice_text, votes=0)
    return question

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('generic_polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.") # defined in index.html
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        question = create_question_with_choice(question_text="Past question.", days=-30)
        empty_question = create_question(question_text="empty", days=-30)
        response = self.client.get(reverse('generic_polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question],)

    def test_future_question(self):
        question = create_question_with_choice(question_text="Future question.", days=30)
        empty_question = create_question(question_text="empty", days=30)
        response = self.client.get(reverse('generic_polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        past_question = create_question_with_choice(question_text="Past question.", days=-30)
        future_question = create_question_with_choice(question_text="Future question.", days=30)
        empty_past = create_question(question_text="empty past", days=-30)
        empty_future = create_question(question_text="empty future", days=30)
        response = self.client.get(reverse('generic_polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [past_question], )

    def test_two_past_questions(self):
        question1 = create_question_with_choice(question_text="First question.", days=-25)
        question2 = create_question_with_choice(question_text="Second question.", days=-30)
        empty_question = create_question(question_text="empty", days=-50)
        response = self.client.get(reverse('generic_polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question1, question2], )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question_with_choice(question_text="future question", days=5)
        url = reverse('generic_polls:detail', args=(future_question.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_empty_future_question(self):
        future_question = create_question(question_text="empty", days=5)
        url = reverse('generic_polls:detail', args=(future_question.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question_with_choice(question_text="past question", days=-5)
        url = reverse('generic_polls:detail', args=(past_question.id, ))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_empty_past_question(self): 
        past_question = create_question(question_text="empty", days=-5)
        url = reverse('generic_polls:detail', args=(past_question.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
