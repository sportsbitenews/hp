# -*- coding: utf-8 -*-
#
# This file is part of the jabber.at homepage (https://github.com/jabber-at/hp).
#
# This project is free software: you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This project is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License along with this project. If not, see
# <http://www.gnu.org/licenses/>.

import re

import dns.resolver

from django import forms
from django.conf import settings
from django.core.validators import RegexValidator
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from bootstrap.formfields import BootstrapCharField
from bootstrap.formfields import BootstrapEmailField
from bootstrap.formfields import BootstrapFileField
from bootstrap.formfields import BootstrapMixin

from .widgets import DomainWidget
from .widgets import EmailVerifiedDomainWidget
from .widgets import FingerprintWidget
from .widgets import NodeWidget
from .widgets import UsernameWidget


class UsernameField(BootstrapMixin, forms.MultiValueField):
    formgroup_class = 'form-group-username'
    default_error_messages = {
        'syntax': _('The username is invalid.'),
        'exists': _('This username is already taken.'),
        'error': _('Could not check if the username already exists: Error communicating with the server.'),
    }

    def __init__(self, **kwargs):
        self.register = kwargs.pop('register', False)
        kwargs.setdefault('label', _('Username'))

        if self.register is True:
            choices = tuple([(d, d) for d in settings.REGISTER_HOSTS.keys()])
        else:
            choices = tuple([(d, d) for d in settings.MANAGED_HOSTS.keys()])

        if 'help_text' not in kwargs:
            if self.register is True:
                kwargs['help_text'] = _("Your username is used to identify you on the Jabber network.")

        fields = (
            forms.CharField(
                widget=NodeWidget(register=self.register),
                min_length=settings.MIN_USERNAME_LENGTH,
                max_length=settings.MAX_USERNAME_LENGTH,
                error_messages={
                    'min_length': _('Username must have at least %(limit_value)d characters.'),
                    'max_length': _('Username must have at most %(limit_value)d characters.'),
                },
                validators=[
                    RegexValidator(r'^[^@\s]+$', _('Username contains invalid characters.')),
                ],
            ),
            forms.ChoiceField(initial=settings.DEFAULT_XMPP_HOST,
                              choices=choices, widget=DomainWidget),
        )
        widgets = [f.widget for f in fields]

        self.widget = UsernameWidget(widgets=widgets, attrs={})
        super().__init__(fields=fields, require_all_fields=True, **kwargs)

    def get_help_text(self):
        if self.register is True:
            help_text = _(
                'At least %(MIN_LENGTH)s and up to %(MAX_LENGTH)s characters. No "@" or spaces.'
            ) % {
                'MIN_LENGTH': settings.MIN_USERNAME_LENGTH,
                'MAX_LENGTH': settings.MAX_USERNAME_LENGTH,
            }

            default = format_html('<span id="default">{}</span>',
                                  _('Type to see if the username is still available.'))
            available = format_html('<span id="username-available">{}</span>',
                                    _('The username is still available.'))
            not_available = format_html('<span id="username-not-available">{}</span>',
                                        _('The username is no longer available.'))
            invalid = format_html('<span id="invalid">{}</span>',
                                  _('The username is invalid.'))
            error = format_html('<span id="error">{}</span>',
                                _('An error occured, please try again later.'))
            return format_html(
                '''{}<span class="help-block" id="status-check">{}{}{}{}{}</span>''',
                help_text, default, available, not_available, invalid, error)
        return ''

    def compress(self, data_list):
        node, domain = data_list
        node = node.lower()
        return '@'.join(data_list)


class FingerprintField(BootstrapCharField):
    widget = FingerprintWidget
    invalid_feedback = _('Please enter a valid GPG key fingerprint.')

    def __init__(self, **kwargs):
        # "gpg --list-keys --fingerprint" outputs fingerprint with spaces, making it 50 chars long
        kwargs.setdefault('label', _('Fingerprint'))
        kwargs.setdefault('max_length', 50)
        kwargs.setdefault('min_length', 40)
        kwargs.setdefault('required', False)
        kwargs.setdefault('help_text', _(
            'Add your fingerprint (<code>gpg --fingerprint &lt;you@example.com&gt;</code>) if '
            'your key is available on public key servers...'))

        # define error messages
        kwargs.setdefault('error_messages', {})
        kwargs['error_messages'].setdefault('not-enabled', _('GPG not enabled.'))
        kwargs['error_messages'].setdefault('invalid-length',
                                            _('Fingerprint should be 40 characters long.'))
        kwargs['error_messages'].setdefault('invalid-chars',
                                            _('Fingerprint contains invalid characters.'))
        super().__init__(**kwargs)

    def clean(self, value):
        if not getattr(settings, 'GPG_BACKENDS', {}):  # check, just to be sure
            raise forms.ValidationError(self.error_messages['not-enabled'])

        fp = super().clean(value).strip().replace(' ', '').upper()
        if fp == '':
            return None  # no fingerprint given
        if len(fp) != 40:
            raise forms.ValidationError(self.error_messages['invalid-length'])
        if re.search('[^A-F0-9]', fp) is not None:
            raise forms.ValidationError(self.error_messages['invalid-chars'])

        return fp


class KeyUploadField(BootstrapFileField):
    default_error_messages = {
        'not-enabled': _('GPG not enabled.'),
        'mime-type': _('Only plain-text files are allowed (was: %(value)s)!'),
    }
    default_mime_types = {'text/plain', 'application/pgp-encrypted', }

    def __init__(self, **kwargs):
        kwargs.setdefault('required', False)
        kwargs.setdefault('label', _('GPG Key'))
        kwargs.setdefault('help_text', _(
            '... upload your ASCII armored GPG key directly '
            '(<code>gpg --armor --export &lt;fingerprint&gt;</code>).'
        ))

        # define error messages
        super().__init__(**kwargs)

    def clean(self, value, initial=None):
        # This check is just to be sure
        if not getattr(settings, 'GPG_BACKENDS', {}):
            raise forms.ValidationError(self.error_messages['not-enabled'], code='not-enabled')

        return super().clean(value, initial=None)


class EmailVerifiedDomainField(BootstrapEmailField):
    """An email formfield that verifies that the domain actually exists.

    Parameters
    ----------

    kwargs
        All passed to the parent class.
    """
    default_error_messages = {
        'domain-does-not-exist': _('The domain "%(value)s" does not exist.'),
    }
    widget = EmailVerifiedDomainWidget

    def clean(self, *args, **kwargs):
        email = super().clean(*args, **kwargs)
        if not email:
            return email

        _node, domain = email.rsplit('@', 1)
        if domain:
            exists = False
            resolver = dns.resolver.Resolver()

            for typ in ['A', 'AAAA', 'MX']:
                try:
                    resolver.query(domain, typ)
                    exists = True
                    break
                except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
                    continue

            if exists is False:
                raise forms.ValidationError(self.error_messages['domain-does-not-exist'] % {
                    'value': domain,
                }, code='domain-does-not-exist')
        return email
