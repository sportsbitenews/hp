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
# If not, see <http://www.gnu.org/licenses/>.

from django.conf import settings
from django.db.models import Q
from django.http import Http404
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Page
from .models import BlogPost


class TranslateSlugViewMixin(object):
    """A view mixin that allows DetailView to work with translated slugs.

    .. WARNING:: This mixin assumes:

       * There is a ``slug`` kwarg in the URL config
       * The model has a translated slug field (like core.BlogPost and core.Page)
       * The model has a ``get_absolute_url()`` method.

    Background: By default, get_object() would filter for the slug field, the translated
    database field uses the current active language. So this queryset::

        >>> from core.models import Page
        >>> Page.objects.filter(slug='foo')

    ... returns a different result depending on the browser language (on the database level,
    this would result in a ``WHERE slug_en="foo"`` in an English browser). This means that
    the URL "/page/english-slug" works in an English browser but NOT in a German browser.

    So ``get_object()`` is overwritten to filter for all language slugs. ``get()`` additionally
    returns a redirect to the slug in the current language if it's not the same as the one viewed.
    """

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # If the slug used in the view is different from the slug in the current language, redirect
        # to the latter.
        if kwargs['slug'] != self.object.slug.current:
            return HttpResponseRedirect(self.object.get_absolute_url())

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        slug = self.kwargs.get(self.slug_url_kwarg)

        # filter for slugs in all languages
        filter = Q()
        for lang, _name in settings.LANGUAGES:
            filter |= Q(**{'slug_%s' % lang: slug})

        queryset = queryset.filter(filter)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj


class PageView(TranslateSlugViewMixin, DetailView):
    queryset = Page.objects.filter(published=True)


class BlogPostListView(ListView):
    queryset = BlogPost.objects.filter(published=True).order_by('-sticky', '-created')


class BlogPostView(TranslateSlugViewMixin, DetailView):
    queryset = BlogPost.objects.filter(published=True)
    context_object_name = 'post'
