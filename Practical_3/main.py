import math
import numpy
import mesh_class
import field_class
import argparse
import mesh_debug
import initialize
import discretize
import output
import os
import printing

parser = argparse.ArgumentParser()
parser.add_argument('points_file_address')
parser.add_argument('faces_file_address')
parser.add_argument('cells_file_address')
parser.add_argument('boundary_file_address')
parser.add_argument('output_directory_address')
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

output_directory_address = files.output_directory_address
if not os.path.isdir(output_directory_address):
    print("invalid output directory")
    exit()
if len(os.listdir(output_directory_address)) > 0:
    print("non empty output directory")
    exit()

N = len(mesh1.cells)
T = field_class.scalar_field(N)
u = field_class.vector_field(N)
gamma = field_class.scalar_field(N)

source_point_vector = [0.499, 0.0, 0.0]
source_cell = mesh1.find(source_point_vector)

initialize.velocity(u, mesh1)
initialize.variable(T, mesh1)
initialize.diffusion_coef(gamma, mesh1)
#initialize.boundary_condition(mesh1)

tStart = 0.0
tStop = 1.0
time_step = 0.05
tCurrent = tStart
step = 0

print(tCurrent)
output_file = os.path.join(output_directory_address, "step"+str(step)+".dat")
printing.twoD_scalar(output_file, T, mesh1)

while tCurrent < tStop:
    dt = min(time_step, tStop - tCurrent)
    A = numpy.zeros((N, N))
    b = numpy.zeros((N, 1))
    discretize.time_derivative(T, dt, A, b, mesh1)
    # print(A)
    # print(b)
    discretize.diffusion(T, gamma, A, b, mesh1)
    discretize.convection(T, u, A, b, mesh1)
    discretize.source(source_cell, T, A, b, mesh1)
    # if (tCurrent == tStart):
    #     print(A)
    #     print(b)
    T.values = numpy.linalg.solve(A,b)
    tCurrent += dt
    step += 1
    print(tCurrent)
    output_file = os.path.join(output_directory_address, "step"+str(step)+".dat")
    printing.twoD_scalar(output_file, T, mesh1)


