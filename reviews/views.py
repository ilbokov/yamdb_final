from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from titles.models import Title
from users.permissions import IsAuthorOrAdministratorOrReadOnly

from .models import Review
from .serializers import CommentSerializer, ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrAdministratorOrReadOnly]

    def perform_create(self, serializer):
        title = get_object_or_404(Title,
                                  pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs["title_id"])
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrAdministratorOrReadOnly, ]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)
