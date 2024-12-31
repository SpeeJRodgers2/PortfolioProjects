# Employee Turnover Analysis
### Description: The goal of this project is to use exploratory data analysis, visualizations, and statistical modeling methods to determine what factors are playing a role in employee turnover at a company. 

First, it's important to get to know the data that you've been given. I used the pandas library to import the data into a jupyter notebook to work with. The head(), info(), and describe() methods were all useful to see a few rows of the data, check the data types of each column, and get some descriptive statistics. 

Next, I wanted to clean the data. I renamed each column to make them correctly spelled, named, and snake_case'd. The duplicated() method was used to check for duplicates in the data. The duplicates found were then removed because a full row of data being the same for an employee across 10 columns of data is extremely unlikely. There were no missing values in the dataset, so we don't have to worry about that.

With the data clean, it's time to do some exploratory data analysis or EDA using visualtions. First, I wanted to know if we could see a relationship between employees leaving and the number of projects they're working.

insert plot

The boxplot above and on the left shows the percentiles of average monthly hours worked for employees that stayed or left grouped by the number of projects they worked on. The Histogram on the right simply shows the number of employees that stayed or left grouped by the number of projects they worked on. We get some similar information from both plots, but there is even more information given by the boxplot. Both plots show us that every employee working on 7 projects left the company! (This was double checked using pandas to look specifically at that catgeory of employees.) The boxplot tells us something extra though. We see that the median average monthly hours worked is higher for employees that left in each group of projects worked besides those that worked only 2. This is a trend that we can investigate further.

Now, we can look at a scatterplot of employees that stayed or left based on their satisfaction level and average monthly hours worked. Before making the plot, I calculated what could be considered a typical average number of hours worked per month might be. Since a typical job gets about 2 weeks off in a year and works 40 hours in a week, the typical worker will average about 166.67 hours per month. ((50 weeks * 40 hours) / 12 months = 166.67 hours per month)

insert plot

We can see three very distinctive groups of employees that left the company in the scatterplot. The three groups are: employees that worked about 240 to 315 hours on average per month with a very low satisfaction level (basically 0), employees that worked a little less than our calculated normal average hours per month (166.67 hours per month) with somewhat low satisfacton, and employees that worked about 210 to 280 hours on average per month with a good satisfaction level. These groups are so distinctive that I would guess this is artificial data, but this is still good enough data to make a project out of. This scatterplot also shows that most employees work more than what we categorized as the typical amount of hours per month. The two groups of employees that worked a siginifcant amount of hours more than what's typical and left likly left due to being overworked. The group that left and worked under the typical amount of hours per month could have been fired for not working enough or left because they want to work more hours to support their income.

Here's another scatterplot but using an employees last evaluation score vs. their average monthly hours worked.

insert plot

Here, we see two clear groupings of employees that left the company. The first is a group with a high evaluation score that worked about 220 hours to 310 hours on average per month. The high evaluation score of these employees suggests that they probably chose to leave the company fdue to being overworked. The second group has a low evaluation score and worked about 125 to 160 hours on average per month. The low evaluation score leads me to believe that these employees from the second group may have been let go for not working enough hours. We see that most employees are working more than the typical 166.67 hours per month that we calcualted. This suggests something within the culture of this company. 

Let's see if employees are rewarded for working more hours with a promotion.

insert plot

We see in this chart that not many employees get a promotion, and hours worked does not seem to be correlated with being promoted.

Next, we look at employee satisfaction and employee turnover related to how long someone is with the company, tenure. 

insert plot

The first thing I notice looking at these plots is that no one at the company has left once they reached their 7th year with te company. The boxplot shows that employees that leave satisfaction levels drop each year before bottoming out in year 4. This makes sense because unsatisfied employees will leave early and not continue working for a company they don't enjoy being with. The employees with high satisfaction that leave in years 5 and 6 with the company are likely hired at another company and given a prmotion. 

We can check if employees that stay longer stay because they are getting a higher salary.

insert plot

We see here that longer tenured employees aren't disproportionatley comprised of higher-paid salaries.



First, I checked the percentage of employees that stayed vs. left since this is dependent statistic that we'll be modeling to predict. We see that about 83% of employees stayed while about 17% left. Next
