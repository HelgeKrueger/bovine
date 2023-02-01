import logging
import sys
from datetime import datetime, timedelta

from markdown import Markdown
from quart import Quart

from bovine_blog.html import html_blueprint
from bovine_blog.stores.static import StaticStore
from bovine_blog.stores.types import PostEntry
from bovine_blog.utils import rewrite_activity_request

log_format = "[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format, stream=sys.stdout)


md = Markdown(extensions=["mdx_math"])


app = Quart(__name__)

app.before_request(rewrite_activity_request)
app.register_blueprint(html_blueprint)

static_store = StaticStore()
content = """
<p>This is an attempt at providing content,
when I cannot just google lorem ipsum due
to my internet being down. Whoever is reading
this, please admire my ability to code without
internet.</p>

<p>Every great test text should contain some
formatting. <b>So this is bold</b>, <i>This
is in italic</i>. <a href="https://activitypub.rocks/">This is a link,
one can click to test if one has internet</a>.

<blockquote>I enjoy quoting myself.</blockquote>

<code>import pandas as pd, sys
df = pd.read_csv(sys.argv[1])
df.to_excel(sys.argv[1].replace('.csv', '.xlsx'), sheet_name="oh_yeah")</code>
"""

post_entry = PostEntry("local_id", "author", datetime.now(), content)
other_entry = PostEntry(
    "new_id", "other", datetime.now(), "<p>Different content</p>" + content
).set_in_reply_to("/author/local_id")
earlier_entry = PostEntry(
    "local_id",
    "author",
    datetime.now() - timedelta(hours=7),
    "<p>I got up earlier, so I come last</p>" + content,
)


math_md = """
Sometimes Euler's formula makes me happy
\\[
\\mathrm{e}^{\\mathrm{i}\\cdot \\pi} + 1 = 0
\\]
"""
math_entry = PostEntry(
    "math_id", "author", datetime.now() - timedelta(hours=1), md.convert(math_md)
)

static_store.add_entry(earlier_entry)
static_store.add_entry(post_entry)
static_store.add_entry(other_entry)
static_store.add_entry(math_entry)

app.config.update({"data_store": static_store, "domain_name": "test_application"})

if __name__ == "__main__":
    app.run()
