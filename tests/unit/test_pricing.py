import pytest

from app.pricing import UnknownProductError, calculate_total, price_for_quantity

SILVER = {"unit_price": 100, "offer": {"quantity": 3, "price": 200}}
GOLD = {"unit_price": 80, "offer": {"quantity": 2, "price": 120}}
PLATINUM = {"unit_price": 50, "offer": None}


@pytest.mark.parametrize(
    ("quantity", "expected"),
    [(0, 0), (1, 100), (2, 200), (3, 200), (4, 300), (6, 400), (7, 500)],
)
def test_silver_label_bundle_pricing(quantity, expected):
    assert price_for_quantity(quantity, SILVER) == expected


@pytest.mark.parametrize(
    ("quantity", "expected"),
    [(0, 0), (1, 80), (2, 120), (3, 200), (4, 240), (5, 320)],
)
def test_gold_label_bundle_pricing(quantity, expected):
    assert price_for_quantity(quantity, GOLD) == expected


@pytest.mark.parametrize("quantity", [0, 1, 2, 3, 10])
def test_product_without_offer_charges_unit_price(quantity):
    assert price_for_quantity(quantity, PLATINUM) == quantity * 50


def test_empty_basket():
    assert calculate_total([]) == 0


def test_single_item():
    assert calculate_total(["004"]) == 50


def test_example_from_brief():
    assert calculate_total(["001", "002", "001", "004", "003"]) == 380


def test_mixed_basket():
    # 6x Silver = 400, 5x Gold = 320, 1x Platinum = 50
    assert calculate_total(["001"] * 6 + ["002"] * 5 + ["003"]) == 770


def test_unknown_product_id_raises():
    with pytest.raises(UnknownProductError):
        calculate_total(["001", "999"])
