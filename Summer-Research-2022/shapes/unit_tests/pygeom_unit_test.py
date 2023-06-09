import unittest
import sys

sys.path.insert(0, './Summer-Research-2022/')

from pygeom import Axes, Polygon, Point
from lattice import Lattice

from shapes.shape_factory import Shape

class TestPygeom(unittest.TestCase):
    def test_draw_plane(self):
        plane = Axes()
        plane = Axes(xlim=(-5,5), ylim=(-5,5), figsize=(9,8))
        plane.draw()

    def test_draw_triangle(self):
        triangle = Polygon([Point(0,0), Point(1,0), Point(0,1)])
        plane = Axes()
        plane = Axes(xlim=(-5,5), ylim=(-5,5), figsize=(9,8))

        plane.add(triangle)

        plane.draw()

    def test_draw_two_triangles(self):
        triangle1 = Polygon([Point(0,0), Point(1,0), Point(0,1)])
        triangle2 = Polygon([Point(1,1), Point(2,1), Point(1,2)])
        plane = Axes()
        plane = Axes(xlim=(-5,5), ylim=(-5,5), figsize=(9,8))

        plane.add(triangle1)
        plane.add(triangle2)

        plane.draw()

    def test_draw_triangle_lattice(self):
        t1 = Lattice(3)
        plane = Axes()
        plane = Axes(xlim=(-5,5), ylim=(-5,5))

if __name__ == "__main__":
    unittest.main()