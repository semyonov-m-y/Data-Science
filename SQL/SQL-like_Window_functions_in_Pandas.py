import datetime
import random
import ffn
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

tickers = [
    "AAPL",  # apple
    "DIS",  # disney
    "NKE",  # nike
    "TSLA",  # tesla
]

# get stock price data
prices = ffn.get(tickers, start="2018-01-01")

# convert data into 'long' table format for purposes of this exercise
prices = prices.melt(ignore_index=False, var_name="ticker", value_name="closing_price")

# reset index to make 'Date' a column
prices = prices.reset_index()

# display 5 example rows in the dataset
prices.sample(5).sort_index()

# create connection to in memory sqlite db
with sqlite3.connect(":memory:") as conn:

    # save prices dataframe to sqlite db
    prices.to_sql(name="prices", con=conn, index=False)

print('Example 1: Calculating the maximum stock price for each company in the time period')
ex1_sql_query = """
SELECT
    date(Date) as Date
    , ticker
    , closing_price
    , MAX(closing_price) OVER(PARTITION BY ticker) as max_price
FROM
    prices
LIMIT 100
"""

# use pandas read_sql to execute the query and return a dataframe
ex1_sql = pd.read_sql(ex1_sql_query, con=conn)
print(ex1_sql)

# copy dataframe to avoid overwritting original (optional)
ex1_pandas = prices.copy()

# add new column
ex1_pandas["max_price"] = ex1_pandas.groupby("ticker")["closing_price"].transform("max")

print(ex1_pandas)

print('Example 2: 28 day closing price moving average for each company')
ex2_sql_query = """
SELECT
    date(Date) AS Date
    , ticker
    , closing_price
    , AVG(closing_price) OVER(
        PARTITION BY ticker
        ORDER BY date(Date)
        ROWS BETWEEN 27 PRECEDING AND CURRENT ROW
    )
     AS ma_28_day
FROM
    prices
LIMIT 100
"""

ex2_sql = pd.read_sql(ex2_sql_query, con=conn)
print(ex2_sql)

# copy original dataframe (optional)
ex2_pandas = prices.copy()

# add new column
ex2_pandas["ma_28_day"] = (
    ex2_pandas.sort_values("Date")
    .groupby("ticker")["closing_price"]
    .transform(lambda x: x.rolling(28, min_periods=1).mean())
)

print(ex2_pandas)

print('Example 3: Get previous day’s closing share price for each ticker')
ex3_sql_query = """
SELECT
    date(Date) AS Date
    , ticker
    , closing_price
    , LAG(closing_price, 1) OVER(
        PARTITION BY ticker
        ORDER BY date(Date)
    ) AS previous_close
FROM
    prices
LIMIT 100
"""

ex3_sql = pd.read_sql(ex3_sql_query, con=conn)
print(ex3_sql)

ex3_pandas = prices.copy()

ex3_pandas["previous_close"] = (
    ex3_pandas.sort_values("Date").groupby("ticker")["closing_price"].shift(1)
)

print(ex3_pandas)

print('Example 4: Daily Percentage Return')
ex4_sql_query = """
SELECT
    Date
    , ticker
    , closing_price
    , closing_price/previous_close - 1 AS daily_return
FROM
    (
    SELECT
         date(Date) AS Date
        , ticker
        , closing_price
        , LAG(closing_price,1) OVER(
            PARTITION BY ticker ORDER BY date(Date)
        ) AS previous_close
    FROM
        prices
)
"""

ex4_sql = pd.read_sql(ex4_sql_query, con=conn)
print(ex4_sql)

ex4_pandas = prices.copy()

ex4_pandas["daily_return"] = (
    ex4_pandas.sort_values("Date")
    .groupby("ticker")["closing_price"]
    .transform(lambda x: x / x.shift(1) - 1)
)

print(ex4_pandas)

print('Example 5: Missing Data Interpolation')
# copy orginal dataframe
ex5_pandas = prices.copy()

# remove 30% of data randomly
pct_missing = 0.3
num_missing = int(pct_missing * len(ex5_pandas))
indexes = random.sample(range(len(ex5_pandas)), k=num_missing)
mask = [i in indexes for i in range(len(ex5_pandas))]

# mask the dataframe with some random NaNs
ex5_pandas["closing_price"] = ex5_pandas["closing_price"].mask(mask)

# interpolate missing data paritioned by ticker
ex5_pandas["closing_price_interpolated"] = (
    ex5_pandas.sort_values("Date")
    .groupby("ticker")["closing_price"]
    .transform(lambda x: x.interpolate(method="ffill"))
)

print(ex5_pandas)

# verify there is no missing data in the new column
ex5_pandas.isnull().sum()



