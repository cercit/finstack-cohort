"""Run: python -I -m pytest test_resale_value.py   (or: python test_resale_value.py)"""
from datetime import date

from resale_value import age_in_years, cc_band, estimate, oem_from_name

TODAY = date(2026, 10, 12)


def test_oem_names():
    assert oem_from_name("MARUTI SUZUKI INDIA LTD") == "maruti"
    assert oem_from_name("TOYOTA KIRLOSKAR MOTOR PVT LTD") == "toyota"
    assert oem_from_name("MAHINDRA & MAHINDRA LIMITED") == "mahindra"
    assert oem_from_name("FORD INDIA PVT LTD") is None


def test_cc_band_edges():
    assert [cc_band(x) for x in ("998", 1000, 1001, 1300, 1301, 1600, 1601, 2000, 2001)] == [0, 0, 1, 1, 2, 2, 3, 3, 4]


def test_age():
    assert age_in_years("2-2018", TODAY) == 8
    assert age_in_years("11-2016", TODAY) == 9      # 9 years 11 months
    assert age_in_years("10-2026", TODAY) == 0


def test_known_value():
    r = estimate("MARUTI SUZUKI INDIA LTD", "998", "2-2018", TODAY)
    assert r["value"] == 161000 and r["low"] < r["value"] < r["high"]


def test_not_valued():
    assert estimate("MARUTI SUZUKI INDIA LTD", "998", "2-2012", TODAY)["value"] is None   # 14 years
    assert estimate("FORD INDIA PVT LTD", "1498", "1-2020", TODAY)["value"] is None
    assert estimate("TATA MOTORS LIMITED", "1199", "1-2030", TODAY)["value"] is None


def test_value_falls_with_age():
    values = [estimate("HYUNDAI MOTOR INDIA LTD", "1197", f"6-{2026 - y}", TODAY)["value"] for y in range(0, 10)]
    assert values == sorted(values, reverse=True)


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("PASS", name)
