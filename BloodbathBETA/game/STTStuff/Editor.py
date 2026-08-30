import tkinter as tk
from tkinter import filedialog, messagebox


# ============================================================
# SETTINGS
# ============================================================

GRID_WIDTH = 40
GRID_HEIGHT = 35
CELL_SIZE = 20

EMPTY = "0"
WALL = "1"
SPAWN = "S"


# ============================================================
# EDITOR
# ============================================================

class MapEditor:

    def __init__(self, root):
        self.root = root
        self.root.title("Ursina FPS Map Editor")

        self.current_tool = WALL

        # Create map
        self.map_data = [
            [EMPTY for _ in range(GRID_WIDTH)]
            for _ in range(GRID_HEIGHT)
        ]

        # Default spawn
        self.spawn_x = GRID_WIDTH // 2
        self.spawn_y = GRID_HEIGHT // 2
        self.map_data[self.spawn_y][self.spawn_x] = SPAWN

        # ----------------------------------------------------
        # Toolbar
        # ----------------------------------------------------

        toolbar = tk.Frame(root)
        toolbar.pack(fill="x")

        tk.Button(
            toolbar,
            text="Wall",
            command=lambda: self.set_tool(WALL)
        ).pack(side="left")

        tk.Button(
            toolbar,
            text="Erase",
            command=lambda: self.set_tool(EMPTY)
        ).pack(side="left")

        tk.Button(
            toolbar,
            text="Spawn",
            command=lambda: self.set_tool(SPAWN)
        ).pack(side="left")

        tk.Button(
            toolbar,
            text="Clear",
            command=self.clear_map
        ).pack(side="left")

        tk.Button(
            toolbar,
            text="Save",
            command=self.save_map
        ).pack(side="left")

        tk.Button(
            toolbar,
            text="Load",
            command=self.load_map
        ).pack(side="left")

        self.tool_label = tk.Label(
            toolbar,
            text="Tool: Wall"
        )

        self.tool_label.pack(side="right")

        # ----------------------------------------------------
        # Canvas
        # ----------------------------------------------------

        self.canvas = tk.Canvas(
            root,
            width=GRID_WIDTH * CELL_SIZE,
            height=GRID_HEIGHT * CELL_SIZE,
            bg="white"
        )

        self.canvas.pack()

        self.canvas.bind(
            "<Button-1>",
            self.left_click
        )

        self.canvas.bind(
            "<Button-3>",
            self.erase_click
        )

        self.canvas.bind(
            "<B1-Motion>",
            self.left_click
        )

        self.draw_grid()

    # ========================================================
    # TOOLS
    # ========================================================

    def set_tool(self, tool):
        self.current_tool = tool

        if tool == WALL:
            self.tool_label.config(text="Tool: Wall")

        elif tool == EMPTY:
            self.tool_label.config(text="Tool: Erase")

        elif tool == SPAWN:
            self.tool_label.config(text="Tool: Spawn")

    # ========================================================
    # DRAW
    # ========================================================

    def draw_grid(self):

        self.canvas.delete("all")

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):

                value = self.map_data[y][x]

                x1 = x * CELL_SIZE
                y1 = y * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                if value == WALL:
                    fill = "black"

                elif value == SPAWN:
                    fill = "green"

                else:
                    fill = "white"

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=fill,
                    outline="gray"
                )

                if value == SPAWN:
                    self.canvas.create_text(
                        x1 + CELL_SIZE // 2,
                        y1 + CELL_SIZE // 2,
                        text="S",
                        fill="white",
                        font=("Arial", 10, "bold")
                    )

    # ========================================================
    # MOUSE
    # ========================================================

    def get_cell(self, event):

        x = event.x // CELL_SIZE
        y = event.y // CELL_SIZE

        if x < 0 or x >= GRID_WIDTH:
            return None

        if y < 0 or y >= GRID_HEIGHT:
            return None

        return x, y

    def left_click(self, event):

        cell = self.get_cell(event)

        if cell is None:
            return

        x, y = cell

        # Spawn tool
        if self.current_tool == SPAWN:

            # Remove old spawn
            for row in range(GRID_HEIGHT):
                for col in range(GRID_WIDTH):
                    if self.map_data[row][col] == SPAWN:
                        self.map_data[row][col] = EMPTY

            self.map_data[y][x] = SPAWN

        else:
            self.map_data[y][x] = self.current_tool

        self.draw_grid()

    def erase_click(self, event):

        cell = self.get_cell(event)

        if cell is None:
            return

        x, y = cell

        self.map_data[y][x] = EMPTY

        self.draw_grid()

    # ========================================================
    # CLEAR
    # ========================================================

    def clear_map(self):

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                self.map_data[y][x] = EMPTY

        self.map_data[
            GRID_HEIGHT // 2
        ][
            GRID_WIDTH // 2
        ] = SPAWN

        self.draw_grid()

    # ========================================================
    # SAVE
    # ========================================================

    def save_map(self):

        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Map files", "*.txt"),
                ("All files", "*.*")
            ]
        )

        if not path:
            return

        with open(path, "w") as file:

            for row in self.map_data:
                file.write("".join(row) + "\n")

        messagebox.showinfo(
            "Saved",
            "Map saved successfully!"
        )

    # ========================================================
    # LOAD
    # ========================================================

    def load_map(self):

        path = filedialog.askopenfilename(
            filetypes=[
                ("Map files", "*.txt"),
                ("All files", "*.*")
            ]
        )

        if not path:
            return

        with open(path, "r") as file:
            lines = [
                line.strip()
                for line in file
                if line.strip()
            ]

        if len(lines) != GRID_HEIGHT:
            messagebox.showerror(
                "Error",
                "Map has the wrong height."
            )
            return

        for y in range(GRID_HEIGHT):

            if len(lines[y]) != GRID_WIDTH:
                messagebox.showerror(
                    "Error",
                    f"Row {y} has the wrong width."
                )
                return

            for x in range(GRID_WIDTH):

                value = lines[y][x]

                if value not in ("0", "1", "S"):
                    messagebox.showerror(
                        "Error",
                        f"Invalid character '{value}'."
                    )
                    return

                self.map_data[y][x] = value

        self.draw_grid()


# ============================================================
# START
# ============================================================

root = tk.Tk()

editor = MapEditor(root)

root.mainloop()