from datetime import date, timedelta
import calendar, frappe
from frappe.utils import flt, getdate, date_diff, cint, add_months

# Helper Function
def last_day_of_month(dt):
    last_day = calendar.monthrange(dt.year, dt.month)[1]
    return date(dt.year, dt.month, last_day)

# Get total no. of depreciation for the WDV depreciation method
@frappe.whitelist()
def get_total_no_of_depreciation(
    opening_value,
    rate_of_depreciation,
    available_for_use_date,
    depreciation_start_date,
    frequency,
    daily_prota_based=0,
):
    start_date = getdate(depreciation_start_date)
    available_date = getdate(available_for_use_date)

    rate = flt(rate_of_depreciation) / 100
    current_value = flt(opening_value)
    frequency = cint(frequency)

    data = []
    idx = 1
    previous_schedule_date = None

    while current_value > 1:
        if idx == 1:
            schedule_date = start_date
            no_of_days = date_diff(start_date, available_date) + 1
        else:
            schedule_date = add_months(start_date, idx - 1)
            no_of_days = date_diff(schedule_date, previous_schedule_date)

        depreciation_amount = flt((current_value * rate / (frequency * 365)) * no_of_days)

        current_value -= depreciation_amount

        data.append({
            "idx": idx,
            "schedule_date": schedule_date,
            "no_of_days": no_of_days,
            "opening_value": current_value,
            "dep%": rate,
            "depreciation_amount": depreciation_amount,
            "remaining_value": current_value,
        })

        previous_schedule_date = schedule_date
        idx += 1
        
    return len(data) - 1
