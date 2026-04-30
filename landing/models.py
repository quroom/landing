import secrets
from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.utils.text import slugify


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
        return (
            f"{self.name} ({self.email}) - {self.get_email_delivery_status_display()}"
        )


class FunnelEvent(models.Model):
    event_name = models.CharField(max_length=80, db_index=True)
    page_key = models.CharField(max_length=40, blank=True)
    lead_source = models.CharField(max_length=80, blank=True)
    client_ip = models.GenericIPAddressField(null=True, blank=True, db_index=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.event_name} ({self.page_key or '-'})"


class AnalyticsExcludedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    note = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at", "-created_at"]
        verbose_name = "Analytics Excluded IP"
        verbose_name_plural = "Analytics Excluded IPs"

    def __str__(self) -> str:
        state = "active" if self.is_active else "inactive"
        return f"{self.ip_address} ({state})"


class BuildNote(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    class Category(models.TextChoices):
        SOLO_DEV = "solo_dev", "1인 개발"
        MVP = "mvp", "MVP"
        OUTSOURCING = "outsourcing", "외주"
        RETROSPECTIVE = "retrospective", "제품 회고"
        OPERATIONS = "operations", "운영/마케팅"

    title = models.CharField(max_length=120)
    slug = models.SlugField(
        max_length=140,
        unique=True,
        blank=True,
        allow_unicode=True,
        help_text=(
            "비워두면 제목으로 자동 생성합니다. 국내 검색 의도가 강한 글은 "
            "짧은 한글 slug를 써도 됩니다. 예: 1인-개발자-mvp-범위. "
            "너무 긴 문장형 slug는 공유/분석 URL이 지저분해질 수 있어 피합니다."
        ),
    )
    summary = models.TextField(max_length=300)
    body_markdown = models.TextField()
    category = models.CharField(
        max_length=30,
        choices=Category.choices,
        default=Category.SOLO_DEV,
        db_index=True,
    )
    tags = models.CharField(
        max_length=200,
        blank=True,
        help_text="쉼표로 구분합니다. 예: 1인 개발,MVP,외주",
    )
    seo_title = models.CharField(max_length=120, blank=True)
    seo_description = models.CharField(max_length=160, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
    )
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        indexes = [
            models.Index(fields=["status", "-published_at"]),
        ]

    def __str__(self) -> str:
        return self.title

    @property
    def is_published(self) -> bool:
        return self.status == self.Status.PUBLISHED and self.published_at is not None

    @property
    def tag_list(self) -> list[str]:
        return [tag.strip() for tag in self.tags.split(",") if tag.strip()]

    @classmethod
    def _unique_slug(cls, title: str, current_pk: int | None = None) -> str:
        base_slug = slugify(title, allow_unicode=True)[:120] or "build-note"
        slug = base_slug
        suffix = 2
        queryset = cls.objects.all()
        if current_pk:
            queryset = queryset.exclude(pk=current_pk)
        while queryset.filter(slug=slug).exists():
            suffix_text = f"-{suffix}"
            slug = f"{base_slug[: 140 - len(suffix_text)]}{suffix_text}"
            suffix += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._unique_slug(self.title, self.pk)
        if self.status == self.Status.PUBLISHED and self.published_at is None:
            self.published_at = timezone.now()
        if self.status != self.Status.PUBLISHED:
            self.published_at = None
        super().save(*args, **kwargs)


class TestimonialInvite(models.Model):
    token = models.CharField(max_length=64, unique=True, db_index=True)
    target_note = models.CharField(max_length=200, blank=True)
    expires_at = models.DateTimeField(db_index=True)
    consumed_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    reissued_from = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reissued_links",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Invite({self.token[:8]})"

    @staticmethod
    def _generate_token() -> str:
        return secrets.token_urlsafe(24)

    @classmethod
    def issue(
        cls,
        *,
        target_note: str = "",
        expires_in_days: int = 7,
        reissued_from: "TestimonialInvite | None" = None,
    ) -> "TestimonialInvite":
        expires_at = timezone.now() + timedelta(days=expires_in_days)
        invite = cls(
            target_note=target_note.strip(),
            expires_at=expires_at,
            reissued_from=reissued_from,
        )
        invite.save()
        return invite

    @property
    def is_expired(self) -> bool:
        return timezone.now() >= self.expires_at

    @property
    def is_consumed(self) -> bool:
        return self.consumed_at is not None

    def is_usable(self) -> bool:
        return self.is_active and not self.is_expired and not self.is_consumed

    def mark_consumed(self) -> None:
        self.consumed_at = timezone.now()
        self.save(update_fields=["consumed_at", "updated_at"])

    def reissue(self, *, expires_in_days: int = 7) -> "TestimonialInvite":
        self.is_active = False
        self.save(update_fields=["is_active", "updated_at"])
        return self.issue(
            target_note=self.target_note,
            expires_in_days=expires_in_days,
            reissued_from=self,
        )

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self._generate_token()
        super().save(*args, **kwargs)


class Testimonial(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    invite = models.ForeignKey(
        TestimonialInvite,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="testimonials",
    )
    name = models.CharField(max_length=50)
    role_title = models.CharField(max_length=80, blank=True)
    company_name = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    consent_public = models.BooleanField(default=False)
    consent_collected_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        if self.status == self.Status.APPROVED and self.approved_at is None:
            self.approved_at = timezone.now()
        if self.status != self.Status.APPROVED:
            self.approved_at = None
        super().save(*args, **kwargs)
