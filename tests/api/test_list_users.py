import pytest
import requests
import time

# Fixture for base URL
# Fixtures are reusable functions that provide data/setup for tests
# This fixture returns the base API endpoint URL
@pytest.fixture
def base_url():
    return "https://reqres.in/api/users"

# Fixture for common headers
# This fixture provides HTTP headers that will be used across multiple tests
# Fixtures help avoid code duplication and provide consistent setup
@pytest.fixture
def common_headers():
    return {
        "Accept": "application/json",  # Tell server we want JSON response
        "User-Agent": "pytest-api-test/1.0",  # Identify our test client
        "x-api-key": "reqres-free-v1"  # API key (though reqres.in doesn't actually require this)
    }


# Test class - groups related tests together
# @pytest.mark decorators are used to categorize tests for filtering
@pytest.mark.api  # Mark as API test - can run with: pytest -m api
@pytest.mark.smoke  # Mark as smoke test - can run with: pytest -m smoke
class TestListUsers:

    # Parametrized test - runs the same test with different input values
    # Creates 2 separate test cases: one for page 1, one for page 2
    @pytest.mark.parametrize("page,expected_page", [
        (1, 1),  # Test case 1: request page 1, expect page 1 in response
        (2, 2)   # Test case 2: request page 2, expect page 2 in response
    ])
    def test_list_users_by_page(self, base_url, common_headers, page, expected_page):
        """Test fetching users from different pages"""
        # Parameters for the GET request
        params = {"page": page}
        
        # Make GET request using fixtures and parameters
        response = requests.get(base_url, params=params, headers=common_headers)

        # Assert successful response
        assert response.status_code == 200
        
        # Parse JSON response
        data = response.json()

        # Validate response structure - ensure all required fields exist
        assert "page" in data
        assert "data" in data
        assert "total" in data
        assert "total_pages" in data

        # Validate page number matches what we requested
        assert data["page"] == expected_page

        # Validate data is a list (array of users)
        assert isinstance(data["data"], list)

    # Another parametrized test with different scenarios
    # Tests data presence for valid pages vs invalid pages
    @pytest.mark.parametrize("page,should_have_data", [
        (1, True),    # Page 1 should have data
        (2, True),    # Page 2 should have data
        (999, False)  # Page 999 (non-existent) should have empty data
    ])
    def test_users_data_presence(self, base_url, common_headers, page, should_have_data):
        """Test data presence for different pages"""
        params = {"page": page}
        response = requests.get(base_url, params=params, headers=common_headers)

        # API returns 200 even for non-existent pages (with empty data)
        assert response.status_code == 200
        data = response.json()

        # Check if data array has content based on expectation
        if should_have_data:
            assert len(data["data"]) > 0  # Should have user data
        else:
            assert len(data["data"]) == 0  # Should be empty for non-existent pages

    # Performance test - marked as slow and integration test
    @pytest.mark.slow  # Mark as slow test - can exclude with: pytest -m "not slow"
    @pytest.mark.integration  # Mark as integration test
    def test_response_time(self, base_url, common_headers):
        """Test API response time"""
        # Measure response time
        start_time = time.time()
        response = requests.get(base_url, params={"page": 1}, headers=common_headers)
        end_time = time.time()

        # Verify successful response
        assert response.status_code == 200
        
        # Verify response time is acceptable (less than 5 seconds)
        assert (end_time - start_time) < 5  # Performance assertion

    # Error handling test - tests API behavior with invalid endpoints
    @pytest.mark.error_handling  # Mark as error handling test
    def test_invalid_endpoint(self, base_url, common_headers):
        """Test handling of invalid endpoint"""
        # Create invalid URL by appending "/invalid"
        invalid_url = base_url + "/invalid"
        
        # Make request to invalid endpoint
        response = requests.get(invalid_url, headers=common_headers)

        # Should return 404 Not Found for invalid endpoints
        assert response.status_code == 404
