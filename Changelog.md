# Changelog

## 2016-09-11

* Improve logging configuration to make sure that logging calls are properly logged in any
  configuration, via uWSGI and Celery. `log.error()` and exceptions in Celery tasks are now mailed
  to admins.
* The set-language view (`/api/set-lang/`) no longer fails if any query parameter is missing. The
  query string is also passed via the `next` query parameter.
* Add `rel="nofollow"` set-language links.
* Remove dependency for python-gnupg (we use pygpgme now).

### Contact form

* Do not CC the message to anonymous users, to make sure that the contact form cannot be abused to
  send SPAM.
* Set the Reply-To header to the contact address and the users address. That way we can just hit
  "Reply" to answer more quickly.
* Add the IP-Address that submitted the contact form is passed in the `X-Homepage-Submit-Address`
  header.
* The user currently logged in, if any, is passed in the `X-Homepage-Logged-In-User` header.
* Add the users GPG keys as attachement, if he has configured any.