def read_input_file(file_name: str) -> list:
    with open(file_name) as f:
        content = f.read().splitlines()

    coordinates = []
    for c in content:
        x, y = c.split(', ')
        x, y = int(x), int(y)
        coordinates.append((x,y))

    return coordinates

def manhattan_distance(p1: tuple, p2: tuple) -> int:
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

def compute_part_one(file_name: str) -> None:
    coordinates = read_input_file(file_name)
    print(f'{coordinates= }')

    maxX = max(coordinates, key=lambda c: c[0])[0] + 1
    maxY = max(coordinates, key=lambda c: c[1])[1] + 1
    # max_x = max(c[0] for c in coordinates)
    coordinate_areas = [0] * len(coordinates)
    part_two_area = 0

    for x in range(maxX):
        for y in range(maxY):
            closest_coord = 0
            shortest_distance = None
            total_distance = 0
            for i, coord in enumerate(coordinates):
                distance = abs(x - coord[0]) + abs(y - coord[1])
                if shortest_distance is None or distance < shortest_distance:
                    closest_coord = i
                    shortest_distance = distance
                elif distance == shortest_distance:
                    closest_coord = -1  # tie between several coords

                total_distance += distance
            if closest_coord != -1:
                coordinate_areas[closest_coord] += 1
            if total_distance < 10000:
                part_two_area += 1

# sweep 2, include the edges and if the area changes, exclude it.
# alternative solution, see day6-github
    coordinate_areas_edge = [0] * len(coordinates)
    for x in range(-1, maxX+1):
        for y in range(-1, maxY+1):
            closest_coord = 0
            shortest_distance = None
            for i, coord in enumerate(coordinates):
                distance = abs(x - coord[0]) + abs(y - coord[1])
                if shortest_distance is None or distance < shortest_distance:
                    closest_coord = i
                    shortest_distance = distance
                elif distance == shortest_distance:
                    closest_coord = -1  # tie between several coords
            if closest_coord != -1:
                coordinate_areas_edge[closest_coord] += 1

    filtered_areas = [a for a, b in zip(coordinate_areas, coordinate_areas_edge) if a == b]
    print("partI: Largest area around one coord:", max(filtered_areas))
    print("partII: Area with a distance of less than 10000 to all coords:", part_two_area)

    return



if __name__ == '__main__':
    file_path = 'input/input6.txt'
    compute_part_one(file_path)
