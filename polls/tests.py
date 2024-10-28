from django.test import TestCase
from django.utils import timezone
import datetime 
from django.urls import reverse

from .models import Question, Choice

# Create your tests here.


class QuestionModelTest(TestCase):
    
    # test methods begins with test ..
    def test_was_published_recently_with_future_question(self):
        """_summary_
        was_published_recently() return false for the questions whose
        pub_date is in the future

        Args:
            TestCase (_type_): Inherited class for performing the automatic test
        """
        #future question test 
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
        
        
    def test_was_published_recently_with_old_question(self):
        """_summary_
        should return false if the question is older one . 
        """
        # old question 
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)
        
    def test_was_published_recently_with_recent_question(self):
        """
        It should return True
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

        
    
# Question creator function 

def create_question(question_text, days):
    """_summary_

    Args:
        question_text (string): question text
        days (numbers): days to be published 
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date= time)
    
class IndexViewTest(TestCase):
    def test_no_questions(self):
        """
        If no question, a message will be displayed 
        """
        response = self.client.get(reverse("polls:main"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])
        
    def test_past_questions(self):
        """question with the pub_date in past should displayed in index
        """
        question = create_question(question_text="past Question", days=-30)
        response = self.client.get(reverse("polls:main"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"], [question]
        )
        
    def test_future_question(self):
        """
        Future question should not display in the index page
        """
        question = create_question(question_text="future question", days=10)
        response = self.client.get(reverse("polls:main"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(
            response.context["latest_question_list"], []
        )
        
    def test_past_question_future_question(self):
        """
        only past question should displayed
        """
        question = create_question(question_text="past_question", days=-30)
        create_question(question_text="future_question", days=30)
        response = self.client.get(reverse("polls:main"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"], [question]
        )
        
    def test_two_past_question(self):
        """"
        both past question should displayed
        """
        question_1 = create_question(question_text="old_question1", days=-30)
        question_2 = create_question(question_text="old_question_2", days=-20)
        response = self.client.get(reverse("polls:main"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question_2, question_1],
        )

# test for detail view 

class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        """
        The future question should not be published 
        """
        question = create_question(question_text="Future Question", days= 10)
        url = reverse("polls:detail", args=(question.id, ))
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, 404
        )
    
        
    def test_old_question_with_no_choice(self):
        """
        The old question in detail should be shown 
        """
        question = create_question(question_text="Old question", days=-5)
        url = reverse("polls:detail", args=(question.id, ))
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, 404
        )
        