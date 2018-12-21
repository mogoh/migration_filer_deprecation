from typing import Type

from cmsplugin_filer_file.models import FilerFile
from cmsplugin_filer_image.models import FilerImage
from cmsplugin_filer_link.models import FilerLinkPlugin
from django.apps.registry import Apps
from django.db import migrations
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from djangocms_file.models import File
from djangocms_file.models import get_templates as get_file_templates
from djangocms_link.models import Link
from djangocms_picture.models import Picture
from djangocms_picture.models import get_templates as get_picture_templates

from ceres.settings.production import STATIC_URL


def forwards_filer_folder(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> bool:
    """Migrate data from cmsplugin_filer_folder to djangocms_file_folder.

    Attation: This is basically the same as the gist, this code is based on and is not tested at all.
    """
    try:
        cmsplugin_filer_folder = apps.get_model('cmsplugin_filer_folder', 'FilerFolder')
        djangocms_file_folder = apps.get_model('djangocms_file', 'Folder')
        for old_object in cmsplugin_filer_folder.objects.all():
            old_cmsplugin_ptr = old_object.cmsplugin_ptr
            new_object = djangocms_file_folder(
                folder_src=old_object.folder,

                # defaults for fields that don't exist in the old_object
                template=get_file_templates()[0][0],
                link_target='',
                show_file_size=0,

                # fields for the cms_cmsplugin table
                plugin_type='FolderPlugin',
                position=old_cmsplugin_ptr.position,
                language=old_cmsplugin_ptr.language,
                creation_date=old_cmsplugin_ptr.creation_date,
                changed_date=old_cmsplugin_ptr.changed_date,
                parent=old_cmsplugin_ptr.parent,
                placeholder=old_cmsplugin_ptr.placeholder,
                depth=old_cmsplugin_ptr.depth,
                numchild=old_cmsplugin_ptr.numchild,
                path=old_cmsplugin_ptr.path,
                cmsplugin_ptr_id=old_object.cmsplugin_ptr_id,
            )
            old_object.delete()
            new_object.save()
        return True
    except LookupError:
        return False


def forwards_filer_link(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> bool:
    """Migrate data from cmsplugin_filer_link to djangocms_file_link."""
    try:
        cmsplugin_filer_link = apps.get_model('cmsplugin_filer_link', 'FilerLinkPlugin')  # type: Type[FilerLinkPlugin]
        djangocms_file_link = apps.get_model('djangocms_link', 'Link')  # type: Type[Link]
        djangocms_file_file = apps.get_model('djangocms_file', 'File')  # type: Type[File]
        for old_object in cmsplugin_filer_link.objects.all():
            if old_object.file:
                new_object = djangocms_file_file(
                    # Style has never been used by us ... and has no equivalent in the new model.
                    #old_object.style

                    file_name=old_object.name,
                    file_src=old_object.file,
                    link_target='_blank' if old_object.new_window else '',
                    link_title=old_object.name,
                    attributes=old_object.link_attributes,
                    template=get_file_templates()[0][0],

                    # show_file_size was the default in cmsplugin_filer_file
                    # Setting this to 1 would keep the old behaviour.
                    # One could also let this be the default.
                    show_file_size=1,

                    # fields for the cms_cmsplugin table
                    plugin_type='FilePlugin',
                    position=old_object.position,
                    language=old_object.language,
                    creation_date=old_object.creation_date,
                    changed_date=old_object.changed_date,
                    parent=old_object.parent,
                    placeholder=old_object.placeholder,
                    depth=old_object.depth,
                    numchild=old_object.numchild,
                    path=old_object.path,
                    cmsplugin_ptr_id=old_object.cmsplugin_ptr_id,
                )
                old_object.delete()
                new_object.save()
            else:
                new_object = djangocms_file_link(
                    attributes=old_object.link_attributes,
                    external_link=old_object.url if old_object.url else '',
                    internal_link_id=old_object.page_link_id if old_object.page_link else None,
                    mailto=old_object.mailto if old_object.mailto else '',
                    name=old_object.name,
                    target='_blank' if old_object.new_window else '',

                    # anchor and phone are unset and therefore remain in there default values.
                    #anchor
                    #phone

                    # Adjust this to your needs:
                    template='more' if old_object.link_style == ' more ' else 'default',

                    # fields for the cms_cmsplugin table
                    plugin_type='LinkPlugin',
                    position=old_object.position,
                    language=old_object.language,
                    creation_date=old_object.creation_date,
                    changed_date=old_object.changed_date,
                    parent=old_object.parent,
                    placeholder=old_object.placeholder,
                    depth=old_object.depth,
                    numchild=old_object.numchild,
                    path=old_object.path,
                    cmsplugin_ptr_id=old_object.cmsplugin_ptr_id,
                )
                old_object.delete()
                new_object.save()
        return True
    except LookupError:
        return False


def forwards_filer_file(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> bool:
    """Migrate data from cmsplugin_filer_file to djangocms_file_file."""
    try:
        cmsplugin_filer_file = apps.get_model('cmsplugin_filer_file', 'FilerFile')  # type: Type[FilerFile]
        djangocms_file_file = apps.get_model('djangocms_file', 'File')  # type: Type[File]

        for old_object in cmsplugin_filer_file.objects.all():
            new_object = djangocms_file_file(
                # Style has never been used by us ... and has no equivalent in the new model.
                #old_object.style

                file_name=old_object.title,
                file_src=old_object.file,
                link_target='_blank' if old_object.target_blank else '',
                link_title=old_object.title,
                attributes=old_object.link_attributes,
                template=get_file_templates()[0][0],

                # show_file_size was the default in cmsplugin_filer_file
                # Setting this to 1 would keep the old behaviour.
                # One could also let this be the default.
                show_file_size=1,

                # fields for the cms_cmsplugin table
                plugin_type='FilePlugin',
                position=old_object.position,
                language=old_object.language,
                creation_date=old_object.creation_date,
                changed_date=old_object.changed_date,
                parent=old_object.parent,
                placeholder=old_object.placeholder,
                depth=old_object.depth,
                numchild=old_object.numchild,
                path=old_object.path,
                cmsplugin_ptr_id=old_object.cmsplugin_ptr_id,
            )
            old_object.delete()
            new_object.save()
        return True
    except LookupError:
        return False


def forwards_filer_image(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> bool:
    """Migrate data from cmsplugin_filer_image to djangocms_picture."""

    try:
        cmsplugin_filer_image = apps.get_model('cmsplugin_filer_image', 'FilerImage')  # type: Type[FilerImage]
        djangocms_picture = apps.get_model('djangocms_picture', 'Picture')  # type: Type[Picture]
        for old_object in cmsplugin_filer_image.objects.all():
            attributes = {}

            if old_object.alt_text:
                attributes.update({'alt': old_object.alt_text})

            if old_object.image and not old_object.height and old_object.width:
                # height was not externally defined: use ratio to scale it by the width
                old_object.height = int(
                    float(old_object.width) * float(old_object.image._height) / float(old_object.image._width))
            elif old_object.image and not old_object.width and old_object.height:
                # width was not externally defined: use ratio to scale it by the height
                old_object.width = int(
                    float(old_object.height) * float(old_object.image._width) / float(old_object.image._height))

            if old_object.free_link:
                link_url = old_object.free_link
            elif old_object.file_link:
                link_url = STATIC_URL[:-1] + old_object.file_link.file.url
            else:
                link_url = ''

            new_object = djangocms_picture(
                # style has never been used in our ... and has no equivalent in the new model
                # Adjust this to your needs.
                # Maybe you can use your old styles as new templates.
                #old_object.style

                # We ignore the description, because we barely use it and where, we did it wrong.
                #old_object.description,

                use_no_cropping=old_object.use_original_image,
                link_target='_blank' if old_object.target_blank else '',
                link_url=link_url,
                link_page=old_object.page_link,
                caption_text=old_object.caption_text if old_object.caption_text else '',
                external_picture=old_object.image_url if old_object.image_url else '',
                use_automatic_scaling=old_object.use_autoscale,
                width=old_object.width,
                height=old_object.height,
                use_crop=old_object.crop,
                use_upscale=old_object.upscale,
                alignment=old_object.alignment if old_object.alignment else '',
                picture=old_object.image,
                thumbnail_options=old_object.thumbnail_option,
                attributes=attributes,
                link_attributes=old_object.link_attributes,

                # defaults for fields that don't exist in the old_object
                template=get_picture_templates()[0][0],

                # use_responsive_image is a new field, and left to its default.
                #use_responsive_image

                # fields for the cms_cmsplugin table
                plugin_type='PicturePlugin',
                position=old_object.position,
                language=old_object.language,
                creation_date=old_object.creation_date,
                changed_date=old_object.changed_date,
                parent=old_object.parent,
                placeholder=old_object.placeholder,
                depth=old_object.depth,
                numchild=old_object.numchild,
                path=old_object.path,
                cmsplugin_ptr_id=old_object.cmsplugin_ptr_id,
            )

            old_object.delete()
            new_object.save()
        return True
    except LookupError:
        return False


def forwards(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    # Disable forwards if you don't need them:
    forwards_filer_file(apps, schema_editor)
    #forwards_filer_folder(apps, schema_editor)
    forwards_filer_image(apps, schema_editor)
    forwards_filer_link(apps, schema_editor)


class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
    dependencies = [
        ('djangocms_file', '0011_auto_20181211_0357'),
        ('djangocms_picture', '0009_auto_20181212_1003'),
        ('djangocms_link', '0013_fix_hostname'),
        #('cmsplugin_filer_file', '0005_auto_20160713_1853'),
    ]
