from dataclasses import dataclass, filed
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

@dataclass
class face:
    vertices: list
    owner: int = false
    neighbour: int = false
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

        