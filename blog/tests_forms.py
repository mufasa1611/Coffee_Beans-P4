from django.test import TestCase
from .forms import CommentForm


class TestCommentForm(TestCase):
    def test_comment(self):
        comment_form = CommentForm ({'content':''})
        self.assertFalse(comment_form.is_valid(), msg="form is not okay")
        
    def test_comment_Valid(self):
        comment_form = CommentForm ({'content':'New text'})
        self.assertTrue(comment_form.is_valid(), msg="form is ok")

