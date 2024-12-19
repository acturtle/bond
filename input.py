import pandas as pd
from cashflower import Runplan, ModelPointSet

runplan = Runplan(data=pd.DataFrame({
    "version": [1],
    "valuation_year": [2022],
    "valuation_month": [12],
}))

bond = ModelPointSet(data=pd.DataFrame({
    "nominal": [1000],
    "coupon_rate": [0.03],
    "term": [120],
    "issue_year": [2022],
    "issue_month": [6],
}))

assumption = {
  "INTEREST_RATE": 0.02
}
