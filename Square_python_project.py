import tkinter as tk
from tkinter import simpledialog, messagebox
import random

class GridApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Interactive Grid")

        # Constants for cell size
        self.cell_size = 50  # Size of each cell in pixels

        # Create a canvas for the grid
        self.canvas = tk.Canvas(master)
        self.canvas.pack()

        # Create a control panel
        self.control_panel = tk.Frame(master)
        self.control_panel.pack(pady=10)

        # Lock button
        self.lock_button = tk.Button(self.control_panel, text="I'm done with moving", command=self.lock_positions)
        self.lock_button.pack(side=tk.LEFT, padx=5)

        # Highlight buttons
        self.highlight_frame = tk.Frame(master)
        self.highlight_frame.pack(pady=10)

        self.buttons = {}
        for label in ['A', 'B', 'C']:
            btn = tk.Button(self.highlight_frame, text=label, command=lambda l=label: self.toggle_highlight(l))
            btn.pack(side=tk.LEFT, padx=10)
            self.buttons[label] = {'button': btn, 'highlighted': False}

        # Additional highlight buttons for outside highlighting
        for label in ["A'", "B'", "C'"]:
            btn = tk.Button(self.highlight_frame, text=label, command=lambda l=label: self.toggle_outside_highlight(l))
            btn.pack(side=tk.LEFT, padx=10)
            self.buttons[label] = {'button': btn, 'highlighted': False}

        # Initialize variables
        self.rectangles = []  # List to store rectangle info and IDs
        self.selected_rectangle = None  # Currently selected rectangle
        self.is_locked = False  # Flag for locking rectangle positions

        # Bind mouse click and key press events
        self.canvas.bind("<Button-1>", self.on_click)
        self.master.bind("<KeyPress>", self.on_key_press)

        # Ask for grid and rectangle dimensions
        self.ask_grid_and_rectangle_sizes()

    def ask_grid_and_rectangle_sizes(self):
        self.size_frame = tk.Toplevel(self.master)
        self.size_frame.title("Enter Grid and Rectangle Sizes")

        # Frame for grid size input
        grid_frame = tk.Frame(self.size_frame)
        grid_frame.pack(pady=5)

        grid_label = tk.Label(grid_frame, text="Grid Size (Rows, Columns):")
        grid_label.pack(side=tk.LEFT)

        self.grid_entry = tk.Entry(grid_frame, width=10)
        self.grid_entry.pack(side=tk.LEFT)

        # Prepare to enter rectangle sizes
        self.dimensions = []
        for i in range(3):  # For up to 3 rectangles
            frame = tk.Frame(self.size_frame)
            frame.pack(pady=5)

            label = tk.Label(frame, text=f"Rectangle {i + 1} (Width, Height):")
            label.pack(side=tk.LEFT)

            entry = tk.Entry(frame, width=10)
            entry.pack(side=tk.LEFT)
            self.dimensions.append(entry)

        submit_button = tk.Button(self.size_frame, text="Submit", command=self.process_sizes)
        submit_button.pack(pady=10)

    def process_sizes(self):
        try:
            # Process grid size
            grid_size = self.grid_entry.get().split(',')
            self.rows, self.cols = map(int, grid_size)
            if self.rows <= 0 or self.cols <= 0:
                raise ValueError("Grid dimensions must be positive integers.")

            # Draw the grid now that we have dimensions
            self.canvas.config(width=self.cols * self.cell_size, height=self.rows * self.cell_size)
            self.draw_grid()

            # Calculate total boxes and display it
            total_boxes = self.rows * self.cols
            self.display_total_boxes(total_boxes)  # Call the function to create the label

            # Process rectangle sizes
            for i, entry in enumerate(self.dimensions):
                width, height = map(int, entry.get().split(','))
                if width <= 0 or height <= 0:
                    raise ValueError("Dimensions must be positive integers.")
                self.place_rectangle(width, height, chr(65 + i))  # A=65, B=66, C=67

            self.size_frame.destroy()  # Close the input window
        except Exception as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}")
    
    def display_total_boxes(self, total_boxes):
        if hasattr(self, 'total_boxes_label'):
            self.total_boxes_label.config(text=f"Total Boxes: {total_boxes}")  # Update existing label
        else:
            self.total_boxes_label = tk.Label(self.master, text=f"Total Boxes: {total_boxes}", font=("Arial", 12))
            self.total_boxes_label.place(relx=0.95, rely=0.01, anchor='ne')  # Position it in the top right corner


    def place_rectangle(self, width, height, label):
        # Random position for rectangle
        x = random.randint(0, self.cols - width) * self.cell_size
        y = random.randint(0, self.rows - height) * self.cell_size
        rectangle_id = self.canvas.create_rectangle(
            x, y,
            x + width * self.cell_size,
            y + height * self.cell_size,
            outline="black", fill="", width=4
        )
        
        # Create a label in the top right corner
        label_id = self.canvas.create_text(
            x + width * self.cell_size - 10, y + 10,
            text=label, anchor=tk.NE, font=("Arial", 10, "bold"), fill="black"
        )

        self.rectangles.append((rectangle_id, (width, height), label_id))  # Store rectangle ID, size, and label ID

    def draw_grid(self):
        self.canvas.delete("grid")  # Clear previous grid if any
        for i in range(self.rows):
            for j in range(self.cols):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="white", tags="grid")

    def on_click(self, event):
        if self.is_locked:
            return  # Do nothing if locked

        clicked_item = self.canvas.find_closest(event.x, event.y)
        if clicked_item:
            rect_id = clicked_item[0]
            # Check if the clicked item is a rectangle
            if rect_id in [r[0] for r in self.rectangles]:
                self.selected_rectangle = rect_id  # Set the selected rectangle

                # Toggle the boldness of the rectangle's outline
                current_outline = self.canvas.itemcget(rect_id, "outline")
                if current_outline == "black":
                    self.canvas.itemconfig(rect_id, outline="red", width=6)  # Highlight
                else:
                    self.canvas.itemconfig(rect_id, outline="black", width=6)  # Reset

    def on_key_press(self, event):
        if self.is_locked:
            return  # Do nothing if locked

        if self.selected_rectangle is not None:
            if event.keysym == "Left":
                self.move_rectangle(-self.cell_size, 0)
            elif event.keysym == "Right":
                self.move_rectangle(self.cell_size, 0)
            elif event.keysym == "Up":
                self.move_rectangle(0, -self.cell_size)
            elif event.keysym == "Down":
                self.move_rectangle(0, self.cell_size)
            elif event.keysym == "r":  # Rotate on 'r' key press
                self.rotate_rectangle()

    def move_rectangle(self, dx, dy):
        # Move the selected rectangle by dx and dy
        self.canvas.move(self.selected_rectangle, dx, dy)
        
        # Snap to grid
        self.snap_to_grid()

        # Update label position after moving rectangle
        for rectangle in self.rectangles:
            if rectangle[0] == self.selected_rectangle:
                width, height = rectangle[1]
                x1, y1 = self.canvas.coords(self.selected_rectangle)[:2]
                self.canvas.coords(rectangle[2], x1 + width * self.cell_size - 10, y1 + 10)  # Update label position

    def snap_to_grid(self):
        coords = self.canvas.coords(self.selected_rectangle)
        x1, y1, x2, y2 = coords
        
        # Calculate new snapped positions
        new_x1 = round(x1 / self.cell_size) * self.cell_size
        new_y1 = round(y1 / self.cell_size) * self.cell_size

        # Move to snapped positions
        self.canvas.move(self.selected_rectangle, new_x1 - x1, new_y1 - y1)

        # Update label position after snapping
        for rectangle in self.rectangles:
            if rectangle[0] == self.selected_rectangle:
                width, height = rectangle[1]
                self.canvas.coords(rectangle[2], new_x1 + width * self.cell_size - 10, new_y1 + 10)

    def rotate_rectangle(self):
        current_coords = self.canvas.coords(self.selected_rectangle)
        x1, y1, x2, y2 = current_coords
        width = (x2 - x1) / self.cell_size
        height = (y2 - y1) / self.cell_size

        # Swap width and height
        new_width = height
        new_height = width

        # Update rectangle coordinates
        self.canvas.coords(self.selected_rectangle, x1, y1, x1 + new_width * self.cell_size, y1 + new_height * self.cell_size)

        # Update label position after rotating
        for rectangle in self.rectangles:
            if rectangle[0] == self.selected_rectangle:
                self.canvas.coords(rectangle[2], x1 + new_width * self.cell_size - 10, y1 + 10)

    def lock_positions(self):
        self.is_locked = True  # Set the lock flag
        messagebox.showinfo("Locked", "You can no longer move the rectangles.")

    def toggle_highlight(self, label):
        rect_info = next((r for r in self.rectangles if chr(65 + self.rectangles.index(r)) == label), None)
        if rect_info:
            rect_id, (width, height), _ = rect_info
            coords = self.canvas.coords(rect_id)

            # Toggle the highlight
            button_state = self.buttons[label]['highlighted']
            if button_state:  # If currently highlighted, remove highlight
                self.remove_highlight(rect_id, coords)
                self.buttons[label]['highlighted'] = False
                self.buttons[label]['button'].config(relief=tk.RAISED)  # Button appears raised
            else:  # If not highlighted, add highlight
                self.add_highlight(rect_id, coords)
                self.buttons[label]['highlighted'] = True
                self.buttons[label]['button'].config(relief=tk.SUNKEN)  # Button appears sunken

            # Ensure labels remain visible
            for rectangle in self.rectangles:
                _, _, label_id = rectangle
                self.canvas.itemconfig(label_id, state=tk.NORMAL if not self.buttons[label]['highlighted'] else tk.VISIBLE)

    def toggle_outside_highlight(self, label):
        rect_info = next((r for r in self.rectangles if chr(65 + self.rectangles.index(r)) == label[0]), None)
        if rect_info:
            rect_id, (width, height), _ = rect_info
            coords = self.canvas.coords(rect_id)

            # Toggle the outside highlight
            button_state = self.buttons[label]['highlighted']
            if button_state:  # If currently highlighted, remove highlight
                self.remove_outside_highlight(coords)
                self.buttons[label]['highlighted'] = False
                self.buttons[label]['button'].config(relief=tk.RAISED)  # Button appears raised
            else:  # If not highlighted, add highlight
                self.add_outside_highlight(coords)
                self.buttons[label]['highlighted'] = True
                self.buttons[label]['button'].config(relief=tk.SUNKEN)  # Button appears sunken

    def add_highlight(self, rect_id, coords):
        # Highlight with a circle in the center of each cell within the rectangle
        x1, y1, x2, y2 = coords
        for i in range(self.rows):
            for j in range(self.cols):
                if x1 <= j * self.cell_size < x2 and y1 <= i * self.cell_size < y2:
                    center_x = j * self.cell_size + self.cell_size // 2
                    center_y = i * self.cell_size + self.cell_size // 2
                    self.canvas.create_oval(
                        center_x - 7, center_y - 7,
                        center_x + 7, center_y + 7,
                        fill="darkred", outline=""
                    )

        # Ensure the rectangle perimeter remains visible
        self.canvas.itemconfig(rect_id, outline="black", width=2)

    def remove_highlight(self, rect_id, coords):
        # Remove highlight circles from boxes inside the rectangle
        x1, y1, x2, y2 = coords
        for i in range(self.rows):
            for j in range(self.cols):
                if x1 <= j * self.cell_size < x2 and y1 <= i * self.cell_size < y2:
                    center_x = j * self.cell_size + self.cell_size // 2
                    center_y = i * self.cell_size + self.cell_size // 2
                    # Find the circles to delete
                    item = self.canvas.find_overlapping(center_x - 7, center_y - 7, center_x + 7, center_y + 7)
                    for circle in item:
                        if self.canvas.itemcget(circle, "fill") == "darkred":
                            self.canvas.delete(circle)

        # Ensure the rectangle perimeter remains visible
        self.canvas.itemconfig(rect_id, outline="black", width=5)

    def add_outside_highlight(self, coords):
        # Highlight with a circle in the center of each cell outside the rectangle
        x1, y1, x2, y2 = coords
        for i in range(self.rows):
            for j in range(self.cols):
                if not (x1 <= j * self.cell_size < x2 and y1 <= i * self.cell_size < y2):
                    center_x = j * self.cell_size + self.cell_size // 2
                    center_y = i * self.cell_size + self.cell_size // 2
                    self.canvas.create_oval(
                        center_x - 7, center_y - 7,
                        center_x + 7, center_y + 7,
                        fill="darkred", outline=""
                    )

    def remove_outside_highlight(self, coords):
        # Remove highlight circles from boxes outside the rectangle
        x1, y1, x2, y2 = coords
        for i in range(self.rows):
            for j in range(self.cols):
                if not (x1 <= j * self.cell_size < x2 and y1 <= i * self.cell_size < y2):
                    center_x = j * self.cell_size + self.cell_size // 2
                    center_y = i * self.cell_size + self.cell_size // 2
                    # Find the circles to delete
                    item = self.canvas.find_overlapping(center_x - 7, center_y - 7, center_x + 7, center_y + 7)
                    for circle in item:
                        if self.canvas.itemcget(circle, "fill") == "darkred":
                            self.canvas.delete(circle)

if __name__ == "__main__":
    root = tk.Tk()
    app = GridApp(root)
    root.mainloop() 