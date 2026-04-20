import pytest


@pytest.fixture()
def context(browser):
    ctx = browser.new_context(
        locale="pl-PL",
        timezone_id="Europe/Warsaw",
        geolocation={"latitude": 52.2297, "longitude": 21.0122},
        permissions=["geolocation"],
        extra_http_headers={"Accept-Language": "pl-PL,pl;q=0.9"},
    )
    yield ctx
    ctx.close()
