import unittest
from app.models import Blog, User, Category, Comment, Like

class AllModelsTest(unittest.TestCase):
    def setUp(self):
        '''
        The setup method will run before each test case
        '''
        self.new_posts = Blog(title='Test-title',content='test-content', poster_id=1,category_id=1)
        self.new_user = User(firstname='Lemmy',lastname='Mwaura',email='lemmy@lemmy.com',username='lem',password='lemisawesome')
        self.new_category = Category(name='Bsns')
        self.new_comment = Comment(text='Awesome idea',post_id=1,poster_id=1)
        self.new_like = Like(post_id=1,author='Lem')

    def test_instance(self):
        self.assertTrue(isinstance(self.new_posts, Blog))
        self.assertTrue(isinstance(self.new_user, User))
        self.assertTrue(isinstance(self.new_category, Category))
        self.assertTrue(isinstance(self.new_comment, Comment))
        self.assertTrue(isinstance(self.new_like, Like))

    if __name__=='__main__':
        unittest.main()
