import os
import ursina


class Floor(ursina.Entity):
    def __init__(self):
        super().__init__(
            model="cube",
            texture=os.path.join("assets", "floor.png"),
            scale=(80, 0.1, 70),
            position=(0, 1, -1),
            collider="box"
        )

        self.texture.filtering = None