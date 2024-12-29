# Employee Turnover Analysis
### Description: The goal of this project is to use exploratory data analysis, visualizations, and statistical modeling methods to determine what factors are playing a role in employee turnover at a company. 

First, it's important to get to know the data that you've been given. I used the pandas library to import the data into a jupyter notebook to work with. The head(), info(), and describe() methods were all useful to see a few rows of the data, check the data types of each column, and get some descriptive statistics. 

Next, I wanted to clean the data. I renamed each column to make them correctly spelled, named, and snake_case'd. The duplicated() method was used to check for duplicates in the data. The duplicates found were then removed because a full row of data being the same for an employee across 10 columns of data is extremely unlikely. There were no missing values in the dataset, so we don't have to worry about that.

With the data clean, it's time to do some exploratory data analysis or EDA using visualtions. First, I wanted to know if we could see a relationship between employees leaving and the number of projects they're working.

insert plot

The boxplot above and on the left shows the percentiles of average monthly hours worked for employees that stayed or left grouped by the number of projects they worked on. The Histogram on the right simply shows the number of employees that stayed or left grouped by the number of projects they worked on. We get some similar information from both plots, but there is even more information given by the boxplot. Both plots show us that every employee working on 7 projects left the company! (This was double checked using pandas to look specifically at that catgeory of employees.) The boxplot tells us something extra though. We see that the median average monthly hours worked is higher for employees that left in each group of projects worked besides those that worked only 2. This is a trend that we can investigate further.

Now, we can look at a scatterplot of employees that stayed or left based on their satisfaction level and average monthly hours worked.

insert plot



First, I checked the percentage of employees that stayed vs. left since this is dependent statistic that we'll be modeling to predict. We see that about 83% of employees stayed while about 17% left. Next
