# Generated by Django 2.2.7 on 2019-11-18 10:48

from django.conf import settings
from django.db import connection, migrations, models
import django.db.models.deletion


# TODO work out how to do this in Django ORM
# although I think this should be compatible with all SQL dialects
def forwards_new_resume(apps, schema_editor):
    with connection.cursor() as cursor:
        # create new resumes for each user in the database
        cursor.execute('''
            INSERT INTO resume_resume (user_id, name)
            SELECT DISTINCT user_id, 'My Resume'
            FROM resume_resumeitem
        ''')

        # set the resume items to point to the new resumes
        cursor.execute('''
            UPDATE resume_resumeitem
            SET resume_id = (
                SELECT id
                FROM resume_resume
                WHERE resume_resumeitem.user_id = resume_resume.user_id
            )
        ''')


def backwards_new_resume(apps, schema_editor):
    with connection.cursor() as cursor:
        cursor.execute('''
            DELETE FROM resume_resume
        ''')


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('resume', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to=settings.AUTH_USER_MODEL)),
            ],
        ),

        # add a new nullable resume field
        migrations.AddField(
            model_name='resumeitem',
            name='resume',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='resume.Resume'),
        ),

        # add a new name field
        migrations.AddField(
            model_name='resume',
            name='name',
            # default to My Resume for lack of something else to call it
            field=models.TextField(default='My Resume'),
            preserve_default=False,
        ),

        # create the new resume items
        migrations.RunPython(forwards_new_resume, backwards_new_resume),


        # TODO MAKE THE FOLLOWING BACKWARDS-COMPATIBLE
        # Currently we cannot reverse migrations due to this.

        # Remove the user field from resume item
        migrations.RemoveField(
            model_name='resumeitem',
            name='user',
        ),

        # remove the null capabilities
        migrations.AlterField(
            model_name='resumeitem',
            name='resume',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='resume.Resume'),
        ),

        # remove the default
        migrations.AlterField(
            model_name='resume',
            name='name',
            field=models.TextField(),
        ),
    ]
