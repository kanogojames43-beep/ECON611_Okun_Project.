# ECON 611 Project Plan

### Research Question

Does Okun's Law still hold in the United States over the Last 20 years?

#### Expected Result

I expect to find a negative relationship between economic growth and unemployment. When economic growth increases, I expect unemployment to decrease.  

### Data Source

I will use economic data from FRED. I will use the FRED series UNRATE for the U.S. unemployment rate. I will use the FRED series GDPC1 for U.S. Real Gross Domestic Product. I will use the Python fredapi package to pull the data from the FRED API. 

I will fetch data starting in January 2004 and ending in December 2024. The 2004 data is only used so I can calculate the changes for 2005 Q1.

### Data Frequency

I will use quarterly data, because GDP is only reported quarterly.

### Cleaning Steps

I will convert the monthly unemployment data to quarterly data by averaging the three months in each quarter.
I will merge the unemployment and GDP data by quarter.
I will calculate GDP growth as the quarter-over-quarter percent change in real GDP: (GDP this quarter / GDP last quarter - 1) x 100. I will not annualize it.
I will calculate the change in the unemployment rate as the unemployment rate this quarter minus the unemployment rate last quarter, in percentage points.
I will keep only 2005 Q1 through 2024 Q4 for the analysis (80 quarters).
I will remove any missing values.

### Charts and Statistical Test

I will create a scatter plot of GDP growth (x-axis) and change in the unemployment rate (y-axis).
I will run a simple OLS regression of the change in the unemployment rate on GDP growth:

change in unemployment = a + b x GDP growth + error

I will report the slope (b), its p-value, and the R-squared.

As a robustness check, I will run the same regression again without 2020 Q2 and 2020 Q3 (the COVID quarters) and compare the slopes.

### What Would Support or Contradict My Expectation

A negative and statistically significant slope (b) would support my expectation. A positive slope, or a slope that is not statistically significant, would contradict my expectation.
