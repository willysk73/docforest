import unittest

from docforest.main import chunk_document


class TestChunking(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def test_chunking_empty(self):
        content = ""
        expected_output = []
        result = chunk_document(content=content, style="markdown")

        self.assertEqual(result, expected_output)

    def test_chunking_plain_text(self):
        content = "This is a test sentence. This is another test sentence."
        expected_output = []
        result = chunk_document(content=content, style="markdown")

        self.assertEqual(result, expected_output)

    def test_chunking_markdown_only_headings(self):
        content = (
            "# This is section level 1\n"
            "## This is section level 2\n"
            "### This is section level 3\n"
        )
        expected_output = [
            "# This is section level 1\n"
            "## This is section level 2\n"
            "### This is section level 3"
        ]
        result = chunk_document(content=content, style="markdown")

        self.assertEqual(result, expected_output)

    def test_chunking_markdown_easy(self):
        content = (
            "# This is section level 1\n"
            "content in section level 1\n"
            "## This is first section level 2\n"
            "first content in section level 2\n"
            "## This is second section level 2\n"
            "second content in section level 2"
        )
        expected_output = [
            (
                "# This is section level 1\ncontent in section level 1\n"
                "## This is first section level 2\nfirst content in section level 2"
            ),
            (
                "# This is section level 1\ncontent in section level 1\n"
                "## This is second section level 2\nsecond content in section level 2"
            ),
        ]
        result = chunk_document(content=content, style="markdown")

        self.assertEqual(result, expected_output)

    def test_unsupported_style(self):
        with self.assertRaises(ValueError):
            chunk_document(content="Some content", style="unsupported_style")
