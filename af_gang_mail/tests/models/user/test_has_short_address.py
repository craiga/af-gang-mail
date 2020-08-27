"""User has_short_address tests."""

# pylint: disable=too-many-arguments

import pytest
from model_bakery import baker


@pytest.mark.parametrize(
    "line1, line2, city, state, postcode, country",
    [
        ("", "", "", "", "", ""),
        ("1049 Gotho Road", "", "", "", "", ""),
        ("", "", "", "", "BS4 4AR", ""),
        ("1049 Gotho Road", "", "", "", "BS4 4AR", ""),
        ("", "", "", "", "BS4 4AR", "GB"),
    ],
)
def test_short_address(line1, line2, city, state, postcode, country):
    """Test has_short_address."""

    user = baker.prepare(
        "af_gang_mail.User",
        address_line_1=line1,
        address_line_2=line2,
        address_city=city,
        address_state=state,
        address_postcode=postcode,
        address_country=country,
    )
    assert user.has_short_address()


@pytest.mark.parametrize(
    "line1, line2, city, state, postcode, country",
    [("1049 Gotho Road", "", "Bristol", "", "", "GB")],
)
def test_long_address(line1, line2, city, state, postcode, country):
    """Test has_short_address with long address."""

    user = baker.prepare(
        "af_gang_mail.User",
        address_line_1=line1,
        address_line_2=line2,
        address_city=city,
        address_state=state,
        address_postcode=postcode,
        address_country=country,
    )
    assert not user.has_short_address()
