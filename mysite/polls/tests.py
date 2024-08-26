from django.test import TestCase
from django.utils import timezone
import datetime 
from django.urls import reverse

from .models import Question, Choice

# Create your tests here.


class QuestionModelTest(TestCase):
    
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
        #old question 
        time = timezone.now() - datetime.timedelta(days=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)
        

        
    
    def test_was_published_recently_with_current_question(self):
        #current time 
        time = timezone.now()
        current_question = Question(pub_date=time)
        self.assertIs(current_question.was_published_recently(), True)
        
class QuestionDetailViewTests(TestCase):
    
    def test_future_question(self):
        
        """_
        The detail view of question with a pub_date in the future 
        returns a 404  not found 
        """
        
        future_question = Question(question_text="Future question", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response= self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_past_question(self):
        """
        The detail view of the question with the pub_date in the past should
        display the question text 
        """
        past_question = Question(question_text="Past Question", days=-5)
        url= reverse("polls:detail", args=(past_question.id,))
        response= self.client.get(url)
        self.assertContains(response, past_question.question_text)
        
    