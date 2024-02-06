import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from dramapi.models import Color, Entry, Rating, Type
from rest_framework.authtoken.models import Token


class EntryTests(APITestCase):

    fixtures = ['users', 'tokens', 'types', 'colors', 'ratings']

    def setUp(self):
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_entry(self):
        '''Ensure we can create a new entry'''

        # Define the endpoint in the API to which
        # the request will be sent
        url = "/entries"

        # Define the request body
        data = {
            "whiskey": "Test Whiskey",
            "type_id": 7,
            "country": "USA",
            "part_of_country": "Tennessee",
            "age_in_years": 12,
            "proof": 100,
            "color_id": 10,
            "mash_bill": "100% malted barley",
            "maturation_details": "former Tennessee whiskey barrels",
            "nose": "roasted grain, caramel, vanilla",
            "palate": "apple pie, vanilla icecream",
            "finish": "long and sweet",
            "rating_id": 5,
            "notes": "tasty whiskey"
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the entry was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["whiskey"], "Test Whiskey")
        self.assertEqual(json_response["whiskey_type"], {
                         'id': 7, 'label': 'Single Malt'})
        self.assertEqual(json_response["country"], "USA")
        self.assertEqual(json_response["part_of_country"], "Tennessee")
        self.assertEqual(float(json_response["age_in_years"]), 12.00)
        self.assertEqual(float(json_response["proof"]), 100.00)
        self.assertEqual(json_response["color"]["id"], 10)
        self.assertEqual(json_response["color"]["label"], "amontillado sherry")
        self.assertEqual(float(json_response["color"]["color_grade"]), 0.9)
        self.assertEqual(json_response["color"]["hex_code"], "F7C23B")
        self.assertEqual(json_response["color"]
                         ["tailwind_name"], "amontillado-sherry")
        self.assertEqual(json_response["mash_bill"], "100% malted barley")
        self.assertEqual(
            json_response["maturation_details"], "former Tennessee whiskey barrels")
        self.assertEqual(json_response["nose"],
                         "roasted grain, caramel, vanilla")
        self.assertEqual(json_response["palate"],
                         "apple pie, vanilla icecream")
        self.assertEqual(json_response["finish"], "long and sweet")
        self.assertEqual(json_response["rating"], {
                         'id': 5, 'number_rating': 4, 'label': 'very good'})
        self.assertEqual(json_response["notes"], "tasty whiskey")

    def test_get_entry(self):
        '''Ensure we can get an existing entry'''

        # Seed the database with an entry.
        entry = Entry()
        entry.whiskey = "Test Whiskey"
        entry.whiskey_type = Type.objects.get(pk=7)
        entry.country = "USA"
        entry.part_of_country = "Tennessee"
        entry.age_in_years = 12
        entry.proof = 100
        entry.color = Color.objects.get(pk=10)
        entry.mash_bill = "100% malted barley"
        entry.maturation_details = "former Tennessee whiskey barrels"
        entry.nose = "roasted grain, caramel, vanilla"
        entry.palate = "apple pie, vanilla icecream"
        entry.finish = "long and sweet"
        entry.rating = Rating.objects.get(pk=5)
        entry.notes = "tasty whiskey"
        entry.user = self.user

        entry.save()

        # Initiate a request and store response.
        response = self.client.get(f"/entries/{entry.id}")

        # Parse the JSON in the response body.
        json_response = json.loads(response.content)

        # Assert that the entry was retrieved.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct.
        self.assertEqual(json_response["whiskey"], "Test Whiskey")
        self.assertEqual(json_response["whiskey_type"], {
                         'id': 7, 'label': 'Single Malt'})
        self.assertEqual(json_response["country"], "USA")
        self.assertEqual(json_response["part_of_country"], "Tennessee")
        self.assertEqual(float(json_response["age_in_years"]), 12.00)
        self.assertEqual(float(json_response["proof"]), 100.00)
        self.assertEqual(json_response["color"]["id"], 10)
        self.assertEqual(json_response["color"]["label"], "amontillado sherry")
        self.assertEqual(float(json_response["color"]["color_grade"]), 0.9)
        self.assertEqual(json_response["color"]["hex_code"], "F7C23B")
        self.assertEqual(json_response["color"]
                         ["tailwind_name"], "amontillado-sherry")
        self.assertEqual(json_response["mash_bill"], "100% malted barley")
        self.assertEqual(
            json_response["maturation_details"], "former Tennessee whiskey barrels")
        self.assertEqual(json_response["nose"],
                         "roasted grain, caramel, vanilla")
        self.assertEqual(json_response["palate"],
                         "apple pie, vanilla icecream")
        self.assertEqual(json_response["finish"], "long and sweet")
        self.assertEqual(json_response["rating"], {
                         'id': 5, 'number_rating': 4, 'label': 'very good'})
        self.assertEqual(json_response["notes"], "tasty whiskey")
