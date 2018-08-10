dir <- getwd()
setwd(dir)


library(tm)
library(caTools)
# install.packages("anytime", dependencies=TRUE, repos = "https://cran.rstudio.com/")
library(anytime)
# install.packages("lubridate", dependencies=TRUE, repos = "https://cran.rstudio.com/")
library(lubridate)

library(ROCR)
library(rpart)
library(rpart.plot)
library(caret)


input_file = "Appliances_1.csv"

allData = read.csv(input_file, stringsAsFactors=FALSE)


#clean the data 
corpus <- Corpus(VectorSource(allData$reviewText))
corpus <- tm_map(corpus, tolower)
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, removeWords, stopwords("english"))

temp <- tm_map(corpus, stemDocument, language="english")
dtm <- DocumentTermMatrix(temp)

# shows the document term matrix numbers
# dtm 

# make a sparse dtm, ie. use only words that appear in 10% of reviews or more
spdtm <- removeSparseTerms(dtm, 0.90)
# inspect(spdtm)

dataSparse = as.data.frame(as.matrix(spdtm))

numberData = read.csv(input_file)

#create a dataFrame with just the regression vectors

time = anytime(numberData$unixReview)
year = year(time)
sortedSalesRank = sort(numberData$salesRank_Num)
topTenPercent = as.integer(length(sortedSalesRank)/4)
topTenPercentCutoff = sortedSalesRank[topTenPercent]
best_seller = as.numeric(numberData$salesRank_Num < topTenPercentCutoff)
# summary(best_seller)

dataWhole = data.frame(salesRank=best_seller, price=numberData$price, overall=numberData$overall, year)
regressionData = na.omit(dataWhole)

# summary(regressionData)
library(caTools)
set.seed(123)
split = sample.split(regressionData$salesRank, SplitRatio = 0.7)
train = subset(regressionData, split==TRUE)
test  = subset(regressionData, split==FALSE)

#model 1 is the linear regression model
model1 = lm(salesRank ~ ., data=train)
summary(model1)

training_results = predict(model1)
# length(training_results)
# length(train$salesRank)
test_results = predict(model1, newdata=test)


"regular lin. reg. training accuracy"
training_matrix = table(train$salesRank, training_results >= 0.5)
training_matrix
accuracy = sum(diag(training_matrix))/sum(training_matrix)
accuracy

"regular lin. reg. test accuracy"
test_matrix = table(test$salesRank, test_results >= 0.5)
test_matrix
accuracy = sum(diag(test_matrix))/sum(test_matrix)
accuracy

#model 2 is the logistic regression model
model2 = glm(salesRank ~ ., family="binomial", data=train)
summary(model2)


training_results = predict(model2, type="response")
test_results = predict(model2, test, type="response")


"regular log. reg. training accuracy"
training_matrix = table(train$salesRank, training_results >= 0.5)
training_matrix
accuracy = sum(diag(training_matrix))/sum(training_matrix)
accuracy

"regular log. reg. test accuracy"
test_matrix = table(test$salesRank, test_results >= 0.5)
test_matrix
accuracy = sum(diag(test_matrix))/sum(test_matrix)
accuracy

#model 3 is the tree model
model3 = rpart(salesRank ~ ., data=train)

prp(model3)

training_results = predict(model3)
test_results = predict(model3, newdata=test)

"regular tree model training accuracy"
training_matrix = table(train$salesRank, training_results >= 0.5)
training_matrix
accuracy = sum(diag(training_matrix))/sum(training_matrix)
accuracy

"regular tree model test accuracy"
test_matrix = table(test$salesRank, test_results >= 0.5)
test_matrix
accuracy = sum(diag(test_matrix))/sum(test_matrix)
accuracy



# # put the bag of words columns in the regression data
arrayLength = length(numberData$SalesRank)
words = colnames(numberData)


regressionData <- cbind(dataWhole,dataSparse)
regressionData = na.omit(regressionData)
# summary(regressionData)

# lin reg
library(caTools)
set.seed(123)
split = sample.split(regressionData$salesRank, SplitRatio = 0.7)
train = subset(regressionData, split==TRUE)
test  = subset(regressionData, split==FALSE)

model1_complex = lm(salesRank ~ ., data=train)
model1 = step(model1_complex)
summary(model1_complex)
summary(model1)

training_results = predict(model1)
test_results = predict(model1, newdata=test)

"bag of words + lin. reg. training accuracy"
training_matrix = table(train$salesRank, training_results >= 0.5)
training_matrix
accuracy = sum(diag(training_matrix))/sum(training_matrix)
accuracy


"bag of words + lin. reg. test accuracy"
test_matrix = table(test$salesRank, test_results >= 0.5)
test_matrix
accuracy = sum(diag(test_matrix))/sum(test_matrix)
accuracy


#model 2 is the logistic regression model
model2_complex = glm(salesRank ~ ., family="binomial", data=train)
model2 = step(model2_complex)
summary(model2_complex)
summary(model2)

training_results = predict(model2, type="response")
test_results = predict(model2, test, type="response")


"bag of words + log. reg. training accuracy"
training_matrix = table(train$salesRank, training_results >= 0.5)
training_matrix
accuracy = sum(diag(training_matrix))/sum(training_matrix)
accuracy

"bag of words + log. reg. test accuracy"
test_matrix = table(test$salesRank, test_results >= 0.5)
test_matrix
accuracy = sum(diag(test_matrix))/sum(test_matrix)
accuracy

#model 3 is the tree model
model3 = rpart(salesRank ~ ., data=train)

prp(model3)

training_results = predict(model3)
test_results = predict(model3, newdata=test)

"bag of words + tree model training accuracy"
training_matrix = table(train$salesRank, training_results >= 0.5)
training_matrix
accuracy = sum(diag(training_matrix))/sum(training_matrix)
accuracy

"bag of words + tree model test accuracy"
test_matrix = table(test$salesRank, test_results >= 0.5)
test_matrix
accuracy = sum(diag(test_matrix))/sum(test_matrix)
accuracy

# # table(data_Auto$)


# ### whether or not you are on best seller's list
# # top 100 







