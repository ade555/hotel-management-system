from django.test import TestCase
from hotel.models import *

class TestHotelModels(TestCase):
    def test_string_representatio(self):
        # RoomType Model Test
        room_type = RoomType.objects.create(room_type='Standard')
        self.assertEqual(str(room_type), "Standard")

        # RoomProperties Model Test
        room_properties = RoomProperties.objects.create(room_type=room_type, number_of_beds=1, capacity=2, price_per_night=1.2)
        expected_string = "Standard - Beds: 1, Capacity: 2"
        self.assertEqual(str(room_properties), expected_string)