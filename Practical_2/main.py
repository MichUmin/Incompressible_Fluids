import math
import numpy
import mesh_class
import argparse
import mesh_debug
import initialize
import discretize

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

#mesh_debug.print_neighbours(mesh1)

N = len(mesh1.cells)
T = numpy.zeros((N,1))
u = numpy.zeros((N,3))
gamma = numpy.zeros((N,1))

initialize.velocity(u, mesh1)
initialize.variable(T, mesh1)
initialize.variable(gamma, mesh1)

tStart = 0.0
tStop = 1.0
time_step = 0.5
tCurrent = tStart
print(T)
while tCurrent < tStop:
    dt = min(time_step, tStop - tCurrent)
    A = numpy.zeros((N, N))
    b = numpy.zeros((N, 1))
    discretize.time_derivative(T, dt, A, b, mesh1)
    #print(A)
    #print(b)
    discretize.diffusion(T, gamma, A, b, mesh1)
    #print(A)
    #print(b)
    T = numpy.linalg.solve(A,b)
    print(T)
    tCurrent += dt

