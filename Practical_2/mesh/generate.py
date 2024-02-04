x_size = 0.01
y_size = 1.0
z_size = 1.0
x_cells = 100
y_cells = 1
z_cells = 1


x_points = int(x_cells + 1)
y_points = int(y_cells + 1)
z_points = int(z_cells + 1)

points_file = open("points.txt", 'w')
line = str(x_points*y_points*z_points)
line += '\n'
points_file.write(line)
points_file.write('(\n')
for z_index in range(z_points):
    for y_index in range(y_points):
        for x_index in range(x_points):
            line = '('
            line += str(x_index*x_size)
            line += ' '
            line += str(y_index*y_size)
            line += ' '
            line += str(z_index*z_size)
            line += ')\n'
            points_file.write(line)
points_file.write(')\n')
points_file.close()

faces_file = open("faces.txt", 'w')
line = str(x_points*y_cells*z_cells + x_cells*y_points*z_cells + x_cells*y_cells*z_points)
line += '\n'
faces_file.write(line)
faces_file.write('(\n')
for z_index in range(z_cells):
    for y_index in range(y_cells):
        for x_index in range(x_points):
            line = '4('
            line += str(x_index + y_index*x_points + z_index*x_points*y_points)
            line += ' '
            line += str(x_index + (y_index+1)*x_points + z_index*x_points*y_points)
            line += ' '
            line += str(x_index + (y_index+1)*x_points + (z_index+1)*x_points*y_points)
            line += ' '
            line += str(x_index + y_index*x_points + (z_index+1)*x_points*y_points)
            line += ')\n'
            faces_file.write(line)
for z_index in range(z_cells):
    for y_index in range(y_points):
        for x_index in range(x_cells):
            line = '4('
            line += str(x_index + y_index*x_points + z_index*x_points*y_points)
            line += ' '
            line += str((x_index+1) + y_index*x_points + z_index*x_points*y_points)
            line += ' '
            line += str((x_index+1) + y_index*x_points + (z_index+1)*x_points*y_points)
            line += ' '
            line += str(x_index + y_index*x_points + (z_index+1)*x_points*y_points)
            line += ')\n'
            faces_file.write(line)
for z_index in range(z_points):
    for y_index in range(y_cells):
        for x_index in range(x_cells):
            line = '4('
            line += str(x_index + y_index*x_points + z_index*x_points*y_points)
            line += ' '
            line += str((x_index+1) + y_index*x_points + z_index*x_points*y_points)
            line += ' '
            line += str((x_index+1) + (y_index+1)*x_points + z_index*x_points*y_points)
            line += ' '
            line += str(x_index + (y_index+1)*x_points + z_index*x_points*y_points)
            line += ')\n'
            faces_file.write(line)
faces_file.write(')\n')
faces_file.close()

cells_file = open("cells.txt", 'w')
line = str(x_cells*y_cells*z_cells)
line += '\n'
cells_file.write(line)
cells_file.write('(\n')
for z_index in range(z_cells):
    for y_index in range(y_cells):
        for x_index in range(x_cells):
            line = '6('
            line += str(x_index + z_index*x_points*y_cells + y_index*x_points)
            line += ' '
            line += str(x_index + 1 + z_index*x_points*y_cells + y_index*x_points)
            line += ' '
            line += str(x_points*y_cells*z_cells + x_index + z_index*x_cells*y_points + y_index*x_cells)
            line += ' '
            line += str(x_points*y_cells*z_cells + x_index + z_index*x_cells*y_points + (y_index+1)*x_cells)
            line += ' '
            line += str(x_points*y_cells*z_cells + y_points*x_cells*z_cells + + x_index + z_index*x_cells*y_cells + y_index*x_cells)
            line += ' '
            line += str(x_points*y_cells*z_cells + y_points*x_cells*z_cells + + x_index + (z_index+1)*x_cells*y_cells + y_index*x_cells)
            line += ')\n'
            cells_file.write(line)
cells_file.write(')\n')
cells_file.close()

boundary_file = open("boundary.txt", 'w')
boundary_file.write('6\n')
boundary_file.write('(\n')

boundary_file.write('boundary0\n')
line = str(y_cells*z_cells)
boundary_file.write(line + '\n')
boundary_file.write('(\n')
line = ''
for z_index in range(z_cells):
    for y_index in range(y_cells):
        line += str(y_index*x_points + z_index*y_cells*x_points)
        line += ' '
boundary_file.write(line.rstrip() + '\n')
boundary_file.write(')\n')

boundary_file.write('boundary1\n')
line = str(y_cells*z_cells)
boundary_file.write(line + '\n')
boundary_file.write('(\n')
line = ''
for z_index in range(z_cells):
    for y_index in range(y_cells):
        line += str((x_points - 1) + y_index*x_points + z_index*y_cells*x_points)
        line += ' '
boundary_file.write(line.rstrip() + '\n')
boundary_file.write(')\n')

boundary_file.write('boundary2\n')
line = str(x_cells*z_cells)
boundary_file.write(line + '\n')
boundary_file.write('(\n')
line = ''
for z_index in range(z_cells):
    for x_index in range(x_cells):
        line += str(x_points*y_cells*z_cells + x_index + z_index*x_cells*y_points)
        line += ' '
boundary_file.write(line.rstrip() + '\n')
boundary_file.write(')\n')

boundary_file.write('boundary3\n')
line = str(x_cells*z_cells)
boundary_file.write(line + '\n')
boundary_file.write('(\n')
line = ''
for z_index in range(z_cells):
    for x_index in range(x_cells):
        line += str(x_points*y_cells*z_cells + x_index + z_index*x_cells*y_points + (y_points-1)*x_cells)
        line += ' '
boundary_file.write(line.rstrip() + '\n')
boundary_file.write(')\n')

boundary_file.write('boundary4\n')
line = str(y_cells*x_cells)
boundary_file.write(line + '\n')
boundary_file.write('(\n')
line = ''
for y_index in range(y_cells):
    for x_index in range(x_cells):
        line += str(x_points*y_cells*z_cells + y_points*x_cells*z_cells + + x_index + y_index*x_cells)
        line += ' '
boundary_file.write(line.rstrip() + '\n')
boundary_file.write(')\n')

boundary_file.write('boundary5\n')
line = str(y_cells*x_cells)
boundary_file.write(line + '\n')
boundary_file.write('(\n')
line = ''
for y_index in range(y_cells):
    for x_index in range(x_cells):
        line += str(x_points*y_cells*z_cells + y_points*x_cells*z_cells + + x_index + (z_points-1)*x_cells*y_cells + y_index*x_cells)
        line += ' '
boundary_file.write(line.rstrip() + '\n')
boundary_file.write(')\n')

boundary_file.write(')\n')
boundary_file.close()