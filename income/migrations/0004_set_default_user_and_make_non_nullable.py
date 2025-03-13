from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

def set_default_user(apps, schema_editor):
    Income = apps.get_model('income', 'Income')
    User = apps.get_model('auth', 'User')
    default_user = User.objects.first()
    if default_user:
        Income.objects.filter(user__isnull=True).update(user=default_user)

class Migration(migrations.Migration):

    dependencies = [
        ('income', '0003_assign_default_user'),
    ]

    operations = [
        migrations.RunPython(set_default_user),
        migrations.AlterField(
            model_name='income',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incomes', to=settings.AUTH_USER_MODEL),
        ),
    ]
