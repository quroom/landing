from django.db import models
from django.utils import timezone


class ContactInquiry(models.Model):
    class DeliveryStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"

    name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=100, blank=True)
    contact = models.CharField(max_length=120, blank=True)
    email = models.EmailField()
    inquiry_type = models.CharField(max_length=20)
    message = models.TextField()
    privacy_agreed_at = models.DateTimeField(default=timezone.now)
    marketing_opt_in = models.BooleanField(default=False)
    marketing_opted_in_at = models.DateTimeField(null=True, blank=True)

    email_delivery_status = models.CharField(
        max_length=20,
        choices=DeliveryStatus.choices,
        default=DeliveryStatus.PENDING,
    )
    emailed_at = models.DateTimeField(null=True, blank=True)
    email_error = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} ({self.email}) - {self.get_email_delivery_status_display()}"
