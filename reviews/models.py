from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from titles.models import Title
from users.models import User


class Review(models.Model):
    text = models.TextField(blank=False)
    pub_date = models.DateTimeField("Дата публикации",
                                    auto_now_add=True)
    author = models.ForeignKey(User,
                               blank=True,
                               on_delete=models.CASCADE,
                               related_name="reviews")
    score = models.PositiveIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(10)]
    )
    title = models.ForeignKey(Title,
                              blank=True,
                              on_delete=models.CASCADE,
                              related_name="reviews")

    class Meta:
        ordering = ("pub_date", )
        unique_together = ('author', 'title',)

    def __str__(self):
        return f'Отзыв от {self.author} на {self.title}'[:70]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        "Дата добавления",
        auto_now_add=True,
        db_index=True
    )
