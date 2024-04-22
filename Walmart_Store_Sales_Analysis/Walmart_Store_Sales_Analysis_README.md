# Walmart Store Sales Analysis
#### Description:     In this project, I wanted to see what type of data in the dataset between temperature, fuel price, CPI, & unemployment rate has an affect on weekly sales.

The dataset has weekly sales data across 45 different Walmart stores from many different regions. It also gives the average temperature of that week's sales along with the price of fuel, the consumer price index (CPI), & unemployment rate in that store's region. Lastly, there is a 0 or 1 in a "holiday" column to indicate whether there was a significant holiday that week.

First, I made a pivot table using each store, 1-45, as a row of the pivot table. The columns took averages of weekly sales, temperature, fuel price, CPI, & unemployment. I copy and pasted that data out of the pivot table, so the data can be used in future calculations. I used each stores average data to subtract from it's weekly data to determine whether it was above or below average that week. It's critical that each store's average data was used to find this difference instad of the overall averages since each store is from a different region and should be treated individually to come to accurate conclusions about the overall data. This created 5 new columns of data that can be used to find a correlation between eachother. 

Now, I used the CORREL function to find the correlation between weekly sales above or below average and each of temperature, fuel price, CPI, & unemployment above or below average. This yielded VERY low correlation numbers for each relationship. They all were .1 or lower negative or positive. To put that into perspective a strong correlation is 1 or -1. Something that I believe plays into these correlation numbers being so small is that the difference between the actual and the averages of temperature, fuel price, CPI, & unemployment are MUCH smaller than between weekly sales numbers. Weekly sales numbers could be well over 1 million dollars different while the other data points have double/single digit differences or even less! However, we can still take the correlation number being positive or negative as real data. This indicates whether the numbers have an inverse relationship or not.

![Correlation with Sales](https://github.com/SpeeJRodgers2/PortfolioProjects/blob/main/Walmart_Store_Sales_Analysis/Charts/Correlation_w_%20Sales.png)

In the above chart we can see that temperature, fuel price, & unemployment have a negatively correlated or inverse relationship with sales. This means that sales should go up if any of those data points go down and vice versa. We also see that CPI and sales have a positively correlated relationship, so CPI and sales should move up and down together.

Correlation can be tricky data because totally random data that has nothing to do with eachother can appear to have a relationship, so I want to dig deeper and check these relationships further. To start, I used the COUNTIFS function to count the occurences of each potential relationship. For example, it counted the number of times that weekly sales for a store was above it's average AND temperature was above it's average for that store's region. It also counted the number of occurences (counts) of all the other possible combinations of those statistics being above or below their average. Next, I found the overall count of times that sales were above and below their average. There was actually over 1,000 more occurences of sales being below average than above. That's why we needed those numbers, because the only way to accurately compare the number of times sales are above or below average due to another statistic is by taking the percentage of times it occurs. To find that, I divided the counts of sales above average with X (temperature, fuel price, CPI, or unemployment) above average and then below average by the overall count of times sales were above average. The same thing was done again for sales being below average. This yielded valuable data that will be seen in the charts below. There will also be data with those same percentages with weeks that have significant holidays occuring in them removed. I did this because it's reasonable to assume that consumers will be less price sensitive during holiday weeks, and that could potentially skew the data one way or the other. I will go over the analysis of each relationship under their respective chart.

![Weekly Sales Vs. Temperature Relationships](https://github.com/SpeeJRodgers2/PortfolioProjects/blob/main/Walmart_Store_Sales_Analysis/Charts/Weekly%20Sales%20Vs.%20Temperature%20Relationships.png)

Analysis

![Weekly Sales Vs. Fuel Price Relationships](https://github.com/SpeeJRodgers2/PortfolioProjects/blob/main/Walmart_Store_Sales_Analysis/Charts/Weekly%20Sales%20Vs.%20Fuel%20Price%20Relationships.png)

Analysis

![Weekly Sales Vs. CPI Relationships](https://github.com/SpeeJRodgers2/PortfolioProjects/blob/main/Walmart_Store_Sales_Analysis/Charts/Weekly%20Sales%20Vs.%20CPI%20Relationships.png)

Analysis

![Weekly Sales Vs. Unemployment Relationships](https://github.com/SpeeJRodgers2/PortfolioProjects/blob/main/Walmart_Store_Sales_Analysis/Charts/Weekly%20Sales%20Vs.%20Unemployment%20Relationships.png)

Analysis
