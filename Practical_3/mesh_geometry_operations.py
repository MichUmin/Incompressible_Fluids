import math

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

def dot_product(v1, v2):
    result = v1[0]*v2[0]
    result += v1[1]*v2[1]
    result += v1[2]*v2[2]
    return result

def volume(A, B, C, D):
    base_area = vec_area(A, B, C)
    AD_x = D.x - A.x
    AD_y = D.y - A.y
    AD_z = D.z - A.z
    help = AD_x*base_area[0]
    help += AD_y*base_area[1]
    help += AD_z*base_area[2]
    return abs(help/3)

def distance(A, B):
    result = (A.x - B.x)**2
    result += (A.y - B.y)**2
    result += (A.z - B.z)**2
    return (math.sqrt(result))

def vec_len(vec):
    result = vec[0]*vec[0] + vec[1]*vec[1] + vec[2]*vec[2]
    return (math.sqrt(result))
    