import unittest
from app.models import Comment, Pitch,User
from app import db

class CommentTest(unittest.TestCase):
    """
    Test Class to test the behaviour of the Comment class
    """
    def setUp(self):
        self.user_James = User(username = "James",password = "potato",email = "james@ms.com")
        self.pitch_legacy = Pitch(title = "Legacy",text = "I am living to be more than just another boring eulogy")
        self.new_comment = Comment(comment = "This is a very beautiful pitch.",user = self.user_James,pitch = self.pitch_legacy)

    def tearDown(self):
        Comment.query.delete()
        User.query.delete()
        Pitch.query.delete()

    def test_check_instance_variables(self):
        self.assertEqual(self.new_comment.comment, "This is a very beautiful pitch.")
        self.assertEqual(self.new_comment.user, self.user_James)
        self.assertEqual(self.new_comment.pitch, self.pitch_legacy)

    def test_save_comment(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comment.query.all()) > 0)

    def test_get_comments_by_id(self):
        self.new_comment.save_comment()
        got_comments = Comment.get_comments(40)
        self.assertTrue(len(got_comments) == 1)