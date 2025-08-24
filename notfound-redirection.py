        
class Redirections(models.Model):
    original_url = models.SlugField(
        max_length=200,
        unique=True,
        help_text="Enter slug only (e.g., my-previous-slug)."
    )
    redirect_url = models.URLField(
        help_text="Enter the full URL (e.g., https://google.com)."
    )
    redirect_count = models.PositiveIntegerField(default=0)
    last_modification_date = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['original_url']),
            models.Index(fields=['redirect_url']),
            models.Index(fields=['last_modification_date']),
        ]

    def __str__(self):
        return f"{self.original_url} redirects to {self.redirect_url}"





class NotFoundLog(models.Model):
    url = models.CharField(max_length=255, unique=True)
    user_agent = models.CharField(max_length=255, null=True, blank=True)
    total_error_count = models.IntegerField(default=1)  # Renamed from count
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.url} - {self.total_error_count} times"
        