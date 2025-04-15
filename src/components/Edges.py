import pymunk


class Edges:
    def __init__(self, dimens, space):
        #defining edges as static polygons
        self.space = space
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = ((0, 0))
        self.shape = pymunk.Poly(self.body, dimens)
        self.shape.elasticity = 0.8

    def draw(self):
        #adding edges to screen
        self.space.add(self.body, self.shape)
