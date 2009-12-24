# Unfluff

A statistical content extraction tool written in python - remove the useless fluff from arbitrary HTML pages.

Based on methods discussed (and implemented) in various places, but most directly:

 - [http://www.spicylogic.com/allenday/blog/2008/05/27/statistical-html-content-extraction/](http://www.spicylogic.com/allenday/blog/2008/05/27/statistical-html-content-extraction/)
 - [http://www2003.org/cdrom /papers/refereed/p583/p583-gupta.html](http://www2003.org/cdrom/papers/refereed/p583/p583-gupta.html)

An experiment / work in progress.

### Usage:

The command line tool can either take a file or a URL to extract. It prints the content tree to stdout:

	unfluff /path/to/something.html

or

	unfluff -u 'http://some-website.com/interesting-article.html'

The `unfluff` library has a few functions, which pretty much all do the same thing via different formats:

	import unfluff
	unfluff.from_url('http://whatever/')
	unfluff.from_file('/tmp/input.html')
	unfluff.from_string("<html>inline content</html>")

### Requirements:

 - lxml (fancy HTML parsing)
 - scipy (fancy maths)

Both of these are native (C) extensions, which means you're best off looking for them in your friendly
neighborhood package manager.


#### Licence:

BSD

