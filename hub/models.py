from django.db import models


class Portfolio(models.Model):
    CATEGORY_CHOICES = [
        ('Web Development', 'Web Development'),
        ('Mobile Apps', 'Mobile Apps'),
        ('UI/UX', 'UI/UX'),
        ('Research', 'Research'),
        ('Academic', 'Academic'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES)
    tech = models.JSONField(default=list, blank=True)
    url = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
