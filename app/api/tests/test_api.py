import unittest
from fastapi.testclient import TestClient

from app.main import app


class APITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"message": "Containerized Help Desk Platform API is running"},
        )

    def test_create_ticket_rejects_invalid_priority(self):
        response = self.client.post(
            "/tickets",
            json={
                "employee_name": "Awais",
                "issue": "Laptop cannot connect to network",
                "priority": "Invalid",
            },
        )
        self.assertEqual(response.status_code, 422)

    def test_status_update_rejects_invalid_status(self):
        response = self.client.patch(
            "/tickets/1/status",
            json={"status": "Invalid"},
        )
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
