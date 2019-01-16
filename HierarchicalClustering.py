
from scipy.cluster.hierarchy import dendrogram, linkage,fcluster
from matplotlib import pyplot as plt
X = [[i] for i in [2, 8, 0, 4, 1, 9, 9, 0]]
# X = [[1,2],[3,2],[4,4],[1,2],[1,3]]
print(X)
Z = linkage(X, 'ward')
print(Z)
f = fcluster(Z,4,'distance')
fig = plt.figure(figsize=(5, 3))
dn = dendrogram(Z)
plt.show()