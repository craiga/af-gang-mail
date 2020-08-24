# Generated by Django 3.1 on 2020-08-09 11:26

from django.db import migrations


def create_flatblock(apps, schema_editor):
    """Create draw-sent-intro flat block."""

    FlatBlock = apps.get_model("flatblocks", "FlatBlock")
    if not FlatBlock.objects.filter(slug="draw-sent-intro").exists():
        FlatBlock.objects.create(
            slug="draw-sent-intro",
            header="Confirm that you've sent your gift",
            content=(
                "<p>Would you like to include a message?<p>"
                "<p>If you have them, you might want to include details on how to "
                "track the gift you've sent.</p>"
            ),
        )


class Migration(migrations.Migration):

    dependencies = [
        ("af_gang_mail", "0018_privacy_flatpage"),
    ]

    operations = [
        migrations.RunPython(create_flatblock, migrations.RunPython.noop),
    ]