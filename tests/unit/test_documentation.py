from pathlib import Path
import tempfile
import unittest

from scripts.validate_documentation import check_file


class DocumentationTests(unittest.TestCase):
    def test_examples_external_links_and_fences_are_not_local_targets(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / 'guide.md'
            path.write_text('~~~bash\n[example](missing)\n~~~\n'
                            '`[inline](missing)`\n[official](https://example.com/docs)\n'
                            '[local](guide.md#heading)\n[anchor](#heading)\n')
            self.assertEqual(check_file(path, root), [])

    def test_missing_target_escape_image_and_unclosed_fence_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / 'guide.md'
            path.write_text('[broken](missing.md)\n[escape](../outside.md)\n'
                            '![image](missing.png)\n```python\ncode\n')
            errors = check_file(path, root)
            self.assertEqual(len(errors), 4)
            self.assertTrue(any('unclosed' in error for error in errors))
