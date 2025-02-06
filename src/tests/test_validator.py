import unittest
from utils.validator import validate_ticket

class TestValidator(unittest.TestCase):

    def test_valid_ticket(self):
        ticket_info = {'public_id': '12345', 'first_name': 'John', 'last_name': 'Doe'}
        result = validate_ticket(ticket_info)
        self.assertTrue(result)

    def test_invalid_ticket_public_id(self):
        ticket_info = {'public_id': 'invalid_id', 'first_name': 'John', 'last_name': 'Doe'}
        result = validate_ticket(ticket_info)
        self.assertFalse(result)

    def test_invalid_ticket_name(self):
        ticket_info = {'public_id': '12345', 'first_name': 'Invalid', 'last_name': 'Name'}
        result = validate_ticket(ticket_info)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()