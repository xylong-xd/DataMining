# coding=gbk
from sklearn import metrics
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

iris = load_iris()

X = iris.data
y = iris.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=1)


# ����KNNģ��
knn = KNeighborsClassifier(n_neighbors=1)
# knn = KNeighborsClassifier(n_neighbors=3)

# ѵ��ģ��
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)

# ����ģ��
print("accuracy(in %):", metrics.accuracy_score(y_test, y_pred)*100)