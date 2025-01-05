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

Now, let's check if any specific departments have more employee turnover than others.

insert plot

Nothing really stands out in this plot.

After using visualizations to get familiar with the data, it's time to make some models to predict the target variable, employees staying or leaving. First, I checked the percentage of employees that stayed vs. left because that's the dependent statistic that we'll be trying to predict. We see that about 83% of employees stayed while about 17% left. This split is lopsided, but it's still acceptable. I tried a logistic regression classification model first, so some columns of data needed to be encoded for the model to work. The salary column, containing low, medium, and high, was encoded using the .set_categories() method. This way the natural order of the salary column is kept. This column is an ordinal categorical column meaning the order of these categories has intrinsic value. The rest of the categorical columns could be encoded using the .get_dummies method because they aren't ordinal categorical columns, their order doesn't have instrinsic value. Now, I want to check the correlation of the other independent data columns with eachother. This is to make sure the "no multicollinearity assumption" is met. Here is the correlation heat map I made using seaborn below.

insert heatmap

None of these indepednent columns break the assumption by being too highly correlated. Now let's remove outliers to account for the model's "no extreme outliers assumption". Using boxplots to look at each column of independent data, we see that the tenure column is the only one with outliers (shown below).

insert box plot

The upper and lower limits we'll use to seperate he outliers in the tenure column from the data we'll keep are calculated. First, we need to get the IQR or interquartile range by subtracting the 25th percentile of the tenure column from the 75th percentile. Then we get the upper limit by adding the 75th percentile with 1.5 times the IQR. Similarly, we get the lower limit by subtracting 1.5 times the IQR from the 25th percentile. We use the upper and lower limits to pull the rows of data inbewteen those values to use for the model. 

Now the last bit of data prep before putting it into the model is splitting the data into training and testing sets. This way we can test the model on data it did not see in training. Finally, I trained and tested the model. Below is a confusion matrix showing the results.

insert confusion matrix

Here, we can see that the model has a problem with false negatives. This is very important because that means that the model is struggling to correctly predict employees that are leaving, which is the goal of this process. The recall, or the proportion of employees the model predicts would leave that actually left, was a measly 24%. This model is not useful at all, so let's try some other mo0dels.

We'll try a decision tree classifier model now. This model has no assumptions regarding data distribution and handles collinearity very easily. The only thing to look out for is its succeptibility to overfitting. We will use GridSearchCV to optimize the model's perameters during training. The parameters that were optimized were max_depth (max depth of the tree), min_samples_leaf (minimum number of samples required to be leaf node), and min_samples_split (minimum number of samples to split a node). After training and testing the model, we see that it performs MUCH better than the logistic regression model. We got precision of 95.5%, recall of 91.5%, F1 score of 93.4%, accuracy of 97.9%, and an AUC score of 97.4%. These are all inidcators of a strong model. 

Since decision trees are succeptible to overfitting, let's try a random forest model as-well. These models do not have a problem with overfitting because of their ensemble learning approach. This means that they use many different decision trees in their prediction, so no one decision tree can overly influence the results and cause overfitiing of the training data. GridSearchCV was used here as-well for th parameter tuning. Some of the parameters being tuned are the same ones from a decision tree like max_depth, min_samples_leaf, and min_samples_split. The new parameters specific to the random forest model that we tuned are max_features (number of features considered to determine the best split), max_samples (number of samples drawn from the data to train each tree), and n_estimators (the number of trees being trained). After training and testing the model, we got a precision of 96.7%, recall of 93.4%, F1 score of 95.0%, accuracy of 98.4%, and AUC score of 96.4%. Since recall is the most important model evaluation metric for our use case, the random forest model wins out. It scores higher in every metric besides AUC score and it's more resistant to overfitting. This all leads to it being the model to choose.

In these preliminary tests, data leakage was ignored. Data leakage is using data to train a model that you might not have during deployment of the model. To fix this, I'm going to perform some feature engineering to get new columns of data to train the model on and remove any columns with data leakage. First, the satisfaction_level column is going to be removed since we may not have this information before an employee decides to leave. There's also a chance we don't have enough of a sample to use the average_monthly_hours data column, so let's do some data engineering before dropping this one to prevent data leakage. I already calculated that the typical number of hours an employee works per month is about 167 hours, so we'll say that 175 hours per month means an employee is "overworked". I copied the average_monthly_hours column into a new column called overworked, and then did a true false statement on the column where it's 1 if the value is greater than 175 and 0 if it's not. Now that we have this overworked column, we can drop the average_monthly_hours columnto take away data leakage and still have a column that can be predictive from the data we had to work with.

Using this newly engineered data with reduced leakage, we trained another decision tree and random forest model using the same parameters that were used previously. Both the decision tree and random forest model's performed worse than before the data engineering and dropping of potential data leaking columns. This makes some sense since both of those columns, satisfaction_level was an extremely predictive statistic. We see this below by charting the feature importances of the best estimating models by using the .best_estimator_ and .feature_importances_ methods.

insert decision tree 1 feature importances

insert random forest 1 feature importances

Regardless, it's better to know how the model's will perform during deployment rather than deploying them and being surprised by the difference in results! The decision tree's scores were: precision - 85.7%, recall - 90.4%, F1 score - 87.9%, accuracy - 95.9%, and AUC score - 95.9%. The random forest model's scores were: precision 86.7%, recall - 87.9%, F1 score - 87.2%, accuracy - 95.7%, and AUC score - 96.5%. Let's look at the random forest model's confusion matrix to visualize how strong of a model it is.

insert confusion matrix

This is a huge improvement compared to the first logistic regression model that we started with that had 487 total incorrect predictions. This model only has 115 incorrect predictions. This model does have more false negatives than false postives though. This is useful to keep in mind since that means it's predicting more employees being at risk of leaving or being let go than is actually true. 

Now let's look at the most important features of these new models. 

insert featue importance charts for the second models

We see that our feature engineered overworked column is actually slightly more predictive than the average_monthly_hours column was!

Through this process, we were able to determine what factors drove employee turnover. Figuring out what drives the problem is half the battle. Now, the company can determine ways of fixing the issue! I would suggest a few things to help employee retention: cap the number of pojects an employee can work on, increase overtime benefits and make sure employees are aware how employees that work more hours are benefitted, limit or reduce the number of hours and employee works, and have a company wide meeting to address the current work culture.  
