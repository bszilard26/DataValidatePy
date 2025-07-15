import pytest
import requests
import time

# Test class for user listing API endpoints
@pytest.mark.api  # Mark as API test - can run with: pytest -m api
@pytest.mark.smoke  # Mark as smoke test - can run with: pytest -m smoke
class TestListUsers:

    # Test different page numbers return correct page data
    @pytest.mark.parametrize("page,expected_page", [
        (1, 1),
        (2, 2)
    ])
    def test_list_users_by_page(self, base_url, common_headers, page, expected_page):
        """Test fetching users from different pages"""
        params = {"page": page}
        response = requests.get(base_url, params=params, headers=common_headers)

        assert response.status_code == 200
        data = response.json()

        # Validate response structure
        assert "page" in data
        assert "data" in data
        assert "total" in data
        assert "total_pages" in data

        # Validate page number and data type
        assert data["page"] == expected_page
        assert isinstance(data["data"], list)

    # Test data presence for valid vs invalid pages
    @pytest.mark.parametrize("page,should_have_data", [
        (1, True),
        (2, True),
        (999, False)  # Non-existent page
    ])
    def test_users_data_presence(self, base_url, common_headers, page, should_have_data):
        """Test data presence for different pages"""
        params = {"page": page}
        response = requests.get(base_url, params=params, headers=common_headers)

        assert response.status_code == 200
        data = response.json()

        # Check if data array contains users based on page validity
        if should_have_data:
            assert len(data["data"]) > 0
        else:
            assert len(data["data"]) == 0

    # Performance test - measure API response time
    @pytest.mark.slow
    @pytest.mark.integration
    def test_response_time(self, base_url, common_headers):
        """Test API response time"""
        start_time = time.time()
        response = requests.get(base_url, params={"page": 1}, headers=common_headers)
        end_time = time.time()

        assert response.status_code == 200
        assert (end_time - start_time) < 5  # Should respond within 5 seconds

    # Error handling test - verify 404 for invalid endpoints
    @pytest.mark.error_handling
    def test_invalid_endpoint(self, base_url, common_headers):
        """Test handling of invalid endpoint"""
        invalid_url = base_url + "/invalid"
        response = requests.get(invalid_url, headers=common_headers)
        assert response.status_code == 404



