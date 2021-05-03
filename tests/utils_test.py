"Utils tests."
import unittest
from app.commons.utils import validate_input
from app.commons.schema import create_ingredient
from app.commons.errors import FailedRequest


class TestUtils(unittest.TestCase):
    """Writer test case."""

    def test_validator(self):
        """
        Testing validator.

        :return:
        """
        data = {
            "name": "butter",
            "measure_unit": "ml"
        }

        with self.assertRaises(FailedRequest) as err:
            validate_input({'name': 'peanut'}, create_ingredient)
        self.assertTrue('measure_unit' in err.exception.payload)
        self.assertTrue(err.exception.payload['measure_unit'][0] == 'required field')

        check = validate_input(data, create_ingredient)
        self.assertTrue('name' in check and 'measure_unit' in check)
        self.assertEqual(check['name'], data['name'])
        self.assertEqual(check['measure_unit'], data['measure_unit'])
