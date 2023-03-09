from django.db import migrations

INITIAL_TAGS =[
    {"name": "Завтраки", "color": "#9D00FF", "slug": "breakfast"},
    {"name": "Обед", "color": "#FF44CC", "slug": "lunch"},
    {"name": "Ужин", "color": "#39ff14", "slug": "dinner"}
]


def add_tags(apps, schema_editor):
    Tag = apps.get_model('recipes', 'Tag')
    for tag in INITIAL_TAGS:
        new_tag = Tag(**tag)
        new_tag.save()


def remove_tags(apps, schema_editor):
    Tag = apps.get_model('recipes', 'Tag')
    for tag in INITIAL_TAGS:
        Tag.object.get(slug=tag['slug']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.RunPython(
            add_tags,
            remove_tags
        )
    ]