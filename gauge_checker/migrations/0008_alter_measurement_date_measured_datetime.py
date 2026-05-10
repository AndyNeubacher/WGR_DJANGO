import random
from datetime import datetime
import django.utils.timezone as tz
from django.db import migrations, models


def backfill_random_times(apps, schema_editor):
    Measurement = apps.get_model('gauge_checker', 'Measurement')
    local_tz = tz.get_current_timezone()
    for m in Measurement.objects.filter(date_measured__isnull=False):
        dt = m.date_measured
        if dt.hour == 0 and dt.minute == 0 and dt.second == 0:
            naive = datetime(
                dt.year, dt.month, dt.day,
                random.randint(7, 19),
                random.randint(0, 59),
            )
            m.date_measured = tz.make_aware(naive, local_tz)
            m.save()


class Migration(migrations.Migration):

    dependencies = [
        ('gauge_checker', '0007_technican_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='date_measured',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.RunPython(backfill_random_times, migrations.RunPython.noop),
    ]
