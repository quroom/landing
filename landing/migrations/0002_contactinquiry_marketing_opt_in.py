from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("landing", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="contactinquiry",
            name="marketing_opt_in",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="contactinquiry",
            name="marketing_opted_in_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
