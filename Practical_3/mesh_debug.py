def print_neighbours(some_mesh):
    print("faces")
    for i in some_mesh.faces:
        print(i.owner, i.neighbour)
        print(i.boundary_name)
    print("cells")
    for i in some_mesh.cells:
        print(i.neighbours)

def print_centres(some_mesh):
    num_cells = len(some_mesh.cells)
    num_faces = len(some_mesh.faces)
    for f in range(num_faces):
        print("face", f, "area", some_mesh.faces[f].area, "centre:", some_mesh.faces[f].centre.x, some_mesh.faces[f].centre.y, some_mesh.faces[f].centre.z)

    for c in range(num_cells):
        print("cell", c, "volume", some_mesh.cells[c].volume, "centre:", some_mesh.cells[c].centre.x, some_mesh.cells[c].centre.y, some_mesh.cells[c].centre.z)

