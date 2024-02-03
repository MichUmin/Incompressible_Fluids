from dataclasses import dataclass, field
import math
import argparse
import mesh_geometry_operations as geo
import mesh_debug



class mesh:

    class point:
        def __init__(self, coordinate1, coordinate2, coordinate3):
            self.x = coordinate1
            self.y = coordinate2
            self.z = coordinate3
    
    class face:
        def __init__(self, vertices_list):
            self.vertices = vertices_list
            self.owner = -1
            self.neighbour = -1
            self.centre = False
            self.area = [0.0 , 0.0, 0.0]

    class cell:
        def __init__(self, faces_list):
            self.faces = faces_list
            self.neighbours = []
            self.volume = 0.0
            self.centre = False

    
    def __init__(self, PointsFile, FacesFile, CellsFile, BoundariesFile):
        self.points = []
        n_points = int(PointsFile.readline())
        PointsFile.readline()
        for i in range(n_points):
            new_point = PointsFile.readline()
            new_point = new_point.replace("(", "")
            new_point = new_point.replace(")", "")
            new_point = new_point.split()
            x = float(new_point[0])
            y = float(new_point[1])
            z = float(new_point[2])
            self.points.append(self.point(x, y, z))
        
        self.faces = []
        n_faces = int(FacesFile.readline())
        FacesFile.readline()
        for i in range(n_faces):
            new_face = FacesFile.readline()
            new_face = new_face.split("(")
            n_vertices = int(new_face[0])
            verices_list = new_face[1]
            verices_list = verices_list.replace(")", "")
            verices_list = verices_list.split()
            for j in range(n_vertices):
                verices_list[j] = int(verices_list[j])
            self.faces.append(self.face(verices_list))
            temp_centre_x = 0
            temp_centre_y = 0
            temp_centre_z = 0
            for vertex in self.faces[i].vertices:
                temp_centre_x += self.points[vertex].x / n_vertices
                temp_centre_y += self.points[vertex].y / n_vertices
                temp_centre_z += self.points[vertex].z / n_vertices
            temp_centre = self.point(temp_centre_x, temp_centre_y, temp_centre_z)
            centre_x = 0
            centre_y = 0
            centre_z = 0
            temp_total_area = 0
            for vertex_num in range(n_vertices):
                next = (vertex_num+1) % n_vertices
                A = self.points[self.faces[i].vertices[vertex_num]]
                B = self.points[self.faces[i].vertices[next]]
                tri_area = geo.abs_area(temp_centre, A, B)
                centre_x += (temp_centre_x + A.x + B.x)*tri_area
                centre_y += (temp_centre_y + A.y + B.y)*tri_area
                centre_z += (temp_centre_z + A.z + B.z)*tri_area
                temp_total_area += tri_area
            centre_x = centre_x / (3*temp_total_area)
            centre_y = centre_y / (3*temp_total_area)
            centre_z = centre_z / (3*temp_total_area)
            self.faces[i].centre = self.point(centre_x, centre_y, centre_z)
            for vertex_num in range(n_vertices):
                next = (vertex_num+1) % n_vertices
                A = self.points[self.faces[i].vertices[vertex_num]]
                B = self.points[self.faces[i].vertices[next]]
                self.faces[i].area = geo.add_vectors(self.faces[i].area, geo.vec_area(temp_centre, A, B))

        
        self.cells = []
        n_cells = int(CellsFile.readline())
        CellsFile.readline()
        for i in range(n_cells):
            new_cell = CellsFile.readline()
            new_cell = new_cell.split("(")
            num_sides = int(new_cell[0])
            sides_list = new_cell[1]
            sides_list = sides_list.replace(")", "")
            sides_list = sides_list.split()
            for j in range(num_sides):
                sides_list[j] = int(sides_list[j])
            self.cells.append(self.cell(sides_list))
            for j in range(num_sides):
                side = sides_list[j]
                print(side)
                if (self.faces[side].owner < 0):
                    # face does not have an owner
                    # this is the smallest number cell it belongs to, so this cell becomes the owner
                    self.faces[side].owner = i
                else:
                    # faces has an owner so this is a neighbour
                    self.faces[side].neighbour = i
                    the_other_cell = self.faces[side].owner
                    self.cells[i].neighbours.append(the_other_cell)
                    self.cells[the_other_cell].neighbours.append(i)
            temp_centre_x = 0
            temp_centre_y = 0
            temp_centre_z = 0
            for side_index in range(num_sides):
                side = self.faces[self.cells[i].faces[side_index]]
                temp_centre_x += side.centre.x / n_faces
                temp_centre_y += side.centre.y / n_faces
                temp_centre_z += side.centre.z / n_faces
            temp_centre = self.point(temp_centre_x, temp_centre_y, temp_centre_z)
            centre_x = 0
            centre_y = 0
            centre_z = 0
            temp_total_volume = 0
            for side_index in range(num_sides):
                side = self.faces[self.cells[i].faces[side_index]]
                n_side_verices = len(side.vertices)
                C = side.centre
                for j in range(n_side_verices):
                    next = (j+1) % n_side_verices
                    A = self.points[side.vertices[j]]
                    B = self.points[side.vertices[next]]
                    tetra_volume = geo.volume(temp_centre, C, A, B)
                    centre_x += (temp_centre_x + A.x + B.x + C.x)*tetra_volume
                    centre_y += (temp_centre_y + A.y + B.y + C.y)*tetra_volume
                    centre_z += (temp_centre_z + A.z + B.z + C.z)*tetra_volume
                    temp_total_volume += tetra_volume
            centre_x = centre_x / (4*temp_total_volume)
            centre_y = centre_y / (4*temp_total_volume)
            centre_z = centre_z / (4*temp_total_volume)
            self.cells[i].centre = self.point(centre_x, centre_y, centre_z)
            self.cells[i].volume = 0.0
            for side_index in range(num_sides):
                side = self.faces[self.cells[i].faces[side_index]]
                n_side_verices = len(side.vertices)
                C = side.centre
                for j in range(n_side_verices):
                    next = (j+1) % n_side_verices
                    A = self.points[side.vertices[j]]
                    B = self.points[side.vertices[next]]
                    self.cells[i].volume += geo.volume(self.cells[i].centre, C, A, B)



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
mesh1 = mesh(points_file, faces_file, cells_file, boundaries_file)
points_file.close()
faces_file.close()
cells_file.close()
boundaries_file.close()
del points_file
del faces_file
del cells_file
del boundaries_file

mesh_debug.print_neighbours(mesh1)
