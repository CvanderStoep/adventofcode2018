import numpy as np


def read_input_file(file_name: str) -> np.ndarray:
    with open(file_name) as f:
        coordinates = np.array([list(map(int, line.split(", "))) for line in f.read().splitlines()])
    return coordinates


def manhattan_distance(p1: np.ndarray, p2: np.ndarray) -> np.ndarray:
    return np.abs(p1[:, None, :] - p2[None, :, :]).sum(axis=2)


def compute_part_one(file_name: str) -> None:
    coordinates = read_input_file(file_name)

    minX, minY = coordinates.min(axis=0)
    maxX, maxY = coordinates.max(axis=0)

    gridX, gridY = np.meshgrid(np.arange(minX - 1, maxX + 2), np.arange(minY - 1, maxY + 2))
    grid_points = np.vstack([gridX.ravel(), gridY.ravel()]).T

    distances = manhattan_distance(grid_points, coordinates)

    closest = np.argmin(distances, axis=1)
    unique, counts = np.unique(closest, return_counts=True)

    part_two_area = np.sum(distances.sum(axis=1) < 10000)

    print("Part I: Largest finite area:", counts.max())
    print("Part II: Region with total distance < 10000:", part_two_area)


if __name__ == '__main__':
    file_path = 'input/input6.txt'
    compute_part_one(file_path)
