import re

from dataclasses import dataclass

@dataclass
class Particle:
    x: int
    y: int
    vx: int
    vy: int

    def move(self, time: int):
        """Update position based on velocity and time."""
        self.x += self.vx * time
        self.y += self.vy * time



def read_input_file(file_name: str) -> list:
    with open(file_name) as f:
        content = f.read().splitlines()

    particles = []
    for p in content:
        d = list(map(int, re.findall(r'-?\d+', p)))
        particle = Particle(*d)
        particles.append(particle)

    return particles

def calculate_area(particles: list) -> int:
    points = []
    for particle in particles:
        points.append((particle.x, particle.y))

    minx = min(p[0] for p in points)
    miny = min(p[1] for p in points)
    maxx = max(p[0] for p in points) + 1
    maxy = max(p[1] for p in points) + 1

    area = (maxx-minx) * (maxy-miny)

    return area

def print_particles(particles: list) -> None:
    points = []
    for particle in particles:
        points.append((particle.x, particle.y))

    # minx, maxx = min(p.x for p in particles), max(p.x for p in particles)
    # miny, maxy = min(p.y for p in particles), max(p.y for p in particles)
    # area = (maxx - minx) * (maxy - miny)

    minx = min(p[0] for p in points)
    miny = min(p[1] for p in points)
    maxx = max(p[0] for p in points) + 1
    maxy = max(p[1] for p in points) + 1

    for y in range(miny, maxy):
        for x in range(minx, maxx):
            if (x, y) in points:
                print('#', end='')
            else:
                print('.', end='')
        print()



def compute_part(file_name: str) -> None:
    particles = read_input_file(file_name)
    print(f'{particles= }')
    min_area = calculate_area(particles)

    for t in range(1,20000):
        for p in particles:
            p.move(1)
        area = calculate_area(particles)
        if area < min_area:
            t_min = t
            min_area = area

    particles = read_input_file(file_name)
    for p in particles:
        p.move(t_min)
    print("part I:")
    print_particles(particles)
    print(f"Part II: {t_min= }")


if __name__ == '__main__':
    file_path = 'input/input10.txt'
    compute_part(file_path)
