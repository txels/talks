# Dynastatic websites in Django

Did you know the Django we all know and love can also be a great tool for building static websites?

In this talk I will be covering topics like "what is a static site anyway?", alternative definitions (read-only / read-mostly / read-write sites, pre-generated pages vs generated on demand) to help reframe the conversation.

We will walk through what is provided out of the box by Django (staticfiles and its extension points). We will check out third party applications that leverage those extension points (whitenoise, django-storages...) and what they bring to the table.

We will see a couple of different approaches to leveraging "the static way" (decoupling rendering content from serving) from two different projects:

 - A classic HTML site rendered using `django-distill` to generate a "web-server-friendly" layout.
 - A "static" JSON API for a Single Page Application-style front-end.

Finally, I will show how you can incorporate the "write" (dynamic) parts of the application (to justify the "dynastatic" name and the title of the talk, after all).
