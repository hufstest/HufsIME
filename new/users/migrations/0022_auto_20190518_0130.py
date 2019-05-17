# Generated by Django 2.1.7 on 2019-05-17 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_auto_20190518_0059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Article'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Article'),
        ),
        migrations.AlterField(
            model_name='hit',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Article'),
        ),
        migrations.AlterField(
            model_name='hit',
            name='date',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='like',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Article'),
        ),
        migrations.AlterField(
            model_name='taggedpost',
            name='content_object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Article'),
        ),
    ]