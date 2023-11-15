from model import *
import glm
from math import floor, ceil


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = list()
        self.d_reflector = None
        self.load()
        # skybox
        self.skybox = AdvancedSkyBox(app)
        # self.skybox = SkyBox(app)

    def add_object(self, obj, d_reflector=False):
        if not d_reflector:
            self.objects.append(obj)
        else:
            assert self.d_reflector is None, "Already have a dynamic reflector"
            self.d_reflector = obj

    def load(self):
        app = self.app
        add = self.add_object

        # floor
        n, s = 20, 2
        for x in range(-n, n, s):
            for z in range(-n, n, s):
                add(Cube(app, pos=(x, -s, z), tex_id=2 * ceil(((z / 2) / 2) % 2 - 0.5)))

        # # columns
        # for i in range(9):
        #     add(Cube(app, pos=(15, i * s, -11 + i), tex_id=2))
        #     add(Cube(app, pos=(15, i * s, 5 - i), tex_id=2))

        # cat
        # add(Cat(app, pos=(0, -1, -10), scale=(0.5, 0.5, 0.5)))
        # add(ShinyCat(app, pos=(0, -1, 10), rot=(-90, 180, 0), scale=(0.5, 0.5, 0.5)))
        add(Cat(app, pos=(0, -1, -10), scale=(1, 1, 1)))
        add(ShinyCat(app, pos=(0, -1, 10), rot=(-90, 180, 0), scale=(1, 1, 1)))

        # moving cube
        self.moving_cube = MovingCube(app, pos=(0, 6, 0), scale=(1, 1, 1), tex_id=1)
        add(self.moving_cube)

        add(ShinyCube(app, pos=(10, 10, 0), scale=(1, 1, 1)), d_reflector=True)

    def update(self):
        self.moving_cube.rot.xyz = self.app.time
