from tkinter import *
from tkinter import ttk

MAT = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
       [1, 1, 1, 0, 0, 0, 0, 1, 1, 1], 
       [1, 1, 0, 0, 0, 0, 0, 0, 1, 1], 
       [1, 1, 1, 0, 0, 0, 0, 1, 1, 1], 
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
p = [(0, 4), (1, 4), (1, 3), (1, 2), (2, 2), (2, 1), (3, 1), (4, 1), (4, 2), (5, 2), (5, 3), (5, 4), (6, 4)]

def showGrid(matrix, path):
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()

    # Define the size of each cell in pixels
    cell_size = 50

    canvas = Canvas(frm, width=len(matrix[0]) * cell_size, height=len(matrix) * cell_size)
    canvas.grid(column=0, row=0, columnspan=len(matrix[0]), rowspan=len(matrix))

    # Draw cells
    for r in range(len(matrix)):
        for c in range(len(matrix[0])):
            color = "green" if matrix[r][c] == 1 else "red"
            x0, y0 = c * cell_size, r * cell_size
            x1, y1 = x0 + cell_size, y0 + cell_size
            canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")
        
    # Convert the path to canvas coordinates and draw the line 
    path_coords = [(c * cell_size + cell_size // 2, r * cell_size + cell_size // 2) for (r, c) in path]

    canvas.create_line(path_coords, fill="blue", width=2)

    root.mainloop()