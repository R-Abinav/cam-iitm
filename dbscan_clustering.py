import numpy as np
from sklearn.cluster import DBSCAN
from extract_line_data import extractLineData

def clusteringAndMerging(line_data):
    if not line_data:
        print("Error -> Line Data not found/provided")
    
    #Extract Rho, Theta for clustering
    features = []
    for line in line_data:
        features.append([line['rho'], line['theta']])

    features_np = np.array(features)

    #Variables for DBSCAN
    eps = 0.1
    min_samples = 2

    #Perform DBSCAN clustering
    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(features_np)

    #Cluster Labels
    labels = clustering.labels_

    #Group and merge lines by clusters
    merged_lines = []
    unique_labels = set(labels)

    for label in unique_labels:
        #Skipping the noise points
        if label == -1:
            continue

        #Get all lines in the current cluster
        cluster_lines = []
        for i in range(len(labels)):
            if labels[i] == label:
                cluster_lines.append(line_data[i])

        #Computing average rho and theta for the cluster
        rho_values = []
        theta_values = []
        for line in cluster_lines:
            rho_values.append(line['rho'])
            theta_values.append(line['theta'])

        avg_rho = np.mean(rho_values)
        avg_theta = np.mean(theta_values)

        #Recompute slope and intercept for the merged line
        a = np.cos(avg_theta)
        b = np.sin(avg_theta)

        if abs(b) > 1e-6:
            slope = -a/b
            

def main():
    line_data = extractLineData()
    clusteringAndMerging(line_data)

if __name__ == "__main__":
    main()