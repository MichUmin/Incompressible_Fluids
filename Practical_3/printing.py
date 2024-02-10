def twoD_scalar(file_path, to_print, some_mesh):
    file = open(file_path, 'w')
    n_cells = len(some_mesh.cells)
    for i in range(n_cells):
        file.write(str(some_mesh.cells[i].centre.x)+" "+str(some_mesh.cells[i].centre.y)+" "+str(to_print.values[i][0])+"\n")
    file.close()