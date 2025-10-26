from fredapi import Fred
import pandas as pd

fred = Fred(api_key='YOUR-API-KEY')

series = {
    '10Y': 'DGS10',
    '2Y': 'DGS2',
    'CPI': 'CPIAUCSL',
    'FedFunds': 'FEDFUNDS',
    'VIX': 'VIXCLS',
    'USD_Index': 'DTWEXBGS',
    # 'Debt_to_GDP': 'GFDEGDQ188S',
    'Oil': 'DCOILWTICO',
    'InflExp': 'T5YIE'
}

data = pd.DataFrame({name: fred.get_series(code) for name, code in series.items()})
data = data.resample('M').last()
data['CPI_YoY'] = data['CPI'].pct_change(12) * 100
data['Slope'] = data['10Y'] - data['2Y']
data['Δ10Y'] = data['10Y'].diff()


gdp_q = fred.get_series("GDPC1").to_frame("GDP_Real_SAAR")
gdp_q.index = gdp_q.index.to_period("Q").to_timestamp("Q")
start_date = "2015-12-01"
end_date   = "2025-10-31"
gdp_q = gdp_q.loc[start_date:end_date]
gdp_m = gdp_q.resample("M").ffill()
gdp_m = gdp_m.loc[start_date:end_date]
extra_data = pd.DataFrame({
    "GDP_Real_SAAR": [23770.976, 23770.976, 23770.976]
}, index=pd.to_datetime(["2025-08-31", "2025-09-30", "2025-10-31"]))
gdp_m = pd.concat([gdp_m, extra_data])



federal_debt_q = fred.get_series("GFDEBTN").to_frame("Federal_Debt_Billions")
federal_debt_q.index = federal_debt_q.index.to_period("Q").to_timestamp("Q")
start_date = "2015-12-01"
end_date   = "2025-10-31"
federal_debt_q = federal_debt_q.loc[start_date:end_date]
federal_debt_m = federal_debt_q.resample("M").ffill()
federal_debt_m = federal_debt_m.loc[start_date:end_date]
extra_data = pd.DataFrame({
    "Federal_Debt_Billions": [36211469.0, 36211469.0, 36211469.0]
}, index=pd.to_datetime([ "2025-08-31", "2025-09-30", "2025-10-31"]))
federal_debt_m = pd.concat([federal_debt_m, extra_data])



df1 = data.iloc[len(data) - 118:].merge(gdp_m[1:], left_index=True, right_index=True, how='outer')
df1
df = df1.merge(federal_debt_m[1:], left_index=True, right_index=True, how='outer')
df['Debt_To_GDP'] = df['Federal_Debt_Billions'] / df['GDP_Real_SAAR']
df['Δ10Y'] = df['10Y'].diff()
df.to_csv('data.csv')