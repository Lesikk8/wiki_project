from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Section(models.Model):
    name = models.CharField(max_length=200, verbose_name='Назва розділу')
    slug = models.SlugField(max_length=200, unique=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='children',
        verbose_name='Батьківський розділ'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Розділ'
        verbose_name_plural = 'Розділи'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('section_detail', kwargs={'slug': self.slug})


class Page(models.Model):
    title = models.CharField(max_length=300, verbose_name='Заголовок')
    slug = models.SlugField(max_length=300, unique=True)
    content = models.TextField(verbose_name='Зміст')
    section = models.ForeignKey(
        Section, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='pages',
        verbose_name='Розділ'
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, related_name='pages',
        verbose_name='Автор'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубліковано')

    class Meta:
        verbose_name = 'Сторінка'
        verbose_name_plural = 'Сторінки'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('page_detail', kwargs={'slug': self.slug})


class PageVersion(models.Model):
    page = models.ForeignKey(
        Page, on_delete=models.CASCADE,
        related_name='versions',
        verbose_name='Сторінка'
    )
    title = models.CharField(max_length=300, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Зміст')
    edited_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, verbose_name='Відредаговано'
    )
    edited_at = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(
        max_length=500, blank=True,
        verbose_name='Коментар до змін'
    )

    class Meta:
        verbose_name = 'Версія сторінки'
        verbose_name_plural = 'Версії сторінок'
        ordering = ['-edited_at']

    def __str__(self):
        return f'{self.page.title} — {self.edited_at.strftime("%d.%m.%Y %H:%M")}'


class AccessRight(models.Model):
    ROLE_CHOICES = [
        ('viewer', 'Читач'),
        ('editor', 'Редактор'),
        ('admin', 'Адміністратор'),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='access_rights',
        verbose_name='Користувач'
    )
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE,
        related_name='access_rights',
        verbose_name='Розділ'
    )
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES,
        default='viewer', verbose_name='Роль'
    )

    class Meta:
        verbose_name = 'Право доступу'
        verbose_name_plural = 'Права доступу'
        unique_together = ('user', 'section')

    def __str__(self):
        return f'{self.user.username} — {self.section.name} ({self.get_role_display()})'


class PageSummary(models.Model):
    page = models.OneToOneField(
        Page, on_delete=models.CASCADE,
        related_name='ai_summary',
        verbose_name='Сторінка'
    )
    summary = models.TextField(verbose_name='ШІ-резюме', blank=True)
    generated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'ШІ-резюме'
        verbose_name_plural = 'ШІ-резюме'

    def __str__(self):
        return f'Резюме: {self.page.title}'
