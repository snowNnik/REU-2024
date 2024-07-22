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

    # Mark the start point
    start_row, start_col = path[0]
    start_x = start_col * cell_size + cell_size // 2
    start_y = start_row * cell_size + cell_size // 2
    canvas.create_oval(start_x - 15, start_y - 15, start_x + 15, start_y + 15, outline="black", width=2)
    canvas.create_text(start_x, start_y, text="S", fill="Black", font=("Helvetica", 16, "bold"))

    # Mark the end point
    end_row, end_col = path[-1]
    end_x = end_col * cell_size + cell_size // 2
    end_y = end_row * cell_size + cell_size // 2
    canvas.create_oval(end_x - 15, end_y - 15, end_x + 15, end_y + 15, outline="black", width=2)
    canvas.create_text(end_x, end_y, text="X", fill="Black", font=("Helvetica", 16, "bold"))

    # Load and resize the GIF
    original_gif = PhotoImage(file="./drone.png")  ############## Change path accordingly #################
    # Resize the image
    resized_gif = original_gif.subsample(6,5)  # Adjust the subsample factor as needed
    drone_img = resized_gif
    
    # Create the image on the canvas
    drone = canvas.create_image(0, 0, anchor=NW, image=drone_img)

    # Animate the drone along the path
    def move_drone(index=0):
        if index < len(path_coords):
            x, y = path_coords[index]
            canvas.coords(drone, x - 20, y - 20)  # Adjust position to center the image
            root.after(500, move_drone, index + 1)  # Move to next point after 500 ms

    # Start the drone animation
    move_drone()

    root.mainloop()