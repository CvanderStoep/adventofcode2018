from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np


def read_input_file(file_name: str) -> list:
    tuples_list = []
    with open(file_name, 'r') as file:
        for line in file:
            # Strip whitespace and split by comma
            numbers = line.strip().split(',')
            # Convert to integers and form a tuple
            tuple_item = tuple(int(num) for num in numbers)
            tuples_list.append(tuple_item)
    return tuples_list


def compute_part_one(file_name: str) -> str:
    data = read_input_file(file_name)
    print(f'{data= }')

    # Convert to NumPy array
    X = np.array(data)

    # Apply DBSCAN with Manhattan distance
    dbscan = DBSCAN(eps=3, min_samples=1, metric='manhattan')
    labels = dbscan.fit_predict(X)

    # Reduce dimensions to 2D for visualization
    pca = PCA(n_components=2)
    X_reduced = pca.fit_transform(X)

    # Plotting
    plt.figure(figsize=(8, 6))
    unique_labels = set(labels)
    colors = plt.cm.get_cmap('tab10', len(unique_labels))

    for label in unique_labels:
        mask = labels == label
        plt.scatter(X_reduced[mask, 0], X_reduced[mask, 1],
                    label=f'Cluster {label}' if label != -1 else 'Noise',
                    s=100, edgecolors='k')

    plt.title('DBSCAN Clustering (Manhattan Distance)')
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

    return f"Number of clusters: {n_clusters}"


def compute_part_two(file_name: str) -> str:
    content = read_input_file(file_name)
    return "part 2 not yet implemented"


if __name__ == '__main__':
    file_path = 'input/input25.txt'
    print(f"Part I: {compute_part_one(file_path)}")
    print(f"Part II: {compute_part_two(file_path)}")