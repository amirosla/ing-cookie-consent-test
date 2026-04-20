import pytest


# Realistic desktop Chrome user-agent avoids bot-detection (Imperva/Incapsula)
_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Override context args to appear as a real Polish desktop user."""
    return {
        **browser_context_args,
        "locale": "pl-PL",
        "timezone_id": "Europe/Warsaw",
        "geolocation": {"latitude": 52.2297, "longitude": 21.0122},
        "permissions": ["geolocation"],
        "user_agent": _USER_AGENT,
        "extra_http_headers": {"Accept-Language": "pl-PL,pl;q=0.9,en;q=0.8"},
        "viewport": {"width": 1280, "height": 800},
    }
