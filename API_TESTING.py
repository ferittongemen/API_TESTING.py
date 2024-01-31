import unittest
import requests
import json

from HtmlTestRunner import HTMLTestRunner


class APITest(unittest.TestCase):
    url = "https://jsonplaceholder.typicode.com/posts/1"

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_1_api_request_success(self):
        response = requests.get(self.url)
        self.assertEqual(response.status_code, 200, "İstek Başarısız")

    def test_2_api_responses_contains_fields(self):
        response = requests.get(self.url)
        data = response.json()
        print(data)
        self.assertIn("userId", data, "userId alanı bulunamadı")
        self.assertIn("id", data, "id alanı bulunamadı")
        self.assertIn("title", data, "title alanı bulunamadı")
        self.assertIn("body", data, "body alanı bulunamadı")

    def test_3_api_invalid_endpoint(self):
        invalid_url = "https://jsonplaceholder.typicode.com/invalid"
        response = requests.get(invalid_url)
        expected_status_code = 404
        self.assertEqual(response.status_code, expected_status_code,
                         f"Hata! Beklenen {expected_status_code} hatası alınmadı.")

    def test_4_check_data_type(self):
        url = "https://jsonplaceholder.typicode.com/posts"
        response = requests.get(url)
        data = json.loads(response.text)
        self.assertIsInstance(data[0], dict, "Veri Tipi Hatalı")

    def test_5_post_request(self):
        url = "https://jsonplaceholder.typicode.com/posts"
        headers = {'Content-Type': 'application/json'}

        new_post_data = {
            "title": "Test Post",
            "body": "This is a test post.",
            "userId": 1
        }
        response = requests.post(url, data=json.dumps(new_post_data), headers=headers)
        print(response)
        self.assertEqual(response.status_code, 201,
                         f"Hata! POST isteği başarısız. Status code: {response.status_code}")

        created_post_id = response.json().get("id", None)
        self.assertIsNotNone(created_post_id, "Hata! Oluşturulan öğenin id'si alınamadı.")

        self.created_post_id = created_post_id

    def test_6_delete_request(self):

        if hasattr(self, "created_post_id"):
            url = f"https://jsonplaceholder.typicode.com/posts/{self.created_post_id}"
            response = requests.delete(url)
            self.assertEqual(response.status_code, 204,
                             f"Hata! DELETE isteği başarısız. Status code: {response.status_code}")


if __name__ == '__main__':
    unittest.main(testRunner=HTMLTestRunner(output='test_reports'))
