# PopMov-covid19
A linear regression model based on population flow and imported cases is used to evaluate the effect of COVID-19 lockdown policies and predict future risks.
## code

```
Spider_BaiduQianxi.py
Baiduqianxi big data released spider scripts of regional migration data during the 2020 Spring Festival travel rush

correlation.py
Correlation analysis to evaluate the relationship between population movement and confirmed cases.

lockdown_mov_pop.py
A comparison of population migration in Wuhan during the Spring Festival in 2019 and the Spring Festival in 2020.

map_additinal_cases_nontravelban.py
Heat map of additional cases for cities in China, caused by cancelling Wuhan’s travel ban on 23 January 2020.

map_protect_3day.py
Protection rate heat map for cities in China based on a three-day-earlier lockdown of Wuhan. 

map_work_resumption_current_scenario.py
Evaluation of the risk of population reflux due to work resumption. 
Get risk heat map for cities with positive population net influx based on current population movement data between Feb 7 and 14, 2020.

model_mcmc.py
We assumed that the observed case counts followed a Poisson distribution and that the expected case counts were linearly proportional to the population movement volume.
Then We build a linear regression model to compute the maximum likelihood estimate (MLE) of the regression coefficient 𝛽 and other effects 𝛾 through a Markov chain Monte Carlo (MCMC) analysis.

mcmc_interval.py
We generated a bootstrapped dataset by sampling 200 cities with replacement (half from the cities with more cases and half from the cities with fewer cases). Second, we reestimated 𝛽 and 𝛾 using the bootstrapped dataset. Third, we simulated case counts for all cities using re-estimated 𝛽 and 𝛾. These three steps were repeated 1000 times to generate 1000 simulated case counts from which the lower and upper PI bounds (2×5th and 97×5th percentiles) are computed.
```
## data
```
Citycode and Population data for each city
Citycode.csv

Case data
case_city_20200101-20200214.csv

Qianxi Data
20190112-20190301-qianxi_index.csv
qianxi_20200101-20200214_in.csv
qianxi_20200101-20200214_out.csv

geographical coordinates of each nodes
city_coordinates.csv

Model input data
model_input_data.csv

shipfile to draw the map
gadm36_CHN_shp
```
## results
```
Protection or risk data under different travel ban policies
additional_cases_no_travelban.csv
three-day-earlier_travelban.csv
seven-day-earlier_travelban.csv

risk of work resumption 
reflux_risk_current.csv
reflux_risk_travelban_for_Hubei.csv
reflux_risk_without_travelban.csv

Model parameters
bootstrap_para_100
```
## figures
```
paper
figures in paper

example 
The figures drawn by the code in the code folder
```
## packages
```
Basemap package
```



