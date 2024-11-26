# Step 0: Import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Step 1: Generate Vertical Data (Columnar Format)
# Example dataset: Features representing customer attributes (Age, Income, Spending Score)
vertical_data = {
    "Age": [25, 34, 45, 23, 35, 40, 29, 60, 55, 18],
    "Income": [40000, 60000, 80000, 30000, 70000, 75000, 50000, 100000, 95000, 20000],
    "Spending_Score": [65, 70, 55, 75, 60, 50, 68, 30, 35, 80]
}
df = pd.DataFrame(vertical_data)

# Step 2: Preprocess Data
# Standardize the data for efficient clustering
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df)

# Step 3: Apply K-Means Clustering
# Choose the number of clusters
num_clusters = 3
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
clusters = kmeans.fit_predict(scaled_data)

# Add cluster labels to the dataset
df['Cluster'] = clusters

# Step 4: Visualize Clusters
# For visualization, we'll plot only two dimensions: Age vs Spending Score
plt.figure(figsize=(10, 6))
for cluster_id in range(num_clusters):
    cluster_points = df[df['Cluster'] == cluster_id]
    plt.scatter(cluster_points['Age'], cluster_points['Spending_Score'], label=f"Cluster {cluster_id}")

# Plot centroids
centroids = scaler.inverse_transform(kmeans.cluster_centers_)
plt.scatter(centroids[:, 0], centroids[:, 2], s=200, c='red', marker='X', label='Centroids')

plt.title('Pattern Recognition: Clustering on Vertical Data')
plt.xlabel('Age')
plt.ylabel('Spending Score')
plt.legend()
plt.grid()
plt.show()

# Step 5: Print Cluster Assignments
print("Cluster Assignments:")
print(df)
