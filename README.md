eGFRAnalysis
============

a data mining model in Python based on Naive Bayesian filter and Logistic Regression to predict eGFR's trend according to the patient's medical log to check how well the patient’s kidneys are working.

mysqltest.py: get the raw data, which contains only the patient's ID, start date and groundtruth
get_the_code.py: get the code according to the raw data to build the sample data
NB_LR_count_code.py: Count code to vectorise and use NB and Logistic Regression(LR) model
NB_LG_TFidf.py: Use TfIdf to vectorise and use NB and LR model
NB_LR_Tfidf_improved.py: Use TfIdf to vectorise and use NB and LR model, delete the code whose coefficient in LR model are lower than the threshold. (different from useing NB's coefficients in our presentation, because LR's are better) Get the optimised threshold with the best mean accuracy.
data.txt: the whold prepared data
data_1.txt: a small subset of the whole prepared data
