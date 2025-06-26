from django.test import TestCase

# Create your tests here.
class SamoleTestCase(TestCase):
    def test_sample1(self):
        self.assertEqual(1 + 2, 3)
