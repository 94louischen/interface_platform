# Generated by Django 3.1.6 on 2021-09-17 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testsuits',
            fields=[
                ('id', models.AutoField(help_text='id主键', primary_key=True, serialize=False, verbose_name='id主键')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='套件名称', max_length=200, unique=True, verbose_name='套件名称')),
                ('include', models.TextField(help_text='包含的接口', verbose_name='包含的接口')),
                ('project', models.ForeignKey(help_text='所属项目', on_delete=django.db.models.deletion.CASCADE, related_name='testsuits', to='projects.projects')),
            ],
            options={
                'verbose_name': '套件信息',
                'verbose_name_plural': '套件信息',
                'db_table': 'tb_testsuits',
            },
        ),
    ]