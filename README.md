Logr
====
 - - -

Logr was built with a few simple rules in mind:

1. Less is usually better.
2. The ability to customize is good.
3. Python is awesome.

With these three things in mind, I set out to build a simple static blogging
platform that would allow hackers to spend their time writing, instead of having
to worry about what date format they want to use and how many addons they can
get.

There are still a few things the project needs though, and those are outline in
the next section.

Next Feature
============
 - - -

Add optional pages. These could contain information about yourself, how one
would go about getting in contact with you, projects you're working on, or
anything else!

Roadmap
=======
 - - - 

- Include support for code.
- Write setup file.

How It Works
============
 - - -

Logr was designed to be simple, and that's exactly what it is.

To post a new article, all you have to do is create a Markdown file in the
_articles_ directory. Any files in the _articles_ directory will go under the
_Miscellaneous_ category. If you wish to add the new article to a certain
category, just create a subdirectory in _articles_ and leave the file there. 
The name of the category is the same as the name of the subdirectory.

For example, if you wanted an article named _An Introduction to Software
Engineering_ to appear in the _Software Engineering_ category, the location of
the file might look like this:

**./articles/Software\ Engineering/intro\_to\_software\_engineering.md**

There are a few important things to note here:

1. ALL article files that you would like to appear on your site should end in
   _.md_.
2. The title of the article should be the first line of the file.
3. The file will be show as-is. Keep this in mind when editing files.
