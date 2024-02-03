from dataclasses import dataclass, field
import math
import argparse


points = []
faces = []
cells = []

@dataclass
class point:
    x: float
    y: float
    z: float


def vec_area(A, B, C):
    AB_x = B.x - A.x
    AC_x = C.x - A.x
    AB_y = B.y - A.y
    AC_y = C.y - A.y
    AB_z = B.z - A.z
    AC_z = C.z - A.z
    cross_x = (AB_y * AC_z) - (AB_z * AC_y)
    cross_y = (AB_z * AC_x) - (AB_x * AC_z)
    cross_z = (AB_x * AC_y) - (AB_y * AC_x)
    return [0.5*cross_x, 0.5*cross_y, 0.5*cross_z]

def abs_area(A, B, C):
    v = vec_area(A, B, C)
    area_2 = (v[0]*v[0]) + (v[1]*v[1]) + (v[2]*v[2])
    return math.sqrt(area_2)
     
def add_vectors(v1, v2):
    help_v = [0.0, 0.0, 0.0]
    help_v[0] = v1[0] + v2[0]
    help_v[1] = v1[1] + v2[1]
    help_v[2] = v1[2] + v2[2]
    return help_v

def volume(A, B, C, D):
    base_area = vec_area(A, B, C)
    AD_x = D.x - A.x
    AD_y = D.y - A.y
    AD_z = D.z - A.z
    help = AD_x*base_area[0]
    help += AD_y*base_area[1]
    help += AD_z*base_area[2]
    return abs(help/3)


@dataclass
class face:
    vertices_list: list
    owner: int = False
    neighbour: int = False
    centre: point = field(init=False)
    area: list = field(init=False)

    def __post_init__(self):
        temp_centre_x = 0
        temp_centre_y = 0
        temp_centre_z = 0
        for vertex in self.vertices_list:
            temp_centre_x += points[vertex].x
            temp_centre_y += points[vertex].y
            temp_centre_z += points[vertex].z
        n_vertices = len(self.vertices_list)
        temp_centre_x = temp_centre_x / n_vertices
        temp_centre_y = temp_centre_y / n_vertices
        temp_centre_z = temp_centre_z / n_vertices
        temp_centre = point(temp_centre_x, temp_centre_y, temp_centre_z)
        centre_x = 0
        centre_y = 0
        centre_z = 0
        temp_total_area = 0
        
        for i in range(n_vertices):
            next = (i+1) % n_vertices
            A = points[self.vertices_list[i]]
            B = points[self.vertices_list[next]]
            tri_area = abs_area(temp_centre, A, B)
            centre_x += (temp_centre_x + A.x + B.x)*tri_area
            centre_y += (temp_centre_y + A.y + B.y)*tri_area
            centre_z += (temp_centre_z + A.z + B.z)*tri_area
            temp_total_area += tri_area
        centre_x = centre_x / (3*temp_total_area)
        centre_y = centre_y / (3*temp_total_area)
        centre_z = centre_z / (3*temp_total_area)
        self.centre = point(centre_x, centre_y, centre_z)
        self.area = [0, 0, 0]
        for i in range(n_vertices):
            next = (i+1) % n_vertices
            A = points[self.vertices_list[i]]
            B = points[self.vertices_list[next]]
            self.area = add_vectors(self.area, vec_area(temp_centre, A, B))

@dataclass
class cell:
    faces_list: list
    neighbours: list = False
    volume: float = field(init = False)
    centre: point = field(init = False)

    def __post_init__(self):
        temp_centre_x = 0
        temp_centre_y = 0
        temp_centre_z = 0
        n_faces = len(self.faces_list)
        for i in range(n_faces):
            side = faces[self.faces_list[i]]
            temp_centre_x += side.centre.x
            temp_centre_y += side.centre.y
            temp_centre_z += side.centre.z
        temp_centre_x = temp_centre_x / n_faces
        temp_centre_y = temp_centre_y / n_faces
        temp_centre_z = temp_centre_z / n_faces
        temp_centre = point(temp_centre_x, temp_centre_y, temp_centre_z)
        centre_x = 0
        centre_y = 0
        centre_z = 0
        temp_total_volume = 0
        for i in range(n_faces):
            side = faces[self.faces_list[i]]
            n_side_verices = len(side.vertices_list)
            C = side.centre
            for j in range(n_side_verices):
                next = (j+1) % n_side_verices
                A = points[side.vertices_list[j]]
                B = points[side.vertices_list[next]]
                tetra_volume = volume(temp_centre, C, A, B)
                centre_x += (temp_centre_x + A.x + B.x + C.x)*tetra_volume
                centre_y += (temp_centre_y + A.y + B.y + C.y)*tetra_volume
                centre_z += (temp_centre_z + A.z + B.z + C.z)*tetra_volume
                temp_total_volume += tetra_volume
        centre_x = centre_x / (4*temp_total_volume)
        centre_y = centre_y / (4*temp_total_volume)
        centre_z = centre_z / (4*temp_total_volume)
        self.centre = point(centre_x, centre_y, centre_z)
        self.volume = 0
        for i in range(n_faces):
            side = faces[self.faces_list[i]]
            n_side_verices = len(side.vertices_list)
            C = side.centre
            for j in range(n_side_verices):
                next = (j+1) % n_side_verices
                A = points[side.vertices_list[j]]
                B = points[side.vertices_list[next]]
                self.volume += volume(self.centre, C, A, B)

def test():
    global points
    global faces
    global cells

    p0 = point(0, 0, 0)
    p1 = point(1, 0, 0)
    p2 = point(1, 1, 0)
    p3 = point(0, 1, 0)
    p4 = point(0, 0, 1)
    p5 = point(1, 0, 1)
    p6 = point(1, 1, 1)
    p7 = point(0, 1, 1)

    points = [p0, p1, p2, p3, p4, p5, p6, p7]

    f0 = face([0, 1, 2, 3])
    f1 = face([0, 3, 7, 4])
    f2 = face([0, 4, 5, 1])
    f3 = face([1, 2, 6, 5])
    f4 = face([3, 7, 6, 2])
    f5 = face([4, 5, 6, 7])

    faces = [f0, f1, f2, f3, f4, f5]

    v = cell([0, 1, 2, 3, 4, 5])

    cells = [v]
    print(f0.area)
    print(f1.area)
    print(f2.area)
    print(f3.area)
    print(f4.area)
    print(f5.area)
    print(f0.centre)
    print(f1.centre)
    print(f2.centre)
    print(f3.centre)
    print(f4.centre)
    print(f5.centre)
    print(v.volume)
    print(v.centre)
    print(cells[0].volume)

def print_neighbours():
    print("faces")
    for i in faces:
        print(i.owner, i.neighbour)
    print("cells")
    for i in cells:
        print(i.neighbours)

parser = argparse.ArgumentParser()
parser.add_argument('points_file_address')
parser.add_argument('faces_file_address')
parser.add_argument('cells_file_address')
parser.add_argument('boundary_file_address')
files = parser.parse_args()

points = []
points_file = open(files.points_file_address, 'r')
n_points = int(points_file.readline())
points_file.readline()
for i in range(n_points):
    new_point = points_file.readline()
    new_point = new_point.replace("(", "")
    new_point = new_point.replace(")", "")
    new_point = new_point.split()
    x = float(new_point[0])
    y = float(new_point[1])
    z = float(new_point[2])
    points.append(point(x, y, z))
points_file.close()
del points_file
#print(points)

faces = []
faces_file = open(files.faces_file_address, 'r')
n_faces = int(faces_file.readline())
faces_file.readline()
for i in range(n_faces):
    new_face = faces_file.readline()
    new_face = new_face.split("(")
    n_vertices = int(new_face[0])
    verices_list = new_face[1]
    verices_list = verices_list.replace(")", "")
    verices_list = verices_list.split()
    for j in range(n_vertices):
        verices_list[j] = int(verices_list[j])
    faces.append(face(verices_list))
faces_file.close()
#print(faces)

cells = []
cells_file = open(files.cells_file_address, 'r')
n_cells = int(cells_file.readline())
cells_file.readline()
for i in range(n_cells):
    new_cell = cells_file.readline()
    new_cell = new_cell.split("(")
    num_sides = int(new_cell[0])
    sides_list = new_cell[1]
    sides_list = sides_list.replace(")", "")
    sides_list = sides_list.split()
    for j in range(num_sides):
        sides_list[j] = int(sides_list[j])
    cells.append(cell(sides_list))
    for j in range(num_sides):
        side = sides_list[j]
        print(side)
        if (type(faces[side].owner) == type(False)):
            # face does not have an owner
            # this is the smallest number cell it belongs to, so this cell becomes the owner
            faces[side].owner = i
        else:
            # faces has an owner so this is a neighbour
            faces[side].neighbour = i
            the_other_cell = faces[side].owner
            if (type(cells[i].neighbours) == type(False)):
                cells[i].neighbours = [the_other_cell]
            else:
                cells[i].neighbours.append(the_other_cell)
            if (type(cells[the_other_cell].neighbours) == type(False)):
                cells[the_other_cell].neighbours = [i]
            else:
                cells[the_other_cell].neighbours.append(i)
cells_file.close()
print_neighbours()
