from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache

class Author(models.Model):
	author = models.OneToOneField(User, on_delete=models.CASCADE)
	user_rating = models.IntegerField(default = 0)

	def update_rating(self, new_rating):
		self.user_rating = new_rating
		self.save()

	def __str__(self):
		return f'{self.author}'

class Category(models.Model):
	new_category = models.CharField(max_length = 100, unique = True)

	def __str__(self):
		return f'{self.new_category}'

class Post(models.Model):
	POST_TYPE = [('AR', 'Статья'), ('NW', 'Новость')]
	author = models.ForeignKey(Author, on_delete = models.CASCADE)
	post_type = models.CharField(max_length = 2, choices = POST_TYPE, default = 'AR')
	time_create = models.DateTimeField(auto_now_add = True)
	title = models.CharField(max_length = 255)
	text = models.TextField()
	rating = models.IntegerField(default = 0)
	categories = models.ManyToManyField(Category, through='PostCategory')

	# @property
	# def category(self):
	# 	category = list(self.categories.values_list('pk', flat=True))
	# 	return '' if len(category) == 0 else Category.objects.get(pk = category[0]).new_category
	def __str__(self):
		return f'{self.title}.'

	def like(self):
		self.rating += 1
		self.save()

	def dislike(self):
		self.rating -= 1
		self.save()

	def preview(self):
		size = 124 if len(self.text) > 125 else len(self.text)
		return self.text[:size] + '...'

	def get_absolute_url(self):
		return f'/news/'

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		cache.delete(f'news-{self.pk}')

class PostCategory(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete = models.CASCADE)
	def __str__(self):
		return f'Title: {self.post.title} Category: {self.category.new_category}'

class Comment(models.Model):
	text = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	rating = models.IntegerField(default = 0)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def like(self):
		self.rating += 1
		self.save()

	def dislike(self):
		self.rating -= 1
		self.save()

class Subscribers(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	news_category = models.ManyToManyField(to=Category)