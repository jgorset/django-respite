History
-------

1.1.2
^^^^^

* Database settings now compatible with django 1.4.
* Added a test for the JSON serializer.
* Fixes a bug when submitting unicode content through the JSON middleware.
* The JSON middleware now accept encodings other than UTF-8.
* Fixed a bug where the `parse_content_type` included "charset=".
* Fixed a bug in the form serializer test.

1.1.1
^^^^^

* You may now render errors more easily with ``View#_error``.
* Respite will now automatically serialize DateQuerySet and ValuesListQuerySet.

1.1.0
^^^^^

* Respite now serializes JSONP.
* Fixed a bug that caused an AttributeError upon attempting to serialize a top-level list as XML.

1.0.0
^^^^^

* Respite now parses JSON payloads in the body of POST, PUT and PATCH requests.
* Fixed a bug that caused Resource#update to raise a FieldError if request.PATCH
  contained attributes that didn't match its model.
* Fixed a bug that caused a TypeError upon serializing 'None' as XML.

0.11
^^^^

* Respite now supports serialization of any object that defines a 'serialize' method.
* Fixed a bug that caused a TypeError upon attempting to serialize long types.
* Routes are no longer prefixed with the application name.
* The 'prefix' argument to 'resource' now defaults to an empty string.
* Resource#create now returns 201 Created instead of 303 See Other upon creating a new model.
* Respite now defaults to the first of the view's supported formats instead of RESPITE_DEFAULT_FORMAT
  for the wildcard content type (*/*).
* View#_render has a new argument; 'prefix_template_path'.
* Respite's default views now render 404s in the request format.

0.10.4
^^^^^^

* Respite now discards the '_method' parameter on HTTP POST.

0.10.3
^^^^^^

* Resource now has a 'routes' property that contains a list of routes for each of the default views.
* Respite now automatically serializes request context as XML if no XML template for the
  view exists.

0.10.2
^^^^^^

* Respite now automatically serializes many-to-many fields
* Fixed a bug that caused Resource#update to fail form validation for models with many-to-many fields or foreign keys
* Fixed a bug that caused the model in the template context of Resource#index to be in mixedCase rather than underscore_case.

0.10.1
^^^^^^

* Fixed a bug that caused JSON to be serialized as a byte stream with unicode code points.
* Respite now explicitly specifies the charset in the HTTP 'Content-Type' header.

0.10
^^^^

* Respite's default views are now defined in the 'Resource' class.
* Routing has been changed to leverage decorators (see README for details).
* Fixed a bug that caused HTTP Accept headers with whitespace to be parsed incorrectly.

0.9.2
^^^^^

* The '*/*' content type now defaults to the format given in RESPITE_DEFAULT_FORMAT.

0.9.1
^^^^^

* Fixed a bug that caused lambas to be expanded into the default route object, producing
  issues with consequent resource declarations.
* Added route for Views#replace to 'routes.all'.

0.9
^^^

* Respite now supports HTTP PATCH, and routes it to Views#update.
* HTTP PUT is now routed to Views#replace instead of Views#update.

0.8
^^^

* Routing has been redesigned (see README for details).

0.7.6
^^^^^

* Fixed a bug that caused a KeyError upon receiving requests whose methods
  were not GET, POST, PUT or DELETE
* You may now pass a dictionary of HTTP headers to Views#_render.
* Views#_render no longer requires a template.
* Views#_render's 'template' argument now defaults to 'None'.
* Views#_render's 'status' argument now defaults to '200'.
* Respite now responds to HTTP OPTIONS.
* Respite now responds to HTTP HEAD.

0.7.5
^^^^^

* Fixed a bug that caused views for models in CamelCase to be routed incorrectly.
* Fix a bug that caused views to default to the format given in DEFAULT_FORMAT
  regardless of whether or not it was supported.
* Fix a bug that allowed for arbitrary URL suffixes

0.7.4
^^^^^

* You may now override the regular expression used to match resource IDs in the 'id_regex'
  argument to the 'resource' function.
* Fix a bug that caused a TypeError upon attempting to serialize a float.

0.7.3
^^^^^

* You may now decorate methods with the 'override_supported_formats' decorator to override
  the view class' supported formats.
* Fixed a bug that caused a TypeError upon returning non-simple datatypes from a
  model's 'serialize' method.

0.7.2
^^^^^

* Fixed a bug that caused custom actions to be prefixed by an additional slash.

0.7.1
^^^^^

* Add serializer for filefields
* Fix bug when trying to serialize a NoneType

0.7
^^^

* You may now pass a custom form class in Views#form to override automatic form generation
  in Views#new, Views#create, Views#edit and Views#update.
* 'HTTPMethodOverrideMiddleware' has been renamed to 'HttpMethodOverrideMiddleware'.
* 'HTTPPUTMiddleware' has been renamed to 'HttpPutMiddleware'.
* Respite now automatically serializes request context as JSON if no JSON template for the
  view exists.

0.6.1
^^^^^

* Fixed a bug that caused views with no prefix to be routed incorrectly
* Fixed a bug that caused the regular expressions to allow arbitrary input
  between the prefix and action (e.g. news/articles/FOO/index.html).

0.6
^^^

* Fixed a bug that caused an empty prefix to produce URLs with double slashes.
* The 'View' class has been renamed to 'Views'.
* The trailing slash of the 'resource' function's 'prefix' argument is no longer implicit.
* The trailing slash of the 'View' class' 'template_path' property is no longer implicit.

0.5
^^^

* URL pattern names are now prefixed with the model's application name (e.g. 'edit_news_article').

0.4
^^^

* Custom actions may now be routed by HTTP method.
