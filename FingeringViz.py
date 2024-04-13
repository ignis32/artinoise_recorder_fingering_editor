import tkinter as tk
class Hole:
    def __init__(self, canvas, x, y, state, callback, is_octave=False, small=False):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.state = state
        self.callback = callback
        self.is_octave = is_octave
        self.small = small
        self.id = []
        self.draw()

    def draw(self):
        radius = 5 if self.small else 9
        y_offset = 15 if self.is_octave else 0
        # Clear existing canvas items for this hole
        for item in self.id:
            self.canvas.delete(item)
        self.id.clear()

        if self.state == 1:  # Semi-open
            self.id.append(self.canvas.create_arc(self.x-radius, self.y-radius+y_offset, self.x+radius, self.y+radius+y_offset, start=90, extent=180, fill="black"))
            self.id.append(self.canvas.create_arc(self.x-radius, self.y-radius+y_offset, self.x+radius, self.y+radius+y_offset, start=270, extent=180, fill="white"))
        else:
            color = "white" if self.state == 0 else "black"
            self.id.append(self.canvas.create_oval(self.x-radius, self.y-radius+y_offset, self.x+radius, self.y+radius+y_offset, fill=color))

        # Rebind events to new canvas items
        self.bind_events()

    def bind_events(self):
        # Bind a click event to all parts of the hole
        for item in self.id:
            self.canvas.tag_bind(item, "<Button-1>", self.on_click)

    def on_click(self, event):
        self.toggle()
        print(f"Hole clicked: Position ({self.x}, {self.y}), State: {self.state}")

    def toggle(self):
        if self.is_octave:
            self.state = (self.state + 1) % 3  # Octave hole toggles between 0, 1, and 2
        else:
            self.state = 2 if self.state == 0 else 0  # Non-octave holes toggle between 0 and 2
        self.draw()
        self.callback(self)  # Execute the callback to handle the state change

class Flute:
    def __init__(self, canvas, fingering, y_offset, delete_callback,total_variations):
        self.canvas = canvas
        self.fingering = fingering
        self.holes = []
        self.y_offset = y_offset
        self.total_variations = total_variations  # Total variations count, required to prevent deleting the last one
        self.delete_callback = delete_callback
        self.draw_flute()
        
    
    def delete_variation(self):
        # This function will be implemented in the GUI class
        pass

    def draw_flute(self):
        base_y = 50 + self.y_offset  # Adjust vertical position based on offset
        self.canvas.create_rectangle(20, base_y - 30, 340, base_y + 30, outline="grey")  # Drawing a rectangle around each variation

        for i, state in enumerate(self.fingering.holes):
            x = 30 + i * 30
            y = base_y
            is_octave = (i == 0)
            if is_octave:
                y += 5  # Octave hole is positioned below the others
                x += 30 +15  # Center the octave hole slightly to the right for visual balance

            small = (i in [7, 9])
            if small:
                y -= 14  # Small holes moved up
                x += 3


            # moving small holes to be above their big neighbor
            if i == 7:
                x-=  30   
            if i == 9:
                x-= 30 +30

            # compensating for 7th  being small
            if i == 8:
                x -=30

            hole = Hole(self.canvas, x, y, state, self.hole_updated, is_octave=is_octave, small=small)
            self.holes.append(hole)

             # Draw the delete button
            if self.total_variations > 1:
                btn_delete = tk.Button(self.canvas, text="Delete", command=lambda: self.delete_callback(self.fingering))
                btn_delete_window = self.canvas.create_window(350, base_y, window=btn_delete, anchor='nw')


        # Optionally, draw a vertical dividing line between holes 3 and 4
        divide_x = 30 + 3 * 30 + 15  # Halfway between holes 3 and 4
        self.canvas.create_line(divide_x, base_y - 20, divide_x, base_y + 20, fill='grey', width=2)

        

    def hole_updated(self, hole):
        index = self.holes.index(hole)
        self.fingering.holes[index] = hole.state
