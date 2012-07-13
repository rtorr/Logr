Logr
====
 - - -

I never understood why blogging platforms had to be so complex. In my opinion,
the perfect blog software would adhere to a few important principals:

1. Bells and whistles are a waste of time. They never get used.
2. Less is better. You shouldn't have to waste time configuring.
3. Built with Python. Customizing should be quick and easy.

With these three things in mind, I set out searching for my perfect blogging
platform and found nothing that met my needs. Since I couldn't find what I 
wanted, I did what any good hacker would do: I built it.

The result is Logr, a simple, easy to use blog that operates on Markdown files
To post a new article, simply type it into any text editor and save it to the 
/articles directory and you're done. It will appear as soon as you reload the
page.

Add optional pages. These could contain information about yourself, how one
would go about getting in contact with you, projects you're working on, or
anything else!

Roadmap
=======
 - - - 

- Write a setup file. _python setup.py install_ is all you need to type before
  you're up and running.
- Optional pages that could contain information about you, how to contact you,
  projects you're working on, or anything else.

How It Works
============
 - - -

Logr was designed to be simple, and that's exactly what it is.

Creating a Category
-------------------

To create a new category, create a subdirectory inside the _articles_
directory. The name of the directory will be the name of the category.

Creating an Article
-------------------

Open any text editor and write the article using the Markdown markup language.
When you're done, save it to the appropriate directory. Anything in the 
_articles_ directory will show up in the _Miscellaneous_ category.

The title of the article should be the first line of the file. This is what the
link of the front page and the slug for the article are generated from. Choose
wisely.

All files should be saved as _<filename>.md_. Any files that do not end in
_.md_ will not show up on the website.

For example, if you wanted an article named _An Introduction to Software
Engineering_ to appear in the _Software_ category, the location of the file
would look like this: 

-> **./articles/Software/intro\_to\_software\_engineering.md** <-

All files are translated directly from Markdown to HTML. Keep this in mind when
editing. If you have any questions about the Markdown syntax, they should be
answered [here](http://daringfireball.net/projects/markdown/).
