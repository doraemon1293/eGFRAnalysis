# split data set into training and testing set randomly
# and try every threshold to get the highest accuracy

from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import linear_model
import numpy as np
import string
prob=0.05
nb=[]
lr=[]
times=10
for t in range(times):
    regression=[]
    nb=[]
    for t in range(times):
        f=open('data.txt','rb')
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
    #        print n
        tfidf = TfidfVectorizer(sublinear_tf=True,stop_words=None,ngram_range=(1,1),token_pattern=ur'\b\w+\b',lowercase=False)
#        tfidf = CountVectorizer(ngram_range=(1,1),token_pattern=ur'\b\w+\b',lowercase=False)
        training_feature_matrix =tfidf.fit_transform(code)
        #print training_feature_matrix1

        classifier = MultinomialNB()
        classifier.fit(training_feature_matrix,label)
        coef=[]
        for n,i in enumerate(classifier.coef_):
            coef.append( [i,n] )
        coef=sorted(coef,reverse=True)[0:5]
#        for i in coef:
#            print tfidf.get_feature_names()[i[1]]
        f.close()

        testing_feature_matrix =tfidf.transform(code_test)
#        print classifier.score(testing_feature_matrix,label_test)

    #        print 'NB'
    #        print classifier.score(training_feature_matrix,label)
    #        print classifier.score(testing_feature_matrix,label_test)

        #logistic regression
        X=training_feature_matrix
        label=np.array(label)
        clf = linear_model.LogisticRegression()
        clf.fit(X,label)
        coefficient= clf.coef_[0]
        X=testing_feature_matrix
#        print clf.score(X,label_test)
    #       print 'logistic regression'
    #       print clf.score(X,label)
    #       print clf.score(testing_feature_matrix,label_test)
        nb.append(classifier.score(testing_feature_matrix,label_test))
        lr.append(clf.score(X,label_test))
nb=np.array(nb)
lr=np.array(lr)
print "The mean accurcy for NB: "+str(np.mean(nb))
print "The mean accurcy for LR: "+str(np.mean(lr))