from model import *
import glm


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = list()
        self.d_reflector = None
        self.load()
        # skybox
        self.skybox = AdvancedSkyBox(app)

    def add_object(self, obj, d_reflector=False):
        if not d_reflector:
            self.objects.append(obj)
        else:
            assert self.d_reflector is None, "Already have a dynamic reflector"
            self.d_reflector = obj

    def load(self):
        app = self.app
        add = self.add_object

        # # floor
        # n, s = 20, 2
        # for x in range(-n, n, s):
        #     for z in range(-n, n, s):
        #         add(Cube(app, pos=(x, -s, z)))
        #
        # # columns
        # for i in range(9):
        #     add(Cube(app, pos=(15, i * s, -9 + i), tex_id=2))
        #     add(Cube(app, pos=(15, i * s, 5 - i), tex_id=2))

        # cat
        add(Cat(app, pos=(0, -1, -15)))
        add(ShinyCat(app, pos=(0, -1, 15), rot=(-90, 180, 0)), d_reflector=True)
        self.app.camera_cube.position = (0, -1, 15)

        # moving cube
        self.moving_cube = MovingCube(app, pos=(0, 6, 0), scale=(1, 1, 1), tex_id=1)
        add(self.moving_cube)

        add(ShinyCube(app, pos=(0, -6, 0)))

    def update(self):
        self.moving_cube.rot.xyz = self.app.time
