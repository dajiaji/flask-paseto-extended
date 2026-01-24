"""Pytest configuration and custom markers for flask-paseto-extended tests."""



def pytest_configure(config):
    """Register custom markers for test categorization."""
    config.addinivalue_line("markers", "issuer: PasetoIssuer related tests")
    config.addinivalue_line("markers", "verifier: PasetoVerifier related tests")
    config.addinivalue_line("markers", "cookie_session: PasetoCookieSessionInterface related tests")
    config.addinivalue_line("markers", "login_manager: PasetoLoginManager related tests")
    config.addinivalue_line("markers", "integration: Integration tests")
