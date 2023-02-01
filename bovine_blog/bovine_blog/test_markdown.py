from markdown import Markdown


def test_markdown():
    md = Markdown(extensions=["mdx_math"])

    result = md.convert(
        "This is \\(\\mathrm{e}^{2\\pi\\mathrm{i}}+1=0\\) Euler's equation"
    )

    assert (
        result
        == '<p>This is <script type="math/tex">\\mathrm{e}^{2\\pi\\mathrm{i}}+1=0</script> Euler\'s equation</p>'
    )
