from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("landing", "0002_contactinquiry_marketing_opt_in"),
    ]

    operations = [
        migrations.CreateModel(
            name="FunnelEvent",
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
                ("event_name", models.CharField(db_index=True, max_length=80)),
                ("page_key", models.CharField(blank=True, max_length=40)),
                ("lead_source", models.CharField(blank=True, max_length=80)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
