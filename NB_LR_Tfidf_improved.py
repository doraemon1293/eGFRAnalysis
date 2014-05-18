# split data set into training and testing set randomly
# and try every threshold to get the highest accuracy

from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import linear_model
import numpy as np
import string
prob=0.05
threshold=0.01
regression_mean=[]
nb_mean=[]
best_regression_mean=0
best_nb_mean=0
times=10
while threshold<0.4:
    regression=[]
    nb=[]
    for t in range(times):
        f=open('data_1.txt','rb')
        d={}
        code=[]
        code_test=[]
        label_test=[]
        y_test=[]
        label=[]
        y=[]
        n=0
        for line in f:
            key,variation=line.split(',,,')
            variation=float(variation.split(':')[0])
            p=np.random.random()
            if p>prob:
                code.append(line.split(':')[2].strip().replace('/',''))
                d.update( {key:n} )
                y.append(variation)
                if variation>0:
                    label.append(1)
                else:
                    label.append(0)
                n+=1
            else:
                code_test.append(line.split(':')[2].strip().replace('/',''))
                y_test.append(variation)
                if variation>0:
                    label_test.append(1)
                else:
                    label_test.append(0)
                n+=1

        tfidf = TfidfVectorizer(sublinear_tf=True,stop_words=None,ngram_range=(1,1),token_pattern=ur'\b\w+\b',lowercase=False)
        training_feature_matrix =tfidf.fit_transform(code)
        testing_feature_matrix =tfidf.transform(code_test)

        #print training_feature_matrix1

        classifier = MultinomialNB()
        classifier.fit(training_feature_matrix,label)

        f.close()
#        print 'NB'
#        print classifier.score(training_feature_matrix,label)
#        print classifier.score(testing_feature_matrix,label_test)

        #logistic regression
        X=training_feature_matrix
        label=np.array(label)
        clf = linear_model.LogisticRegression()
        clf.fit(X,label)
        coefficient= clf.coef_[0]
 #       print 'logistic regression'
 #       print clf.score(X,label)
 #       print clf.score(testing_feature_matrix,label_test)


        #build new code
        feature_names=tfidf.get_feature_names()
        vocal={}
        for i in range(len(feature_names)):
            vocal.update( {feature_names[i]:coefficient[i]} )
        new_code=[]
        for s in code:
            words=s.split(' ')
            temp_str=''
            for word in words:
                try:
                    if abs(vocal[word])>=threshold:
                        temp_str+=word+' '
                except:
                    temp_str+=word+' '
                    continue
            temp_str=temp_str.strip()
            new_code.append(temp_str)
        tfidf = TfidfVectorizer(sublinear_tf=True,stop_words=None,ngram_range=(1,1),token_pattern=ur'\b\w+\b',lowercase=False)
#        tfidf = CountVectorizer(ngram_range=(1,1),token_pattern=ur'\b\w+\b',lowercase=False)
        training_feature_matrix =tfidf.fit_transform(new_code)
        classifier = MultinomialNB()
        classifier.fit(training_feature_matrix,label)
        testing_feature_matrix =tfidf.transform(code_test)
#        print 'NB'
#        print classifier.score(training_feature_matrix,label)
#        print classifier.score(testing_feature_matrix,label_test)
        nb.append(classifier.score(testing_feature_matrix,label_test))

        X=training_feature_matrix
        clf = linear_model.LogisticRegression()
        clf.fit(X,label)
#        print 'logistic regression'
#        print clf.score(X,label)
#        print clf.score(testing_feature_matrix,label_test)
        regression.append( clf.score(testing_feature_matrix,label_test) )
#    print nb
    nb=np.array(nb)
    print np.mean(nb)
#    print regression
    regression=np.array(regression)
    print np.mean(regression)
    regression_mean.append(np.mean(regression))
    nb_mean.append(np.mean(nb))
    if best_regression_mean<np.mean(regression):
        best_regression_mean=np.mean(regression)
        best_regression_threshold=threshold
    if best_nb_mean<np.mean(nb):
        best_nb_mean=np.mean(nb)
        best_nb_threshold=threshold
    threshold+=0.01
    print threshold
print "The best accurcy for NB: "+str(best_nb_mean)
print "The threshold: "+str(best_nb_threshold)
print "The best accurcy for Logistic Regression: "+str(best_regression_mean)
print "The threshold: "+str(best_regression_threshold)