import math
import numpy
import mesh_class
import field_class
import argparse
import mesh_debug
import initialize
import discretize
import output

parser = argparse.ArgumentParser()
parser.add_argument('points_file_address')
parser.add_argument('faces_file_address')
parser.add_argument('cells_file_address')
parser.add_argument('boundary_file_address')
files = parser.parse_args()

points_file = open(files.points_file_address, 'r')
faces_file = open(files.faces_file_address, 'r')
cells_file = open(files.cells_file_address, 'r')
boundaries_file = open(files.boundary_file_address, 'r')
mesh1 = mesh_class.mesh(points_file, faces_file, cells_file, boundaries_file)
points_file.close()
faces_file.close()
cells_file.close()
boundaries_file.close()
del points_file
del faces_file
del cells_file
del boundaries_file

n_cells = len(mesh1.cells)

for i in range(n_cells):
    for j in range(n_cells):
        point_to_try = mesh1.cells[j].centre
        result = mesh1.is_inside(point_to_try, i)
        if ((i == j)and(result == False)):
            print("Fail centre of", j ,"is in", i)
        if ((i != j)and(result != False)):
            print("Fail centre of", j, "should not be in", i)
    result2 = mesh1.find(mesh1.cells[i].centre)
    if result2 != i:
        print("Fail centre of", i, "should be in", i)
        