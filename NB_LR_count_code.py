#I count the codes to build the vector
#the result is nearly the same as using tfidf
import numpy as np
from sklearn import linear_model
from sklearn.naive_bayes import MultinomialNB

prob=0.05
times=1
nb=[]
lr=[]
for i in range(times):
    feature_names={}
    training=[]
    testing=[]
    label_test=[]
    y_test=[]
    label=[]
    y=[]
    sample=0
    sample_test=0
    n=0
    code=[]
    code_test=[]

    f=open('data.txt','rb')
    for line in f:
        key=line.split(',,,')[0]
        variation=line.split(',,,')[1]
        variation=float(variation.split(':')[0])
        p=np.random.random()
        if p>prob:
            sample+=1
            y.append(variation)
            if variation>0:
                label.append(1)
            else:
                label.append(0)
            code.append(line.split(':')[2].strip().split(' '))
            words=line.split(':')[2].strip().split(' ')
            for word in words:
                if cmp(word,'')!=0:
                    if not feature_names.has_key(word):
                        feature_names.update( {word:n} )
                        n+=1
        else:
            sample_test+=1
            y_test.append(variation)
            if variation>0:
                label_test.append(1)
            else:
                label_test.append(0)
            code_test.append(line.split(':')[2].strip().split(' '))

    print "number of features: "+str(n)

    print "number of sample: "+str(sample)
    vector=np.zeros((sample, n))
    for i in range(sample):
        for word in code[i]:
            if cmp(word,'')!=0:
                index=feature_names[word]
                vector[i][index]+=1
    classifier = MultinomialNB()
    classifier.fit(vector,label)

    coef=[]
    for nn,i in enumerate(classifier.coef_):
        coef.append( [i,nn] )
    coef=sorted(coef,reverse=True)[0:5]
    print "the 5 most important features"
    for i in coef:
        for key in feature_names.keys():
            if feature_names[key]==i[1]:
                print key




#    print vector[0]

    vector_test=np.zeros((sample_test,n))
    for i in range(sample_test):
        for word in code_test[i]:
            if feature_names.has_key(word):
                index=feature_names[word]
                vector_test[i][index]+=1
#    print classifier.score(vector_test,label_test)
    nb.append(classifier.score(vector_test,label_test))
    clf = linear_model.LogisticRegression()
    clf.fit(vector,label)
#    print clf.score(vector_test,label_test)
    lr.append(clf.score(vector_test,label_test))
nb=np.array(nb)
lr=np.array(lr)
print "The accuracy of NB: "+str(np.mean(nb))
print "The accuracy of Logistic Regression: "+str(np.mean(lr))