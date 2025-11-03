from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


CATEGORY_COLOR_CHOICES = [
    ('bg-indigo-500', 'Indigo'),
    ('bg-blue-500', 'Azul'),
    ('bg-purple-500', 'Roxo'),
    ('bg-green-500', 'Verde'),
    ('bg-emerald-500', 'Esmeralda'),
    ('bg-amber-500', 'Âmbar'),
    ('bg-pink-500', 'Rosa'),
    ('bg-red-500', 'Vermelho'),
]

CATEGORY_TYPE_CHOICES = [
    ('income', 'Receita'),
    ('expense', 'Despesa'),
]


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(choices=CATEGORY_TYPE_CHOICES, default='expense', max_length=20)),
                ('color', models.CharField(choices=CATEGORY_COLOR_CHOICES, default='bg-indigo-500', max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
    ]
