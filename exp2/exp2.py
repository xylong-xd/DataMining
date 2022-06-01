# coding=gbk
import pandas as pd
import matplotlib.pyplot as plt  # 加载matplotlib用于数据的可视化
from sklearn.decomposition import PCA  # 加载PCA算法包
import numpy as np
import matplotlib.pylab as pyl

klein_rds = pd.read_csv(r"klein.rds", sep='\t')
xin_rds = pd.read_csv(r"xin.rds", sep='\t')
romanov_rds = pd.read_csv(r"romanov.rds", sep='\t')
zeisel_rds = pd.read_csv(r"zeisel.rds", sep='\t')
lake_rds = pd.read_csv(r"lake.rds", sep='\t')
# print(klein_rds)
np_klein = klein_rds.values
np_xin = xin_rds.values
np_romanov = romanov_rds.values
np_zeisel = zeisel_rds.values
np_lake = lake_rds.values
# print(np_klein.T)
pca = PCA(n_components=2)  # 加载PCA算法，设置降维后主成分数目为2
reduced_np_klein = pca.fit_transform(np_klein.T)  # 对样本进行降维
reduced_np_xin = pca.fit_transform(np_xin.T)  # 对样本进行降维
reduced_np_romanov = pca.fit_transform(np_romanov.T)  # 对样本进行降维
reduced_np_zeisel = pca.fit_transform(np_zeisel.T)  # 对样本进行降维
reduced_np_lake = pca.fit_transform(np_lake.T)  # 对样本进行降维
# print(reduced_np_klein)
x1 = reduced_np_klein.T[0]
y1 = reduced_np_klein.T[1]
print(x1, y1)
pyl.plot(x1, y1, '.')
x2 = reduced_np_xin.T[0]
y2 = reduced_np_xin.T[1]
print(x2, y2)
pyl.plot(x2, y2, '.')
x3 = reduced_np_romanov.T[0]
y3 = reduced_np_romanov.T[1]
pyl.plot(x3, y3, '.')
x4 = reduced_np_zeisel.T[0]
y4 = reduced_np_zeisel.T[1]
pyl.plot(x4, y4, '.')
x5 = reduced_np_lake.T[0]
y5 = reduced_np_lake.T[1]
pyl.plot(x5, y5, '.')
from sklearn.cluster import KMeans

########klein
y_pred = KMeans(n_clusters=4, random_state=9).fit_predict(reduced_np_klein)
plt.scatter(reduced_np_klein[:, 0], reduced_np_klein[:, 1], c=y_pred)
plt.show()
# print(y_pred)
from sklearn import metrics

labels_true = pd.read_csv(r"klein.rds_label", sep='\t')
np.labels_true = labels_true.values
np.labels_true = np.labels_true.reshape(-1)
# print(np.labels_true)
for i in range(len(np.labels_true)):
    np.labels_true[i] = np.labels_true[i].replace("d", "")
# print(np.labels_true)
np.labels_true = list(map(int, np.labels_true))
# print(np.labels_true)
n = metrics.adjusted_rand_score(np.labels_true, y_pred) / metrics.normalized_mutual_info_score(np.labels_true, y_pred)
print(n)
#######xin
y1_pred = KMeans(n_clusters=8, random_state=9).fit_predict(reduced_np_xin)
plt.scatter(reduced_np_xin[:, 0], reduced_np_xin[:, 1], c=y1_pred)
plt.show()
print(y1_pred)

from sklearn import metrics

labels1_true = pd.read_csv(r"xin.rds_label", sep='\t')
np.labels1_true = labels1_true.values
np.labels1_true = np.labels1_true.reshape(-1)

np.labels1_true = np.labels1_true.astype(np.int16)
print(np.labels1_true)
n1 = metrics.adjusted_rand_score(np.labels1_true, y1_pred) / metrics.normalized_mutual_info_score(np.labels1_true,
                                                                                                  y1_pred)
print(n1)
#######zeisel
y2_pred = KMeans(n_clusters=9, random_state=9).fit_predict(reduced_np_zeisel)
plt.scatter(reduced_np_zeisel[:, 0], reduced_np_zeisel[:, 1], c=y2_pred)
plt.show()
# print(y2_pred)

from sklearn import metrics

labels3_true = pd.read_csv(r"zeisel.rds_label", sep='\t')
print(labels3_true)

np.labels3_true = labels3_true.values
np.labels3_true = np.labels3_true.reshape(-1)
print(np.labels3_true)

n2 = metrics.adjusted_rand_score(np.labels3_true, y2_pred) / metrics.normalized_mutual_info_score(np.labels3_true,
                                                                                                  y2_pred)
print(n2)
#######zeisel
y2_pred = KMeans(n_clusters=16, random_state=9).fit_predict(reduced_np_lake)
plt.scatter(reduced_np_lake[:, 0], reduced_np_lake[:, 1], c=y2_pred)
plt.show()
# print(y2_pred)

from sklearn import metrics

labels3_true = pd.read_csv(r"zeisel.rds_label", sep='\t')
print(labels3_true)

np.labels3_true = labels3_true.values
np.labels3_true = np.labels3_true.reshape(-1)
print(np.labels3_true)

n2 = metrics.adjusted_rand_score(np.labels3_true, y2_pred) / metrics.normalized_mutual_info_score(np.labels3_true,
                                                                                                  y2_pred)
print(n2)
#######zeisel
y2_pred = KMeans(n_clusters=9, random_state=9).fit_predict(reduced_np_romanov)
plt.scatter(reduced_np_romanov[:, 0], reduced_np_romanov[:, 1], c=y2_pred)
plt.show()
# print(y2_pred)

from sklearn import metrics

labels3_true = pd.read_csv(r"zeisel.rds_label", sep='\t')
print(labels3_true)

np.labels3_true = labels3_true.values
np.labels3_true = np.labels3_true.reshape(-1)
print(np.labels3_true)

n2 = metrics.adjusted_rand_score(np.labels3_true, y2_pred) / metrics.normalized_mutual_info_score(np.labels3_true,
                                                                                                  y2_pred)
print(n2)
