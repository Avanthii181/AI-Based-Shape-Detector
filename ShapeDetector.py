import tkinter as tk
import math

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Drawing Generator")

        # Create a canvas for the user to draw
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.canvas.pack()

        # Buttons to generate and clear drawings
        self.button_clear = tk.Button(self.root, text="Clear Drawing", command=self.clear_canvas)
        self.button_clear.pack(pady=10)

        # Store the coordinates of the drawing points
        self.drawing_points = []

        # Bind mouse motion to draw on the canvas
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.analyze_drawing)

    def draw(self, event):
        """Allow the user to draw on the canvas"""
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        self.canvas.create_oval(x1, y1, x2, y2, fill="black", width=2)
        self.drawing_points.append((event.x, event.y))  # Save points for analysis

    def analyze_drawing(self, event):
        """Analyze the drawn shape to identify basic shapes"""
        if len(self.drawing_points) < 5:  # If drawing is too small, don't analyze
            return

        # Detect a circle (simple approximation)
        if self.is_circle():
            self.canvas.create_text(200, 375, text="Detected: Circle", fill="blue", font=("Arial", 12))
        # Detect a square (simple approximation)
        elif self.is_square():
            self.canvas.create_text(200, 375, text="Detected: Square", fill="blue", font=("Arial", 12))
        else:
            self.canvas.create_text(200, 375, text="Shape not recognized", fill="red", font=("Arial", 12))

        # Reset drawing points after analysis
        self.drawing_points = []

    def is_circle(self):
        """Check if the drawing approximates a circle"""
        # Approximate by checking if the distances between points are relatively equal
        distances = []
        for i in range(1, len(self.drawing_points)):
            x1, y1 = self.drawing_points[i - 1]
            x2, y2 = self.drawing_points[i]
            distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            distances.append(distance)

        # Check if all distances are close to each other (tolerance for circular shape)
        avg_distance = sum(distances) / len(distances)
        tolerance = 5  # Allow some tolerance in distance
        if all(abs(d - avg_distance) < tolerance for d in distances):
            return True
        return False

    def is_square(self):
        """Check if the drawing approximates a square"""
        if len(self.drawing_points) < 4:
            return False  # Not enough points to form a square

        # Get the distances between consecutive points (assuming they form a closed shape)
        distances = []
        for i in range(1, len(self.drawing_points)):
            x1, y1 = self.drawing_points[i - 1]
            x2, y2 = self.drawing_points[i]
            distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            distances.append(distance)

        # Close the shape by adding distance between last and first point
        x1, y1 = self.drawing_points[-1]
        x2, y2 = self.drawing_points[0]
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        distances.append(distance)

        # Check if all distances are roughly equal
        avg_distance = sum(distances) / len(distances)
        tolerance = 10  # Allow some tolerance in side lengths
        if all(abs(d - avg_distance) < tolerance for d in distances):
            # Check if there are 4 points with roughly equal distances (for square)
            return True
        return False

    def clear_canvas(self):
        """Clear the canvas to start a new drawing"""
        self.canvas.delete("all")
        self.drawing_points = []  # Reset drawing points

    def run(self):
        """Run the application"""
        self.root.mainloop()


# Create the main Tkinter window
root = tk.Tk()
app = DrawingApp(root)
app.run()
