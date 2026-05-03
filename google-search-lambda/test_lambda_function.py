import unittest
from unittest.mock import patch, MagicMock
from lambda_function import lambda_handler


class MockContext:
    function_name = "google-search-lambda"
    aws_request_id = "test-001"


class TestLambdaHandler(unittest.TestCase):

    def _make_mock_response(self, status_code=200, content=b"<html>results</html>"):
        mock_response = MagicMock()
        mock_response.status_code = status_code
        mock_response.content = content
        return mock_response

    @patch("lambda_function.requests.get")
    def test_default_query(self, mock_get):
        mock_get.return_value = self._make_mock_response()
        result = lambda_handler({}, MockContext())
        self.assertEqual(result["statusCode"], 200)
        self.assertEqual(result["query"], "AWS Lambda")
        self.assertEqual(result["responseSize"], len(b"<html>results</html>"))

    @patch("lambda_function.requests.get")
    def test_custom_query(self, mock_get):
        content = b"<html>python results</html>"
        mock_get.return_value = self._make_mock_response(content=content)
        result = lambda_handler({"query": "Python tutorial"}, MockContext())
        self.assertEqual(result["query"], "Python tutorial")
        self.assertEqual(result["responseSize"], len(content))

    @patch("lambda_function.requests.get")
    def test_url_encodes_query(self, mock_get):
        mock_get.return_value = self._make_mock_response()
        lambda_handler({"query": "hello world"}, MockContext())
        called_url = mock_get.call_args[0][0]
        self.assertIn("hello%20world", called_url)

    @patch("lambda_function.requests.get")
    def test_returns_correct_status_code(self, mock_get):
        mock_get.return_value = self._make_mock_response(status_code=429)
        result = lambda_handler({"query": "test"}, MockContext())
        self.assertEqual(result["statusCode"], 429)

    @patch("lambda_function.requests.get")
    def test_request_uses_headers(self, mock_get):
        mock_get.return_value = self._make_mock_response()
        lambda_handler({"query": "test"}, MockContext())
        _, kwargs = mock_get.call_args
        self.assertIn("headers", kwargs)
        self.assertIn("User-Agent", kwargs["headers"])

    @patch("lambda_function.requests.get")
    def test_request_has_timeout(self, mock_get):
        mock_get.return_value = self._make_mock_response()
        lambda_handler({"query": "test"}, MockContext())
        _, kwargs = mock_get.call_args
        self.assertEqual(kwargs.get("timeout"), 10)

    @patch("lambda_function.requests.get")
    def test_empty_response_content(self, mock_get):
        mock_get.return_value = self._make_mock_response(content=b"")
        result = lambda_handler({"query": "test"}, MockContext())
        self.assertEqual(result["responseSize"], 0)


if __name__ == "__main__":
    unittest.main()
