from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок',
        help_text='Введите заголовок поста'
    )
    content = models.TextField(
        verbose_name='Содержание',
        help_text='Введите текст поста'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, #Фиксирует 1 раз при добавлении
        verbose_name='Дата создания'
    )
    update_at = models.DateTimeField(
        auto_now=True, #Фиксирует каждый раз при обновлении
        verbose_name='Дата обновления'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        # user.posts.all()
        related_name='posts',
        null=True, # автор может быть пустым
        blank=True #Может быть пустым
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

        ordering = ['-created_at'] #сортировка по дате поста


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Пост',
        related_name='comments'
    )
    text = models.TextField(verbose_name='Текст комментария')

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='comments'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, #Фиксирует 1 раз при добавлении
        verbose_name='Дата создания'
    )

    def __str__(self):
        return f'Комментарий от {self.author} к "{self.posts.title}"'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']