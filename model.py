from cashflower import variable

from input import bond, runplan, assumption
from settings import settings


@variable()
def t_end():
    years = bond.get("term") // 12
    months = bond.get("term") - years * 12

    end_year = bond.get("issue_year") + years
    end_month = bond.get("issue_month") + months

    if end_month > 12:
        end_year += 1
        end_month -= 12

    valuation_year = runplan.get("valuation_year")
    valuation_month = runplan.get("valuation_month")
    return (end_year - valuation_year) * 12 + (end_month - valuation_month)


@variable()
def cal_month(t):
    if t == 0:
        return runplan.get("valuation_month")
    if cal_month(t-1) == 12:
        return 1
    else:
        return cal_month(t-1) + 1


@variable()
def cal_year(t):
    if t == 0:
        return runplan.get("valuation_year")
    if cal_month(t-1) == 12:
        return cal_year(t-1) + 1
    else:
        return cal_year(t-1)


@variable()
def coupon(t):
    if t != 0 and t <= t_end() and cal_month(t) == bond.get("issue_month"):
        return bond.get("nominal") * bond.get("coupon_rate")
    else:
        return 0


@variable()
def nominal_value(t):
    if t == t_end():
        return bond.get("nominal")
    else:
        return 0


@variable()
def present_value(t):
    i = assumption["INTEREST_RATE"]
    if t == settings["T_MAX_CALCULATION"]:
        return coupon(t) + nominal_value(t)
    return coupon(t) + nominal_value(t) + present_value(t+1) * (1/(1+i))**(1/12)
