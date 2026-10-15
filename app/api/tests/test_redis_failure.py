import unittest
from unittest.mock import Mock, patch

from fastapi.testclient import TestClient
from redis.exceptions import RedisError
from app.main import app

client = TestClient(app)
ROW = (1, "Awais", "Example issue", "High", "Open", "2026-10-15 12:00:00")


class RedisFailureTests(unittest.TestCase):
    def test_committed_writes_survive_invalidation_failure(self):
        for method, path, payload, expected in (
            ("post", "/tickets", {
                "employee_name": "Awais",
                "issue": "Example issue",
                "priority": "High",
            }, 201),
            ("patch", "/tickets/1/status", {"status": "Closed"}, 200),
        ):
            with self.subTest(method=method):
                db = Mock()
                db.cursor.return_value.fetchone.return_value = ROW
                cache = Mock()
                cache.scan_iter.side_effect = RedisError("offline")
                with patch("app.main.get_database_connection", return_value=db), \
                     patch("app.main.get_redis_connection", return_value=cache):
                    response = getattr(client, method)(path, json=payload)
                self.assertEqual(response.status_code, expected, response.text)
                db.commit.assert_called_once()

    def test_reads_survive_cache_get_and_set_failures(self):
        db = Mock()
        db.cursor.return_value.fetchall.return_value = [ROW]
        cache = Mock()
        cache.get.side_effect = RedisError("offline")
        cache.setex.side_effect = RedisError("offline")
        with patch("app.main.get_database_connection", return_value=db), \
             patch("app.main.get_redis_connection", return_value=cache):
            response = client.get("/tickets")
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["source"], "postgresql")
        self.assertEqual(response.json()["tickets"][0]["id"], 1)


if __name__ == "__main__":
    unittest.main()
