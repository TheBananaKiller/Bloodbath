import os
import ursina


class Wall(ursina.Entity):
    def __init__(self, position):
        super().__init__(
            position=position,
            scale=2,
            model="cube",
            texture=os.path.join("assets", "wall.png"),
            origin_y=-0.5
        )

        self.texture.filtering = None
        self.collider = ursina.BoxCollider(
            self,
            size=ursina.Vec3(1, 2, 1)
        )


class Map:
    def __init__(self):

        with open("map.txt", "r") as file:
            map_data = [
                line.strip()
                for line in file
                if line.strip()
            ]

        self.spawn_position = ursina.Vec3(0, 1, 0)

        for z, row in enumerate(map_data):

            for x, cell in enumerate(row):

                world_x = x * 2 - 40
                world_z = z * 2 - 35

                if cell == "1":

                    Wall(
                        ursina.Vec3(
                            world_x,
                            1,
                            world_z
                        )
                    )

                    Wall(
                        ursina.Vec3(
                            world_x,
                            3,
                            world_z
                        )
                    )

                elif cell == "S":

                    self.spawn_position = ursina.Vec3(
                        world_x,
                        1,
                        world_z
                    )