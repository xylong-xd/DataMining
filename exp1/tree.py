# coding=gbk
import pandas as pd
import pydotplus
from IPython.core.display import display, Image
from sklearn import metrics, tree
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

data = pd.read_csv("iris_nan.csv", encoding='GB2312')
data.columns = ['sepal_len', 'sepal_width', 'petal_len', 'petal_width', 'class']

# data.info()
# print(data)
print(data.isna().sum())

iris = data.fillna(data.median())  # �ڲ�ȷ���Ƿ�����쳣ֵʱ���˴�ѡ��ʱ����λ���
print(iris.isna().sum())

# �ֳ����ݼ��Ͳ��Լ�


iris_tree = load_iris()

X = iris_tree.data
y = iris_tree.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=1)
# ������
clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)  # ʹ��ѵ����ѵ��ģ��
y_pred = clf.predict(X_test)  # ʹ��ģ�ͶԲ��Լ�����Ԥ��

print("accuracy(in %):", metrics.accuracy_score(y_test, y_pred)*100)

# ���������ӻ�
dot_data = tree.export_graphviz(clf,
                                out_file=None,
                                feature_names=['sepal_len', 'sepal_width', 'petal_len', 'petal_width'],
                                class_names='class',
                                filled=True,
                                rounded=True
                                )
graph = pydotplus.graph_from_dot_data(dot_data)
display(Image(graph.create_png()))
graph.write_png("dtr.png")
