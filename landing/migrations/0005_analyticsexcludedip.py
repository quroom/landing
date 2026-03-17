from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("landing", "0004_testimonialinvite_testimonial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AnalyticsExcludedIP",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ip_address", models.GenericIPAddressField(unique=True)),
                ("note", models.CharField(blank=True, max_length=200)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Analytics Excluded IP",
                "verbose_name_plural": "Analytics Excluded IPs",
                "ordering": ["-updated_at", "-created_at"],
            },
        ),
    ]
