"""Used-car resale estimate from three RC fields: manufacturer name, engine cc, manufacturing month-year.

Single file, no data file needed (uses datetime and re). Not for a FinStack Logic variable: those allow no
libraries, so use resale_expression.txt there. This file is for scripts, tests and the back end.

    from resale_value import estimate
    estimate("MARUTI SUZUKI INDIA LTD", "998", "2-2018")

Value = base[OEM][cc band] x retention[completed years]; the brand factor is already inside base.
Supported: Maruti Suzuki, Hyundai, Tata, Mahindra, Toyota, Kia; ICE and hybrid; cars up to 10 years old.
All numbers are approximate. Not a quote.
"""
import re
from datetime import date

BANDS = ["<=1000", "1001-1300", "1301-1600", "1601-2000", ">2000"]
RETENTION = [0.9, 0.8, 0.7, 0.6, 0.5, 0.44, 0.38, 0.32, 0.26, 0.22, 0.2]   # completed years 0..10
BASE = {
    "maruti": [619300, 843600, 1400500, 2664200, 2664200],
    "hyundai": [1165100, 841100, 1736200, 1736200, 1736200],
    "tata": [807000, 807000, 1453100, 2222700, 2222700],
    "mahindra": [1118200, 1118200, 1095400, 1926400, 1852500],
    "toyota": [1262500, 929600, 1547600, 2906300, 4868600],
    "kia": [1166600, 884900, 1460900, 1460900, 4767000],
}   # Rs, brand factor included; index = cc band
OEM_WORDS = [("MARUTI", "maruti"), ("HYUNDAI", "hyundai"), ("TATA", "tata"),
             ("MAHINDRA", "mahindra"), ("TOYOTA", "toyota"), ("KIA", "kia")]
MAX_AGE_YEARS = 10
BAND_EDGES = [1000, 1300, 1600, 2000]   # <=1000, 1001-1300, 1301-1600, 1601-2000, >2000
RANGE = 0.10                            # dealers quote a band, so show +-10%


def oem_from_name(manufacturer_name):
    """'MARUTI SUZUKI INDIA LTD' -> 'maruti'. Unknown brand -> None."""
    name = (manufacturer_name or "").upper()
    return next((key for word, key in OEM_WORDS if word in name), None)


def cc_band(cc):
    """Index 0-4 of the cc band. Accepts '998', 998 or '998 cc'."""
    value = int(re.sub(r"[^\d.]", "", str(cc)).split(".")[0])
    return sum(value > edge for edge in BAND_EDGES)


def age_in_years(month_year, today=None):
    """'2-2018' (RC format, month-year) -> completed years of age."""
    today = today or date.today()
    month, year = (int(x) for x in re.split(r"[-/]", str(month_year).strip()))
    if not 1 <= month <= 12:
        raise ValueError(f"month out of range: {month_year!r}")
    return ((today.year * 12 + today.month) - (year * 12 + month)) // 12


def estimate(manufacturer_name, cc, month_year, today=None):
    """Return a dict. value is None when the car cannot be valued; reason says why."""
    oem = oem_from_name(manufacturer_name)
    if oem is None:
        return {"value": None, "reason": "brand not supported (Maruti, Hyundai, Tata, Mahindra, Toyota, Kia only)"}
    age = age_in_years(month_year, today)
    if age < 0:
        return {"value": None, "reason": "manufacturing date is in the future"}
    if age > MAX_AGE_YEARS:
        return {"value": None, "reason": f"car is {age} years old; valuation covers {MAX_AGE_YEARS} years only"}
    band = cc_band(cc)
    base = BASE[oem][band]
    value = round(base * RETENTION[age] / 500) * 500
    return {
        "value": value,
        "low": round(value * (1 - RANGE) / 500) * 500,
        "high": round(value * (1 + RANGE) / 500) * 500,
        "oem": oem,
        "cc_band": BANDS[band],
        "age_years": age,
        "base_inr": base,
        "reason": "ok",
    }


if __name__ == "__main__":
    cases = [("MARUTI SUZUKI INDIA LTD", "998", "2-2018"), ("MARUTI SUZUKI INDIA LTD", "998", "2-2012"),
             ("HYUNDAI MOTOR INDIA LTD", "1197", "6-2021"), ("FORD INDIA PVT LTD", "1498", "1-2020")]
    for case in cases:
        print(case, "->", estimate(*case, today=date(2026, 10, 12)))
