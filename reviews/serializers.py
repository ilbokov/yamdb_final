from rest_framework import serializers

from .models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field='description'
    )
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    def create(self, data):
        name = self.context['view'].kwargs.get('title_id')
        author = self.context["request"].user
        message = 'Author review already exist'
        if Review.objects.filter(title=name, author=author).exists():
            raise serializers.ValidationError(message)
        return Review.objects.create(**data)

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field='username'
    )

    review = serializers.SlugRelatedField(many=False,
                                          read_only=True,
                                          slug_field='text')

    class Meta:
        fields = '__all__'
        model = Comment
