# Presenting Ames House Price Prediction

## Presentation script

### 1. Introduction

I built an application that estimates the historical sale price of a home in Ames, Iowa. A user enters four details and receives an estimate in US dollars. Behind the form is the same regression pipeline I evaluated in my notebook. I chose housing because the question is familiar, but the answer depends on making several careful decisions. Which details would I know before a sale? Which past homes should I learn from? And how far off might my estimate be?

### 2. Problem statement

Imagine two houses with the same living area on the same street. One has better materials and finish. A model based only on size would give them the same estimate. My goal was to learn enough about those differences to beat a simple starting guess. I measured success mainly in dollars of absolute error, because it is easy to explain what a twenty-thousand-dollar miss means. I also wanted to test on later transactions to reflect how someone would actually use historical examples.

### 3. Dataset

I used OpenIntro’s version of the Ames housing data documented by Dean De Cock. It contains 2,930 residential sales and 82 columns. Each row describes a sale. My target is the recorded final price. Living area is measured in square feet, year built records original construction, and neighbourhood is a category. The final model also uses the assessor’s overall quality rating. All examples come from one city between 2006 and 2010. That detail determines what I can reasonably claim about the project.

### 4. Cleaning and preprocessing

I inspected the training records for missing entries, repeated parcels, repeated rows and nonpositive living areas or prices. The three original input fields were complete in the training period. Other columns had many blanks. For instance, missing pool quality could describe a home without a pool. Deleting every row with any blank would remove useful examples. I built a pipeline that learns numeric medians, a categorical fill value and neighbourhood indicators from fitting data. Fitting those steps inside the pipeline keeps the same rules available when the form receives a new house.

### 5. Exploratory analysis

The median training sale price was $161,500. The mean was higher, at about $181,876, and the histogram showed a tail of expensive sales. The correlation between living area and price was about 0.71. I could see the general upward pattern on the scatterplot, but I could also see a wide spread among similarly sized homes. That tells me that size is informative and incomplete. I kept unusual observations because an unexpected price alone does not establish a data-entry error.

### 6. Machine learning approach

My baseline gives every house the median price from its fitting period. It ignores the house details, so it sets a clear benchmark for whether the extra work helps. Linear regression then learns an intercept and weights for the available inputs. One-hot encoding lets the model use neighbourhood without assigning an artificial ranking to neighbourhood names. My first regression used three inputs. My next experiment added overall quality because two houses with similar size and age can still have different materials and finish.

### 7. Training and evaluation

I fitted the candidates on 1,941 sales from 2006 to 2008 and checked their predictions on 648 sales from 2009. The median baseline had a validation MAE of $56,861. The three-feature regression brought that down to $26,372. Adding quality lowered it further to $23,272. I selected the four-feature model at that point and refitted it on all 2,589 development sales. On the 341 reserved sales from 2010, it achieved a mean absolute error of $23,467, an RMSE of $34,379 and an R² of 0.787.

### 8. Challenges and solutions

One challenge was spotting mistakes that average scores could hide. I plotted validation residuals, defining each residual as actual price minus predicted price. Among the top tenth of the original model’s estimates, actual prices exceeded estimates by roughly $12,806 on average. Another challenge was ensuring that the running application used exactly the preprocessing rules I had evaluated. Saving the fitted transformations and regression together solved that problem. I also reloaded the saved artifact and checked its prediction against the in-memory model.

### 9. Demonstration

I launch the local app and leave the example at 1,500 square feet, North Ames, year built 1975 and quality 6. When I click Estimate price, the model returns $176,583. That is a prediction for an illustrative input. I can change one field and compare estimates while keeping the other fields fixed. Then I return to the notebook and show a held-out sale with an actual price of $215,000 and a prediction of about $179,168. That observed miss makes the uncertainty concrete.

### 10. Limitations and future improvements

The test set covers one later period in one city. Quality ratings involve judgement, and changes in the housing market can alter the relationship between features and price. My linear model also treats an extra square foot as having the same effect across a wide range of houses. A future experiment could test nonlinear effects using several chronological validation windows. I would want a fresh holdout for assessing further decisions informed by the published test results.

### 11. Personal learning

The most useful lesson for me was separating model selection from final evaluation. Choosing features is itself a learning decision. If I repeatedly check the final test set while making those choices, I gradually tune the project to the same examples I intend to use as evidence. I also learned why a pipeline matters outside a notebook. It preserves how raw inputs become a prediction when someone runs the project on another computer.

### 12. Closing

I can trace this project from a particular house on the screen back to the fitting records, the validation comparison and the reserved test period. The result is a working local application with a measured error and a defined scope. When someone asks how well it works, I can answer with a year, a sample size, a baseline and a dollar figure.

## 30-second pitch

I built a local house-price estimator from historical sales in Ames, Iowa. I tested whether adding assessor-rated quality improved on a model based on area, neighbourhood and construction year. On 341 later sales, the final model averaged $23,467 in absolute error versus $52,386 for the median baseline. The repository includes the executed notebook, trained pipeline and a working browser form.

## Two-minute interview explanation

I started with a prediction anyone could reproduce: use the median price from older sales for every new house. That gave me a benchmark in dollars. I picked three fields that could reasonably be available before sale and kept the raw target out of the inputs. I then fitted a linear regression that could distinguish houses by size, construction year and neighbourhood. A column transformer kept categorical encoding and numeric preprocessing consistent.

I split by sale year. I fitted on 2006–2008, selected on 2009 and evaluated the final choice on 2010. On the validation sales, the first regression roughly halved the baseline’s absolute error. The residuals still showed substantial variation. Adding the assessor’s quality rating improved validation MAE from $26,372 to $23,272. Only then did I refit the selected model on all sales through 2009.

The final test MAE was $23,467 across 341 sales. The median absolute error was lower, at $16,244, which helped me explain why an average miss differs from a typical individual miss. I packaged the fitted pipeline, included its input ranges and built a local web form around it. My favourite demonstration is to make a prediction and then show an actual held-out error. Together those examples show both the functionality and the uncertainty.

## Five-minute demo

| Time | Demonstration |
|---|---|
| 0:00–1:00 | Open the form, explain the four inputs and run the example. |
| 1:00–2:00 | Open the master notebook and identify one row, the target and the split years. |
| 2:00–3:00 | Compare the baseline, three-input regression and quality experiment using validation MAE. |
| 3:00–4:00 | Explain the sign of a residual and show one actual versus predicted test price. |
| 4:00–5:00 | Return to the app, vary living area and explain why the result applies to historical Ames sales. |

## Ten interview questions and suggested answers

1. **Why split by year?** An estimate for a later sale should depend on earlier transactions. Grouping by year preserves that ordering. A single later period gives limited evidence about stability.
2. **Why use the median baseline?** Among constant guesses, the median minimizes absolute error on the fitting sample. It gives a benchmark in the same units and uses only information available at fitting time.
3. **What does fit learn?** The preprocessing steps learn fill values and neighbourhood categories. Regression learns weights and an intercept from the transformed inputs and the observed prices.
4. **What does predict do?** It applies the already-fitted transformations to new records, then uses the learned weights to compute estimates. New sale prices are unnecessary.
5. **Why one-hot encode neighbourhood?** The labels have no numeric ordering. Indicator columns let regression learn location-related differences without inventing distances between category codes.
6. **Why include quality?** It represents variation in materials and finish. Adding it reduced 2009 MAE by about $3,100 compared with the three-feature model.
7. **What is a positive residual?** I compute actual minus predicted. A positive residual means the sale price exceeded the estimate, so the model underestimated that house.
8. **Why report RMSE as well?** Squaring the errors increases the influence of large misses. Comparing RMSE and MAE shows how much large errors affect the overall result.
9. **How did you prevent leakage?** I excluded the target, fitted transforms within the fitting period and selected features by validation performance. The 2010 price comparisons came after model selection.
10. **Would this work in Waterloo today?** That use would need current local sales, locally meaningful neighbourhoods and a new later-period evaluation. Historical Ames test scores do not quantify accuracy in Waterloo.

## Five technical follow-ups for independent practice

- How would you design rolling-year validation, and how would you aggregate fold results?
- Why can test R² be negative for a training-median baseline?
- What could cause the spread of residuals to increase at high predicted prices?
- How could you test whether quality ratings were consistently available before sale?
- How would you build and evaluate prediction intervals without tuning them on the final holdout?

## Nontechnical explanation

The app learns from older home sales, then estimates what a similar home might have sold for. We checked it against later sales with known prices. An individual estimate can miss by tens of thousands of dollars.

## Résumé bullet options

- Built a local house-price estimation app and a reproducible scikit-learn pipeline using 2,930 historical Ames sales.
- Evaluated a four-feature linear regression on 341 held-out sales, achieving $23,467 MAE versus $52,386 for a median baseline.
- Compared chronological validation performance and reduced MAE from $26,372 to $23,272 by adding assessor-rated quality.

## LinkedIn project description

I built an Ames house-price estimator with Python, pandas and scikit-learn. I compared a median baseline with linear models, used a later year for validation, and packaged the selected pipeline in a local browser app. The public notebook includes exploratory plots, error analysis and results on held-out sales.

## Project completion record

Engineering milestones 1–6 are implemented. Review the split, explain one residual and deliver the five-minute demo before marking presentation practice complete. Personal confidence and independent proficiency are still to be assessed.
