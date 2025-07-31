import pytest
import requests
import json

@pytest.mark.api
@pytest.mark.users
class TestCreateUser:
    
    @pytest.fixture
    def create_user_url(self, base_url):
        """Create user endpoint URL"""
        return base_url  # Same as base_url since it's POST /users
    
    @pytest.fixture
    def valid_user_payload(self):
        """Valid user creation data"""
        return {
            "name": "morpheus",
            "job": "leader"
        }
    
    def test_create_user_success(self, create_user_url, common_headers, valid_user_payload):
        """Test successful user creation"""
        response = requests.post(create_user_url, json=valid_user_payload, headers=common_headers)
        
        assert response.status_code == 201  # Created
        data = response.json()
        
        # Validate response contains input data
        assert data["name"] == valid_user_payload["name"]
        assert data["job"] == valid_user_payload["job"]
        
        # Validate response contains generated fields
        assert "id" in data
        assert "createdAt" in data
        assert data["id"] is not None
        assert data["createdAt"] is not None
    
    @pytest.mark.parametrize("name,job", [
        ("john", "developer"),
        ("jane", "designer"),
        ("test_user", "tester"),
        ("admin", "administrator")
    ])
    def test_create_user_different_data(self, create_user_url, common_headers, name, job):
        """Test creating users with different valid data"""
        payload = {"name": name, "job": job}
        response = requests.post(create_user_url, json=payload, headers=common_headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == name
        assert data["job"] == job
        assert "id" in data
        assert "createdAt" in data
    
    def test_create_user_missing_name(self, create_user_url, common_headers):
        """Test creating user without name field"""
        payload = {"job": "leader"}
        response = requests.post(create_user_url, json=payload, headers=common_headers)
        
        # reqres.in allows creation without name
        assert response.status_code == 201
        data = response.json()
        assert data["job"] == "leader"
        assert "id" in data
        assert "createdAt" in data
    
    def test_create_user_missing_job(self, create_user_url, common_headers):
        """Test creating user without job field"""
        payload = {"name": "morpheus"}
        response = requests.post(create_user_url, json=payload, headers=common_headers)
        
        # reqres.in allows creation without job
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "morpheus"
        assert "id" in data
        assert "createdAt" in data
    
    def test_create_user_empty_payload(self, create_user_url, common_headers):
        """Test creating user with empty payload"""
        payload = {}
        response = requests.post(create_user_url, json=payload, headers=common_headers)
        
        # reqres.in allows empty creation
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert "createdAt" in data
    
    @pytest.mark.parametrize("name,job", [
        ("", "leader"),           # Empty name
        ("morpheus", ""),         # Empty job
        ("a" * 1000, "leader"),   # Very long name
        ("morpheus", "a" * 1000), # Very long job
    ])
    def test_create_user_edge_cases(self, create_user_url, common_headers, name, job):
        """Test creating users with edge case data"""
        payload = {"name": name, "job": job}
        response = requests.post(create_user_url, json=payload, headers=common_headers)
        
        # reqres.in is lenient with validation
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == name
        assert data["job"] == job
    
    def test_create_user_invalid_content_type(self, create_user_url, valid_user_payload):
        """Test creating user with wrong content type"""
        headers = {"Content-Type": "text/plain"}
        response = requests.post(create_user_url, data=json.dumps(valid_user_payload), headers=headers)
        
        # Test that API rejects or handles invalid content type
        assert response.status_code in [400, 415, 201, 401]  # Bad Request, Unsupported Media Type, or Created
    
    def test_create_user_response_time(self, create_user_url, common_headers, valid_user_payload):
        """Test create user response time"""
        import time
        
        start_time = time.time()
        response = requests.post(create_user_url, json=valid_user_payload, headers=common_headers)
        end_time = time.time()
        
        assert response.status_code == 201
        assert (end_time - start_time) < 5  # Should respond within 5 seconds