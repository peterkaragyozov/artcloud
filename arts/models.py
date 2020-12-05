from django.db import models

from accounts.models import UserProfile


class Art(models.Model):
    PAINTING = 'painting'
    SCULPTURE = 'sculpture'
    DRAWING = 'drawing'
    OTHER = 'other'

    ART_TYPES = (
        (PAINTING, 'Painting'),
        (SCULPTURE, 'Sculpture'),
        (DRAWING, 'Drawing'),
        (OTHER, 'Other'),
    )

    type = models.CharField(max_length=9, choices=ART_TYPES, default=OTHER)
    name = models.CharField(max_length=30, blank=False)
    author = models.CharField(max_length=30, blank=False)
    year = models.IntegerField(blank=False)
    description = models.TextField(blank=False)
    image = models.ImageField(
        upload_to='arts',
    )
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'ID {self.id}: "{self.name}" by {self.author}, {self.year}'


class Like(models.Model):
    art = models.ForeignKey(Art, on_delete=models.CASCADE)
    test = models.CharField(max_length=2)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class Comment(models.Model):
    art = models.ForeignKey(Art, on_delete=models.CASCADE)
    text = models.TextField(blank=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
