# Generated by Django 2.2.28 on 2023-01-10 15:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('annotationweb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='imageannotation',
            name='finished',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='imageannotation',
            name='image_view',
            field=models.CharField(choices=[('a4c', 'A4C'), ('a2c', 'A2C'), ('plax', 'PLAX'), ('alax', 'ALAX')], default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='keyframeannotation',
            name='frame_metadata',
            field=models.CharField(default='', help_text='A text field for storing arbitrary metadata on the current frame', max_length=512),
        ),
        migrations.AddField(
            model_name='task',
            name='post_processing_method',
            field=models.CharField(blank=True, default='', help_text='Name of post processing method to use', max_length=255),
        ),
        migrations.AlterField(
            model_name='label',
            name='color_blue',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='label',
            name='color_green',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='label',
            name='color_red',
            field=models.PositiveSmallIntegerField(default=255),
        ),
        migrations.AlterField(
            model_name='task',
            name='type',
            field=models.CharField(choices=[('classification', 'Classification'), ('boundingbox', 'Bounding box'), ('landmark', 'Landmark'), ('cardiac_segmentation', 'Cardiac apical segmentation'), ('cardiac_plax_segmentation', 'Cardiac PLAX segmentation'), ('cardiac_alax_segmentation', 'Cardiac ALAX segmentation'), ('spline_segmentation', 'Spline segmentation'), ('spline_line_point', 'Splines, lines & point segmentation')], max_length=50),
        ),
    ]
