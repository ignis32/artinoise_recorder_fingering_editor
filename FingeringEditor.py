import tkinter as tk
from tkinter import ttk, filedialog, Canvas
from FingeringSystem import FingeringSystem, NoteVariations, NoteFingering
from FingeringViz import Flute, Hole, FluteForPrint
from tkinter import ttk, filedialog, Canvas, messagebox
import os
from PIL import Image, ImageDraw
import re

def sanitize_filename(filename):
    # Remove invalid characters for Windows and Linux
    sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '', filename)
    # Replace spaces with underscores if desired
    sanitized = sanitized.replace(' ', '_')
    # Avoid filenames that could be problematic in Windows
    reserved_names = {
        "CON", "PRN", "AUX", "NUL",
        "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
        "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
    }
    if sanitized.upper() in reserved_names or sanitized == '':
        sanitized = 'default'
    return sanitized

# Example usage
filename = "><>?*"
clean_filename = sanitize_filename(filename)
print(clean_filename)  # Output: default


class FingeringGUI:
    def __init__(self, master, fingering_system=None):
        # Initialization code...
 
        
        self.master = master
        self.fingering_system = fingering_system
        self.master.title("Fingering System Editor")

        # Menu for loading files
        self.menu = tk.Menu(master)
        self.master.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Export", command=self.save_file)
        self.file_menu.add_command(label="Print", command=self.print_fingerings)

        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=master.quit)

        self.label = ttk.Label(master, text="Select a Note:")
        self.label.grid(row=0, column=0, pady=10, sticky='nw')

        self.add_variation_button = ttk.Button(master, text="Add Variation", command=self.add_new_variation)
        self.add_variation_button.grid(row=3, column=0, padx=10, pady=10, sticky='nw')


       # Listbox for notes
        self.note_listbox = tk.Listbox(master, height=15, width=10, exportselection=False)
        self.note_listbox.grid(row=1, column=0, padx=2, pady=10, sticky='nsew')

        # Scrollbar for the Listbox
        self.scrollbar = tk.Scrollbar(master, orient="vertical")
        self.scrollbar.grid(row=1, column=0, sticky='ens')  # Ensure this column is free and right next to the Listbox

        # Configure the Listbox to interact with the Scrollbar
        self.note_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.note_listbox.yview)

        self.note_listbox.bind("<<ListboxSelect>>", self.update_fingering_display)



        # Label for showing the number of variations
        self.variations_label = ttk.Label(master, text="Variations: 0")
        self.variations_label.grid(row=2, column=0, padx=10, pady=10, sticky='nw')

        # Canvas for the flute visualization
        self.canvas = Canvas(master)
        self.canvas.grid(row=0, column=2, rowspan=2, padx=2, pady=20, sticky='nsew')

        # Grid configuration for resizing
        master.grid_rowconfigure(1, weight=1)  # Make the listbox row stretchable
        master.grid_columnconfigure(1, weight=1)  # Ensure the canvas also resizes
        
        self.system_name_label = ttk.Label(master, text="System Name:")
        self.system_name_label.grid(row=4, column=0, padx=10, pady=2, sticky='w')

        self.system_name_entry = ttk.Entry(master, width=20)
        self.system_name_entry.grid(row=5, column=0, padx=10, pady=2, sticky='we')
        
        # Create a blank row below the entry for bottom padding
        master.grid_rowconfigure(6, minsize=30)
        # Assuming 'fingering_system' is an object of FingeringSystem
        if fingering_system:
            self.load_fingering_system(fingering_system)
            self.update_all_list_item_colors()
        else:
            self.fingering_system = create_empty_fingering_system("Empty System")
            self.load_fingering_system(self.fingering_system)
            self.update_all_list_item_colors()  # Start the periodic update

        self.system_name_entry.insert(0, self.fingering_system.name)
        self.system_name_entry.bind("<FocusOut>", self.on_name_edit)

         # Label for displaying collisions
        self.collision_label = ttk.Label(master, text="", justify=tk.LEFT, foreground='red')
        self.collision_label.grid(row=1, column=3, padx=10, pady=10, sticky='ew')

        # Ensuring the label appears on the right side of the window
        master.grid_columnconfigure(2, weight=1)  # This makes column 2 expand and take extra space

        # Start the periodic check for fingering collisions
         

        self.check_fingering_collisions()
    
 

    def print_fingerings(self):
        img_directory = "img"
        os.makedirs(img_directory, exist_ok=True) 

        # A4 dimensions at 300 DPI
        a4_width = 2480
        a4_height = 3508
        base_flute_image_width = 340
        base_flute_image_height = 60

        # Count non-empty fingerings
        total_non_empty = sum(1 for note_variations in self.fingering_system.notes for fingering in note_variations.fingerings if not fingering.is_empty())
        if total_non_empty == 0:
            print("No non-empty fingerings to print.")
            return

        # Try different numbers of columns to find the best fit
        best_layout = (1, float('inf'))  # (scale_factor, number_of_columns)
        for columns in range(1, total_non_empty + 1):
            rows = (total_non_empty + columns - 1) // columns
            scale_factor_width = a4_width / (columns * base_flute_image_width)
            scale_factor_height = a4_height / (rows * base_flute_image_height)
            scale_factor = min(scale_factor_width, scale_factor_height)

            # Compare the area used by this layout to find the most efficient one
            if rows * base_flute_image_height * scale_factor < a4_height:
                best_layout = min(best_layout, (scale_factor, columns), key=lambda x: -x[0])

        # Determine the best number of columns and the corresponding scale factor
        scale_factor, columns = best_layout
        rows = (total_non_empty + columns - 1) // columns

        # Calculate final dimensions of each image
        final_image_width = int(base_flute_image_width * scale_factor)
        final_image_height = int(base_flute_image_height * scale_factor)

        # Create an A4 image with a white background
        a4_image = Image.new('RGB', (a4_width, a4_height), 'white')

        x_offset = 0
        y_offset = 0

        count = 0
        for note_variations in self.fingering_system.notes:
            for fingering in note_variations.fingerings:
                if not fingering.is_empty():
                    flute_image = FluteForPrint(fingering, note_variations.note).get_image()
                    resized_flute_image = flute_image.resize((final_image_width, final_image_height), Image.LANCZOS)
                    a4_image.paste(resized_flute_image, (x_offset, y_offset))
                    x_offset += final_image_width
                    count += 1
                    if count % columns == 0:
                        x_offset = 0
                        y_offset += final_image_height

        # Save the A4 image
        file_path = os.path.join("img", f"{sanitize_filename(self.fingering_system.name)}.png")
        a4_image.save(file_path)
        print(f"Saved all fingerings to {file_path}")




 

    def check_fingering_collisions(self):
        collisions = self.fingering_system.find_fingering_collisions()
        non_zero_variations = sum(1 for note in self.fingering_system.notes for fingering in note.fingerings if not fingering.is_empty())
        collision_text = f"Non-zero Variations: {non_zero_variations}  (max allowed 62)\n"
        collision_text += "\n".join([f"{', '.join(notes)} have the same fingering" for notes in collisions.values()])
        self.collision_label.config(text=collision_text)

        # Schedule the next check
        self.master.after(2000, self.check_fingering_collisions)  # checks every 2000 milliseconds (2 seconds)

    def on_name_edit(self, event=None):
        new_name = self.system_name_entry.get()
        self.fingering_system.update_name(new_name)
        print(f"Updated system name to {new_name}")
    
    def load_fingering_system(self, fingering_system):
        self.fingering_system = fingering_system
        self.note_listbox.delete(0, tk.END)

        # Update the system name entry with the loaded system's name
        self.system_name_entry.delete(0, tk.END)  # Clear the current text
        self.system_name_entry.insert(0, self.fingering_system.name)  # Insert the new system name

        for note_variation in fingering_system.notes:
            index = self.note_listbox.size()
            self.note_listbox.insert(tk.END, note_variation.note)
            # Check if all variations are empty
            if all(fingering.is_empty() for fingering in note_variation.fingerings):
                self.note_listbox.itemconfig(index, {'fg': 'grey'})
    def update_list_item_color(self, index):
        note_variations = self.fingering_system.notes[index]
        if all(fingering.is_empty() for fingering in note_variations.fingerings):
            self.note_listbox.itemconfig(index, {'fg': 'grey'})
        else:
            self.note_listbox.itemconfig(index, {'fg': 'black'})  # Default color
    
    def update_all_list_item_colors(self):
        print("UPDATE")
        for index, note_variation in enumerate(self.fingering_system.notes):
            if all(fingering.is_empty() for fingering in note_variation.fingerings):
                self.note_listbox.itemconfig(index, {'fg': 'grey'})
            else:
                self.note_listbox.itemconfig(index, {'fg': 'black'})
        # Schedule the next update
        self.master.after(1000, self.update_all_list_item_colors)  # updates every 1000 milliseconds (1 second)

   
    def save_file(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".arf",
            filetypes=[("ARF Files", "*.arf"), ("All Files", "*.*")],
            title="Save Fingering System As"
        )
        if filepath:
            self.fingering_system.save_to_file(filepath)
            print(f"System saved to {filepath}")

    def update_fingering_display(self, event=None):
        selection = self.note_listbox.curselection()
        if selection:
            index = selection[0]
            self.current_note = self.note_listbox.get(index)
            note_variations = self.fingering_system.find_note_fingering(self.current_note)
            self.variations_label.config(text=f"Variations: {len(note_variations.fingerings)}")
            self.draw_flute(note_variations)

    def draw_flute(self, note_variations):
        self.canvas.delete("all")  # Clear the canvas before drawing new fingerings
        y_offset = 0
        total_variations = len(note_variations.fingerings)
        for fingering in note_variations.fingerings:
            Flute(self.canvas, fingering, y_offset, self.delete_variation, total_variations)
            y_offset += 70

    def delete_variation(self, fingering):
        note_variations = self.fingering_system.find_note_fingering(self.current_note)
        if fingering in note_variations.fingerings:
            note_variations.fingerings.remove(fingering)
            self.update_fingering_display()  # Refresh the display after deletio

    def open_file(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("ARF Files", "*.arf"), ("All Files", "*.*")]
        )
        if filepath:
            new_fingering_system = FingeringSystem("Loaded System")
            new_fingering_system.load_from_file(filepath)
            self.load_fingering_system(new_fingering_system)
            self.canvas.delete('all')  # Clear canvas
    def add_new_variation(self):
        selection = self.note_listbox.curselection()
        if selection:
            index = selection[0]
            note_name = self.note_listbox.get(index)
            note_variations = self.fingering_system.find_note_fingering(note_name)
            if note_variations:
                # Create a new fingering with all holes set to 0 (closed)
                new_fingering = NoteFingering([0] * 10)  # Adjust the number based on the number of holes
                note_variations.add_fingering(new_fingering)
                self.update_fingering_display()  # Refresh the display
def create_empty_fingering_system(name):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    system = FingeringSystem(name)
    for octave in range(0, 11):  # Assuming you want from C0 to F#10
        for note in notes:
            note_name = f"{note}{octave}"
            if note == 'F#' and octave == 10:
                break
            fingering = NoteFingering([0] * 10)  # Adjust the number based on the number of holes
            variations = NoteVariations(note_name)
            variations.add_fingering(fingering)
            system.add_note_fingering(variations)
    return system
 

if __name__ == "__main__":
    root = tk.Tk()
    fingering_system = create_empty_fingering_system("Empty System")
    app = FingeringGUI(root, fingering_system)
    root.mainloop()
