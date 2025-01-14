import numpy as np
from sklearn.cluster import KMeans

def cluster(line_data):
    #Seperate the vertical (green) and horizontal (red) lines based on theta
    vertical_lines = []
    for line in line_data:
        if abs(line['theta'] - np.pi/2) < 0.1:
            vertical_lines.append(line)

    horizontal_lines = []
    for line in line_data:
        if abs(line['theta']) < 0.1 or abs(line['theta'] - np.pi) < 0.1:
            horizontal_lines.append(line)

    
    #Extract rho values for vertical lines to distuinguish left and right poles 
    vertical_rhos = []
    for line in vertical_lines:
        vertical_rhos.append(line['rho'])
    vertical_rhos = np.array(vertical_rhos)

    #Reshape vertical_rhos to be a 2D array
    vertical_rhos = vertical_rhos.reshape(-1, 1)

    #Use KMeans clustering to seperate vertical lines into two clusters (left and right pole)
    if len(vertical_rhos) >= 2:
        kmeans = KMeans(n_clusters=2, random_state=0).fit(vertical_rhos)
        labels = kmeans.labels_

        left_pole_lines = []
        right_pole_lines = []
        for i in range(len(labels)):
            if labels[i] == np.argmin(kmeans.cluster_centers_):
                left_pole_lines.append(vertical_lines[i])

            if labels[i] == np.argmax(kmeans.cluster_centers_):
                right_pole_lines.append(vertical_lines[i])
    
    else:
        raise ValueError("Not enough vertical lines to perform clustering!!!")
    
    #For horizontal lines, take the average rho and theta to represent the top pole
    if len(horizontal_lines) > 0:
        avg_rho = np.mean([line["rho"] for line in horizontal_lines])
        avg_theta = np.mean([line["theta"] for line in horizontal_lines])
        top_pole_line = {"rho": avg_rho, "theta": avg_theta}
    else:
        raise ValueError("Not enough horizontal lines found for top pole")
    
    #Return the clustered lines
    return {
        "left_pole": left_pole_lines,
        "right_pole": right_pole_lines,
        "top_pole": top_pole_line
    }