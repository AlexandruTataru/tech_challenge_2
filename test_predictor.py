"""
test_predictor.py
"""
import unittest
import api


class MyTestCase(unittest.TestCase):
    """Main test class"""
    def test_predict_api_insufficient_data(self):
        """Validate the exception generated when dataset is not large enough"""
        with self.assertRaises(api.APIException) as context:
            api.predict_next([])
        self.assertTrue('Dataset must contain at least 10 entries' in str(context.exception))


if __name__ == '__main__':
    unittest.main()
