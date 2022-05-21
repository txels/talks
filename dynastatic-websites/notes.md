# Dynastatic websites in Django

Did you know the Django we all know and love can also be a great tool for building static websites?

In this talk we will be covering topics like "what is a static site anyway?",
alternative definitions (read-only / read-mostly / read-write sites, pre-generated
pages vs generated on demand) to help reframe the conversation.
So that we don't draw a line between "static site generators like e.g. Nikola" 
versus "web frameworks like e.g. Ruby on Rails - or the python one :)".
I will make an attempt to justify making up a silly word like dynastatic.

We will walk through what is provided out of the box by Django (staticfiles 
and its extension points). 
We will check out third party applications that leverage those extension points (whitenoise,
django-storages...) and what they bring to the table.

We will mention the differences between hosting a static site (plain files) vs a full blown
Django application (Python code, database, etc).
How the meaning of "caching" is different for both cases.

We will see a couple of different approaches to leveraging "the static way"
(decoupling rendering content from serving) to illustrate how we can support
a couple different scenarios.

We will show why it helps to think of reading and writing as separate things, and
argue that any app where producer (writer) use cases are separate from consumer (reader)
ones is a good candidate for static-ification.

We will show that, for read scenarios, a Django view is just a function that converts
a URL into some mostly textual content (HTML/JSON...).

    view = f(str) -> str

We will use some tool like `django-distill` or other approaches to call these functions
ahead of time and generate a "web-server-friendly" layout.

Finally, we will discuss how you can incorporate the "write" (dynamic) parts of the application
(to justify the "dynastatic" name and the title of the talk, after all), both using the
"Javascript SPA" and the NoJS (*) approaches.

[*] NoJS actually means "no custom JS was written as part of this app".
