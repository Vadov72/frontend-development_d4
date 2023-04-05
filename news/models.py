from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


# Create your models here.
class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    authorRating = models.SmallIntegerField(default=0)

    def update_rating(self):
        post_rating = self.post_set.aggregate(postRating=Sum('rating'))
        postRat = 0
        postRat += post_rating.get('postRating')

        comment_rating = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        comRat = 0
        comRat += comment_rating.get('commentRating')

        self.authorRating = postRat * 3 + comRat
        self.save()


class Category(models.Model):
    category_name = models.CharField('Категории', max_length=64, unique=True)


class Post(models.Model):
    postAuthor = models.ForeignKey(Author, on_delete=models.CASCADE)

    # «статья» или «новость»
    postNews = 'PN'
    postArticle = 'PA'

    POSITIONS = [
        (postArticle, 'Статья'),
        (postNews, 'Новость'),
    ]

    position = models.CharField('Тип', max_length=2, choices=POSITIONS, default=postArticle)
    dateCreation = models.DateTimeField('Поиск по дате в формате "год-месяц-день"', auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    preview_name = models.CharField('Заголовок', max_length=128)
    text = models.TextField('Поле для текста')
    rating = models.SmallIntegerField('Рейтинг', default=0)

    def __str__(self):
        return f'{self.preview_name}'

    def get_absolute_url(self):  # добавим абсолютный путь чтобы после создания нас перебрасывало на главную страницу
        return f'/news/{self.pk}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:124] + '...'


class PostCategory(models.Model):
    pcPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    pcCategory = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    commentText = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
