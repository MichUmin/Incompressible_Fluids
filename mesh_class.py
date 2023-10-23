from dataclasses import dataclass, field
import math

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
    help_v = [0, 0, 0]
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
    vertices: list
    owner: int = False
    neighbour: int = False
    centre: point = field(init=False)
    area: list = field(init=False)

    def __post_init__(self):
        temp_centre_x = 0
        temp_centre_y = 0
        temp_centre_z = 0
        for vertex in self.vertices:
            temp_centre_x += vertex.x
            temp_centre_y += vertex.y
            temp_centre_z += vertex.z
        temp_centre_x = temp_centre_x / len(self.vertices)
        temp_centre_y = temp_centre_y / len(self.vertices)
        temp_centre_z = temp_centre_z / len(self.vertices)
        temp_centre = point(temp_centre_x, temp_centre_y, temp_centre_z)
        centre_x = 0
        centre_y = 0
        centre_z = 0
        temp_total_area = 0
        n_verices = len(self.vertices)
        for i in range(n_verices):
            next = (i+1) % n_verices
            tri_area = abs_area(temp_centre, self.vertices[i], self.vertices[next])
            centre_x += (temp_centre_x + self.vertices[i].x + self.vertices[next].x)*tri_area
            centre_y += (temp_centre_y + self.vertices[i].y + self.vertices[next].y)*tri_area
            centre_z += (temp_centre_z + self.vertices[i].z + self.vertices[next].z)*tri_area
            temp_total_area += tri_area
        centre_x = centre_x / (3*temp_total_area)
        centre_y = centre_y / (3*temp_total_area)
        centre_z = centre_z / (3*temp_total_area)
        self.centre = point(centre_x, centre_y, centre_z)
        help_area = [0, 0, 0]
        for i in range(n_verices):
            next = (i+1) % n_verices
            help_area = add_vectors(help_area, vec_area(temp_centre, self.vertices[i], self.vertices[next]))
        self.area = help_area

@dataclass
class cell:
    faces: list
    neighbours: list = False
    volume: float = field(init = False)
    centre: point = field(init = False)

    def __post_init__(self):
        temp_centre_x = 0
        temp_centre_y = 0
        temp_centre_z = 0
        for side in self.faces:
            temp_centre_x += side.centre.x
            temp_centre_y += side.centre.y
            temp_centre_z += side.centre.z
        temp_centre_x = temp_centre_x / len(self.faces)
        temp_centre_y = temp_centre_y / len(self.faces)
        temp_centre_z = temp_centre_z / len(self.faces)
        temp_centre = point(temp_centre_x, temp_centre_y, temp_centre_z)
        print(temp_centre)
        centre_x = 0
        centre_y = 0
        centre_z = 0
        temp_total_volume = 0
        n_sides = len(self.faces)
        for i in range(n_sides):
            n_verices = len(self.faces[i].vertices)
            for j in range(n_verices):
                next = (j+1) % n_verices
                A = self.faces[i].vertices[j]
                B = self.faces[i].vertices[next]
                C = self.faces[i].centre
                tetra_volume = volume(temp_centre, C, A, B)
                centre_x += (temp_centre_x + A.x + B.x + C.x)*tetra_volume
                centre_y += (temp_centre_y + A.y + B.y + C.y)*tetra_volume
                centre_z += (temp_centre_z + A.z + B.z + C.z)*tetra_volume
                temp_total_volume += tetra_volume
            print(temp_total_volume)
        centre_x = centre_x / (4*temp_total_volume)
        centre_y = centre_y / (4*temp_total_volume)
        centre_z = centre_z / (4*temp_total_volume)
        self.centre = point(centre_x, centre_y, centre_z)
        self.volume = 0
        for i in range(n_sides):
            n_verices = len(self.faces[i].vertices)
            for j in range(n_verices):
                next = (j+1) % n_verices
                A = self.faces[i].vertices[j]
                B = self.faces[i].vertices[next]
                C = self.faces[i].centre
                self.volume += volume(self.centre, C, A, B)



p0 = point(0, 0, 0)
p1 = point(1, 0, 0)
p2 = point(1, 1, 0)
p3 = point(0, 1, 0)
p4 = point(0, 0, 1)
p5 = point(1, 0, 1)
p6 = point(1, 1, 1)
p7 = point(0, 1, 1)

f0 = face([p0, p1, p2, p3])
f1 = face([p0, p3, p7, p4])
f2 = face([p0, p4, p5, p1])
f3 = face([p1, p2, p6, p5])
f4 = face([p3, p7, p6, p2])
f5 = face([p4, p5, p6, p7])

v = cell([f0, f1, f2, f3, f4, f5])
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


