import mesh_geometry_operations as geo

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
            self.inter_coef = 0.5
            self.boundary_name = "internal"

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

            #add centre and volume
            temp_centre_x = 0
            temp_centre_y = 0
            temp_centre_z = 0
            for side_index in range(num_sides):
                side = self.faces[sides_list[side_index]]
                temp_centre_x += side.centre.x / num_sides
                temp_centre_y += side.centre.y / num_sides
                temp_centre_z += side.centre.z / num_sides
            #print(i, "temrorary", temp_centre_x, temp_centre_y, temp_centre_z)
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
            #print(i, "temp volume", temp_total_volume, "centre", centre_x, centre_y, centre_z)
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
            #print(i, "volume", self.cells[i].volume)

            #add owner / neighbour
            for j in range(num_sides):
                side = sides_list[j]
                if (self.faces[side].owner < 0):
                    # face does not have an owner
                    # this is the smallest number cell it belongs to, so this cell becomes the owner
                    self.faces[side].owner = i
                else:
                    # faces has an owner so this is a neighbour
                    self.faces[side].neighbour = i
                    the_other_cell = self.faces[side].owner
                    d_p = geo.distance(self.faces[side].centre, self.cells[the_other_cell].centre)
                    d_n = geo.distance(self.faces[side].centre, self.cells[i].centre)
                    self.faces[side].inter_coef = d_p / (d_p + d_n)
                    self.cells[i].neighbours.append(the_other_cell)
                    self.cells[the_other_cell].neighbours.append(i)
        

        num_boundary_patches = int(BoundariesFile.readline())
        BoundariesFile.readline()
        for i in range(num_boundary_patches):
            name = BoundariesFile.readline() # read the type of the path
            name = name.replace("\n", "") # convert to plain string
            num_faces = int(BoundariesFile.readline()) # read the number of faces in the patch
            BoundariesFile.readline() # skip the opening bracket
            boundary_faces = BoundariesFile.readline()
            boundary_faces = boundary_faces.split(" ")
            for j in range(num_faces):
                boundary_face = int(boundary_faces[j])
                if self.faces[boundary_face].neighbour >= 0:
                    #this face has a neighbour so it is internal
                    print("Internal face encountered when reading bounary path: ", name)
                    quit()
                else:
                    self.faces[boundary_face].boundary_name = name
            BoundariesFile.readline() # skip the closing bracket

        # enforce that the face normal points out of the owner
        for f_index in range(n_faces):
            f = self.faces[f_index]
            o_index = f.owner
            o = self.cells[o_index]
            FC_vector = [0.0, 0.0, 0.0]
            FC_vector[0] = o.centre.x - f.centre.x
            FC_vector[1] = o.centre.y - f.centre.y
            FC_vector[2] = o.centre.z - f.centre.z
            if (geo.dot(FC_vector, f.area) > 0.0):
                self.faces[f_index].area = geo.flip(f.area)
    
    def is_inside(self, point_vector, cell_index):
        n_faces = len(self.cells[cell_index].faces)
        count = 0
        for index in range(n_faces):
            face_index = self.cells[cell_index].faces[index]
            f = self.faces[face_index]
            FP_vector = [0.0, 0.0, 0.0]
            FP_vector[0] = point_vector[0] - f.centre.x
            FP_vector[1] = point_vector[1] - f.centre.y
            FP_vector[2] = point_vector[2] - f.centre.z
            dot_p = geo.dot(f.area, FP_vector)
            if f.owner == cell_index:
                if dot_p <= 0.0:
                    count += 1
                else:
                    return False
            else:
                if dot_p >= 0.0:
                    count += 1
                else:
                    return False
                
        if count == n_faces:
            return True
        else:
            print("Loop done")
            return False
    
    def find(self, point_vector):
        n_cells = len(self.cells)
        for i in range(n_cells):
            if self.is_inside(point_vector, i):
                return(i)
        return(-1)










            