from django.db import migrations
from django.contrib.auth import get_user_model

def assign_default_user(apps, schema_editor):
    Income = apps.get_model('income', 'Income')
    User = get_user_model()
    default_user = User.objects.first()  # Get the first user as default
    if default_user:
        Income.objects.filter(user__isnull=True).update(user=default_user)

class Migration(migrations.Migration):

    dependencies = [
        ('income', '0002_income_user'),
    ]

    operations = [
        migrations.RunPython(assign_default_user),
    ]
