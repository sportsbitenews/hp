# -*- coding: utf-8 -*-
#
# This file is part of the jabber.at homepage (https://github.com/jabber-at/hp).
#
# This project is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This project is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with django-xmpp-account.
# If not, see <http://www.gnu.org/licenses/.

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import gettext_lazy as _

from composite_field.l10n import LocalizedField
from composite_field.base import CompositeField
from mptt.admin import DraggableMPTTAdmin
from tinymce.widgets import TinyMCE

from .models import BlogPost
from .models import Page
from .models import MenuItem
from .models import User


class BasePageAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {
            'widget': TinyMCE(attrs={'cols': 80, 'rows': 10}, mce_attrs={
                'theme': "advanced",
            }),
        },
    }

    def get_readonly_fields(self, request, obj=None):
        fields = list(super(BasePageAdmin, self).get_readonly_fields(request, obj=obj))
        if 'author' not in fields:
            fields.append('author')
        return fields

    def get_actions(self, request):
        actions = super(BasePageAdmin, self).get_actions(request)

        context = {
            'models': self.model._meta.verbose_name_plural,
        }

        actions['make_publish'] = (
            self.make_publish, 'make_publish', self.make_publish.short_description % context,
        )
        actions['make_unpublish'] = (
            self.make_unpublish, 'make_unpublish', self.make_unpublish.short_description % context,
        )
        return actions

    def _get_composite_field_tuple(self, fields):
        new_fields = []
        for name in fields:
            if not isinstance(name, str):  # don't handle tuples et al
                new_fields.append(name)
                continue

            field = self.model._meta.get_field(name)

            if isinstance(field, LocalizedField):
                new_fields.append(tuple([f.name for f in field.subfields.values()]))
            elif isinstance(field, CompositeField):
                new_fields += [f.name for f in field.subfields.values()]
            else:
                new_fields.append(name)
        return new_fields

    def _get_subfields(self, name):
        return tuple([f.name for f in self.model._meta.get_field(name).subfields.values()])

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(BasePageAdmin, self).get_fieldsets(request, obj=obj)

        if self.fieldsets is None and self.fields is None:
            # The ModelAdmin class doesn't set fields or fieldsets - we replace localized
            # fields with tuples.
            fields = []
            has_title = has_slug = has_text = False
            title_fields = self._get_subfields('title')
            slug_fields = self._get_subfields('slug')
            text_fields = self._get_subfields('text')
            for field in fieldsets[0][1]['fields']:
                if field in title_fields:
                    if has_title is False:
                        fields.append(title_fields)
                        has_title = True
                elif field in slug_fields:
                    if has_slug is False:
                        fields.append(slug_fields)
                        has_slug = True
                elif field in text_fields:
                    if has_text is False:
                        fields.append(text_fields)
                        has_text = True
                else:
                    fields.append(field)

            fieldsets[0][1]['fields'] = list(fields)
        else:
            # ModelAdmin sets fields or fieldsets. This means that e.g. 'title' should
            # be replaced with ('title_de', 'title_en').
            for name, options in fieldsets:
                options['fields'] = self._get_composite_field_tuple(options['fields'])

        return fieldsets

    def render_change_form(self, request, context, add, **kwargs):
        """Override to add javascript only when adding an object.

        It adds Javascript to dynamically calculate the slug of a BasePage object and set the field
        accordingly.

        Ordinarily you would add Javascript in a Media subclass, but then it would get *always*
        added. The form for adding/changing an object is identical, so there is no way to only
        act when adding a form (and you don't normally want to change existing slugs, since they're
        part of the URL).
        """

        if add:
            context['media'] += forms.Media(js=("core/js/basepage-add.js", ))
        return super(BasePageAdmin, self).render_change_form(request, context, add, **kwargs)

    def save_model(self, request, obj, form, change):
        if change is False:  # adding a new object
            obj.author = request.user
        obj.save()

    #################
    # Admin actions #
    #################
    def make_publish(self, request, queryset):
        queryset.update(published=True)
    make_publish.short_description = _('Publish selected %(models)s')

    def make_unpublish(self, request, queryset):
        queryset.update(published=False)
    make_unpublish.short_description = _('Unpublish selected %(models)s')


@admin.register(BlogPost)
class BlogPostAdmin(BasePageAdmin):
    fields = ['title', 'slug', 'text', ('published', 'sticky'), 'author']

@admin.register(Page)
class PageAdmin(BasePageAdmin):
    fields = ['title', 'slug', 'text', 'published', 'author']


@admin.register(MenuItem)
class MenuItemAdmin(DraggableMPTTAdmin):
    list_display = (
        'tree_actions',
        'indented_title',
    )
    list_display_links = (
        'indented_title',
    )

@admin.register(User, app_label='auth')
class UserAdmin(admin.ModelAdmin):
    app_label = 'auth'

admin.site.unregister(Group)
