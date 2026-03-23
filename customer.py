import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
#  Load data
df = pd.read_csv("Mall_Customers.csv")
#  Select numeric features for clustering
numeric_features = df[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']]
#  Handle missing values
numeric_features = numeric_features.fillna(numeric_features.mean())
#  Scale features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(numeric_features)
#  Try K-Means for k=2..10
inertia = []
silhouette = []

for k in range(2, 11):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(scaled_features)
    inertia.append(kmeans.inertia_)
    silhouette.append(silhouette_score(scaled_features, labels))
#  Plot Elbow + Silhouette
plt.figure(figsize=(12,5))
plt.subplot(1,2,1)
plt.plot(range(2,11), inertia, marker='o')
plt.title("Elbow Method")
plt.xlabel("Number of clusters")
plt.ylabel("Inertia")
plt.subplot(1,2,2)
plt.plot(range(2,11), silhouette, marker='o')
plt.title("Silhouette Scores")
plt.xlabel("Number of clusters")
plt.ylabel("Silhouette Score")
plt.show(block=True)
#  Best k based on silhouette score
best_k = 2 + silhouette.index(max(silhouette))
print("Best k based on silhouette score:", best_k)
#  Apply KMeans with best k
kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(scaled_features)
#  Print cluster summary table ONLY for numeric columns
numeric_cols = ['Age', 'Annual Income (k$)', 'Spending Score (1-100)']
print("\nCluster Summary:\n")
print(df.groupby('Cluster')[numeric_cols].mean())
#  Scatter plot to visualize clusters
plt.figure(figsize=(8,6))
plt.scatter(df['Annual Income (k$)'], df['Spending Score (1-100)'], 
            c=df['Cluster'], cmap='rainbow', s=50)
plt.xlabel('Annual Income (k$)')
plt.ylabel('Spending Score (1-100)')
plt.title('Customer Segments')
plt.show(block=True)