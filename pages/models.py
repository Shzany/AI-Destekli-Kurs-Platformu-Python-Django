from django.conf import settings
from django.db import models
from django.utils.text import slugify

class Page(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.CharField(max_length=30)
    last_update = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=30, default='')
    slug = models.SlugField(max_length=200, blank=True, null=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['category', 'order', 'title']

    def save(self, *args, **kwargs):
        if not self.order:
            last_order = Page.objects.filter(category=self.category).aggregate(models.Max('order'))
            self.order = (last_order.get('order__max') or 0) + 1
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_image_path(self):
        return f"img/{self.image}"

    def average_rate(self):
        rates = self.rates.all()
        if not rates:
            return 0
        return sum(rate.score for rate in rates) / rates.count()

class Rate(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='rates')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('page', 'user')

    def __str__(self):
        return f"{self.user} - {self.page}: {self.score}"