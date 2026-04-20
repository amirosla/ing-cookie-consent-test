import pytest
from playwright.sync_api import Page, expect


# cookiePolicyGDPR uses a bitmask: 1=technical, 2=analytical, 4=marketing
ANALYTICAL_BIT = 2


def test_ing_analytical_cookie_consent(page: Page) -> None:
    """
    Verifies that:
    1. Cookie customization panel opens on ing.pl
    2. The analytical cookies toggle can be enabled
    3. "Zaakceptuj zaznaczone" saves the selection
    4. cookiePolicyGDPR cookie reflects analytical consent (bit 1 set)
    """
    page.goto("https://www.ing.pl", wait_until="domcontentloaded")

    # --- Step 1: Click "Dostosuj" to open settings panel ---
    dostosuj = page.locator(".js-cookie-policy-main-settings-button")
    expect(dostosuj).to_be_visible(timeout=15_000)
    dostosuj.click()

    # --- Step 2: Enable analytical cookies toggle ---
    # The toggle is a div[role="switch"] with name="CpmAnalyticalOption"
    analytics_toggle = page.locator("[name='CpmAnalyticalOption']")
    expect(analytics_toggle).to_be_visible(timeout=10_000)

    if analytics_toggle.get_attribute("aria-checked") != "true":
        analytics_toggle.click()

    expect(analytics_toggle).to_have_attribute("aria-checked", "true")

    # --- Step 3: Click "Zaakceptuj zaznaczone" ---
    zaakceptuj = page.locator(".js-cookie-policy-settings-decline-button")
    expect(zaakceptuj).to_be_visible(timeout=5_000)
    zaakceptuj.click()

    # Wait for the settings panel to close
    expect(zaakceptuj).to_be_hidden(timeout=10_000)

    # --- Step 4: Verify cookiePolicyGDPR cookie has analytical bit set ---
    cookies = {c["name"]: c["value"] for c in page.context.cookies()}

    assert "cookiePolicyGDPR" in cookies, (
        f"cookiePolicyGDPR cookie not found. Cookies: {list(cookies.keys())}"
    )

    gdpr_value = int(cookies["cookiePolicyGDPR"])
    assert gdpr_value & ANALYTICAL_BIT, (
        f"Analytical consent not set. cookiePolicyGDPR={gdpr_value} "
        f"(expected bit {ANALYTICAL_BIT} to be set)"
    )

    assert "cookiePolicyGDPR__details" in cookies, (
        "cookiePolicyGDPR__details cookie not found"
    )
