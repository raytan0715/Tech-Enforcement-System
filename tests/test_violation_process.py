import unittest
from services.violation_process import process_violation

class TestViolationProcess(unittest.TestCase):

    def test_process_violation(self):
        test_data = {
            'cam_id': '12345',
            'speed_limit': 60,
            'current_speed': 80,
            'licence_plate': 'ABC-123',
            'location': 'Street 1',
            'date_time': '2024-12-22 20:00:00',
            'image': 'path/to/image.jpg'
        }
        result = process_violation(test_data)
        self.assertEqual(result['status'], 'success')
        self.assertIn('data', result)

if __name__ == '__main__':
    unittest.main()
