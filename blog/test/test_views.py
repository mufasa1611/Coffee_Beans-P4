from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from blog.models import Post

class PostListViewTest(TestCase):

    def setUp(self):
        # Create a user to use as the author
        self.user = User.objects.create_user(username='testuser', password='12345')
        # Create a sample post
        Post.objects.create(title='Test Post', slug='test-post', content='Test content', status=1, author=self.user)

    def test_post_list_view(self):
        # Test if the post list view returns status 200
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')
        self.assertContains(response, 'Test Post')

class PostDetailViewTest(TestCase):

    def setUp(self):
        # Create a user to use as the author
        self.user = User.objects.create_user(username='testuser', password='12345')
        # Create a sample post
        self.post = Post.objects.create(title='Test Post', slug='test-post', content='Test content', status=1, author=self.user)

    def test_post_detail_view(self):
        # Test if the post detail view returns status 200
        response = self.client.get(reverse('post_detail', kwargs={'slug': self.post.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertContains(response, 'Test Post')
