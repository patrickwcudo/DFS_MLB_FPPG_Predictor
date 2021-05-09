#!/usr/bin/env python
# coding: utf-8

# In[1]:


def modeling_reg(X_train, X_test, y_train, y_test, class_list):
    #import pandas
    import pandas as pd
    from sklearn.metrics import mean_squared_error
    # import accuracy score
    #from sklearn.metrics import accuracy_score
    # create lists for scores 
    train_score = []
    test_score = []
    #acc_score = []
    rmse = []
    # for each classifier fit and score
    for classifier in class_list:
        classifier.fit(X_train, y_train)
        train_score.append(classifier.score(X_train, y_train))
        test_score.append(classifier.score(X_test, y_test))
        #acc_score.append(accuracy_score(y_test, classifier.predict(X_test)))
        rmse.append(mean_squared_error(squared=False, y_true=y_test, y_pred=classifier.predict(X_test)))
    # combine into dataframe
    return pd.DataFrame(data=[train_score , test_score, rmse],
                 index=['R2 Score - Train','R2 Score - Test','RMSE'],
                 columns=[str(c) for c in class_list]).T


# In[ ]:
def modeling_class(X_train, X_test, y_train, y_test, class_list):
        #import pandas
    import pandas as pd
    from sklearn.metrics import accuracy_score, f1_score, recall_score
    # create lists for scores 
    train_score = []
    test_score = []
    acc_score = []
    f1_test = []
    f1_train = []
    # for each classifier fit and score
    for classifier in class_list:
        classifier.fit(X_train, y_train)
        train_score.append(classifier.score(X_train, y_train))
        test_score.append(classifier.score(X_test, y_test))
        acc_score.append(accuracy_score(y_test, classifier.predict(X_test)))
        f1_test.append(recall_score(y_test, classifier.predict(X_test)))
        #f1_train.append(f1_score(y_train, classifier.predict(X_train)))
    # combine into dataframe
    return pd.DataFrame(data=[train_score, test_score, acc_score, f1_test],
                 index=['train_score', 'test_score', 'acc_score', 'recall_score'],
                 columns=[str(c) for c in class_list]).T




