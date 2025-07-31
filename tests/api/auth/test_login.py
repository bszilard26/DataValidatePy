import pytest
import requests

@pytest.mark.api
@pytest.mark.auth
class TestLogin:
    
    @pytest.fixture
    def login_url(self, base_url):
        """Login endpoint URL"""
        return base_url.replace("/users", "/login")
    
    @pytest.fixture
    def valid_login_payload(self):
        """Valid login credentials"""
        return {
            "email": "eve.holt@reqres.in",
            "password": "cityslicka"
        }
    
    def test_successful_login(self, login_url, common_headers, valid_login_payload):
        """Test successful login with valid credentials"""
        response = requests.post(login_url, json=valid_login_payload, headers=common_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert data["token"] is not None
    
    @pytest.mark.parametrize("email,password,expected_status", [
        ("eve.holt@reqres.in", "wrong_password", 400),
        ("invalid@email.com", "cityslicka", 400),
        ("", "cityslicka", 400),
        ("eve.holt@reqres.in", "", 400),
    ])
    def test_login_with_invalid_credentials(self, login_url, common_headers, email, password, expected_status):
        """Test login with various invalid credentials"""
        payload = {"email": email, "password": password}
        response = requests.post(login_url, json=payload, headers=common_headers)
        
        assert response.status_code == expected_status
    
    def test_login_missing_password(self, login_url, common_headers):
        """Test login with missing password field"""
        payload = {"email": "eve.holt@reqres.in"}
        response = requests.post(login_url, json=payload, headers=common_headers)
        
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
    
    def test_login_missing_email(self, login_url, common_headers):
        """Test login with missing email field"""
        payload = {"password": "cityslicka"}
        response = requests.post(login_url, json=payload, headers=common_headers)
        
        assert response.status_code == 400
        data = response.json()
        assert "error" in data