# V1 Conditional Probability Calculator

This is the original version of my conditional probability calculator. It was built using Python and the `tkinter` library to create a local desktop GUI for exploring visual models of conditional probability.

This app uses `tkinter` to draw a customizable grid and display interactive rectangles representing probability events. The tool was designed to test basic ideas before developing more advanced web-based versions.

This version only runs locally and is meant as a basic prototype. There’s no web interface or persistent data storage.

---

## Project Description

The calculator creates a grid-based environment where users can place, move, and highlight rectangles to simulate conditional probability events. The project was designed to help visualize overlapping events (like A, B, and C) and their complements (A', B', C') on a defined grid.

---

## Key Features

- Custom grid creation by specifying rows and columns.
- Up to three rectangles (A, B, C) can be sized and randomly placed on the grid.
- Rectangles can be selected and moved using arrow keys, and they snap to the nearest grid position.
- Pressing `r` rotates the selected rectangle.
- A “Lock” button disables further movement to freeze rectangle positions.
- Highlight buttons let users display which cells fall inside or outside each rectangle using circles.

---

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/colburn-anderson/V1-Conditional-Probability-Calculator.git
   cd V1-Conditional-Probability-Calculator
