import unittest

from docforest import DocForest, DocStyle


class TestChunking(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None
        self.doc_forest = DocForest(style=DocStyle.MARKDOWN)

    def test_chunking_empty(self):
        content = ""
        expected_output = []
        result = self.doc_forest.chunk(content=content)

        self.assertEqual(result, expected_output)

    def test_chunking_plain_text(self):
        content = "This is a test sentence. This is another test sentence."
        expected_output = []
        result = self.doc_forest.chunk(content=content)

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
        result = self.doc_forest.chunk(content=content)

        self.assertEqual(result, expected_output)

    def test_chunking_markdown_content_with_no_headings(self):
        content = (
            "This is a test sentence.\n"
            "This is another test sentence.\n"
            "# This is section level 1\n"
            "content in section level 1"
        )
        expected_output = ["# This is section level 1\ncontent in section level 1"]
        result = self.doc_forest.chunk(content=content)

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
        result = self.doc_forest.chunk(content=content)

        self.assertEqual(result, expected_output)

    def test_chunking_markdown_same_level(self):
        content = (
            "# section level 1 - 1\n"
            "content in section level 1\n"
            "# section level 1 - 2\n"
            "content in section level 1\n"
            "# section level 1 - 3\n"
            "content in section level 1\n"
            "# section level 1 - 4\n"
            "content in section level 1\n"
        )
        expected_output = [
            ("# section level 1 - 1\ncontent in section level 1"),
            ("# section level 1 - 2\ncontent in section level 1"),
            ("# section level 1 - 3\ncontent in section level 1"),
            ("# section level 1 - 4\ncontent in section level 1"),
        ]
        result = self.doc_forest.chunk(content=content)

        self.assertEqual(result, expected_output)

    def test_chunking_markdown_skipping_heading_levels(self):
        content = (
            "# section level 1\n"
            "content in section level 1\n"
            "#### section level 4\n"
            "content in section level 4\n"
            "### section level 3 again\n"
            "content in section level 3 again\n"
        )
        expected_output = [
            (
                "# section level 1\n"
                "content in section level 1\n"
                "#### section level 4\n"
                "content in section level 4"
            ),
            (
                "# section level 1\n"
                "content in section level 1\n"
                "### section level 3 again\n"
                "content in section level 3 again"
            ),
        ]
        result = self.doc_forest.chunk(content=content)

        self.assertEqual(result, expected_output)

    def test_chunking_markdown_medium(self):
        content = (
            "# section level 1\n"
            "content in section level 1\n"
            "## section level 2\n"
            "content in section level 2\n"
            "### section level 3\n"
            "content in section level 3\n"
            "## section level 2 again\n"
            "content in section level 2 again\n"
            "### section level 3 again\n"
            "content in section level 3 again\n"
            "## section level 2 yet again\n"
            "content in section level 2 yet again\n"
            "### section level 3 yet again\n"
            "content in section level 3 yet again\n"
            "### section level 3 yet again\n"
            "content in section level 3 yet again"
        )
        expected_output = [
            (
                "# section level 1\n"
                "content in section level 1\n"
                "## section level 2\n"
                "content in section level 2\n"
                "### section level 3\n"
                "content in section level 3"
            ),
            (
                "# section level 1\n"
                "content in section level 1\n"
                "## section level 2 again\n"
                "content in section level 2 again\n"
                "### section level 3 again\n"
                "content in section level 3 again"
            ),
            (
                "# section level 1\n"
                "content in section level 1\n"
                "## section level 2 yet again\n"
                "content in section level 2 yet again\n"
                "### section level 3 yet again\n"
                "content in section level 3 yet again"
            ),
            (
                "# section level 1\n"
                "content in section level 1\n"
                "## section level 2 yet again\n"
                "content in section level 2 yet again\n"
                "### section level 3 yet again\n"
                "content in section level 3 yet again"
            ),
        ]
        result = self.doc_forest.chunk(content=content)

        self.assertEqual(result, expected_output)
