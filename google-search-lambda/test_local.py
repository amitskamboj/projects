import logging
import json
from lambda_function import lambda_handler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


class MockContext:
    function_name = "google-search-lambda"
    aws_request_id = "local-test-001"


if __name__ == "__main__":
    event = {"query": "Python AWS Lambda tutorial"}
    result = lambda_handler(event, MockContext())
    print("\nLambda result:", json.dumps(result, indent=2))
