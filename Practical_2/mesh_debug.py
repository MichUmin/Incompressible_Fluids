def print_neighbours(some_mesh):
    print("faces")
    for i in some_mesh.faces:
        print(i.owner, i.neighbour)
        print(i.boundary_type)
    print("cells")
    for i in some_mesh.cells:
        print(i.neighbours)

