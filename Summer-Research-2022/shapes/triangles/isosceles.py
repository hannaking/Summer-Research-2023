import math
from shapely.geometry import Point
from shapes.geometry import Geometry

DEFAULT_SIDE_LENGTH = 1

class Isosceles:
    def __init__(self, known_coords):
        self._points = known_coords

    def coordinatize(self):
        scenarios = []

        if None not in self._points:
            scenarios.append(self._points)
            return scenarios

        first_sort = [(i, p) for i, p in enumerate(self._points)]
        sorted_points = [b[1] for b in sorted(first_sort, key=lambda e: e[1] is None)]

        point1 = sorted_points[0]
        point2 = sorted_points[1]
        point3 = sorted_points[2]

        vertex_gluing = False

        if point2 is None:
            point2 = self.get_second_point(point1)
            vertex_gluing = True

        if point3 is None:
            third_points = self.get_third_points(point1, point2)

        for i in range(len(third_points)):
            scenarios.append([point1, point2, third_points[i]])

        if vertex_gluing:
            angles = [30, 45, 60, 90, 180, -30, -45, -60, -90]
            original_scenario_len = len(scenarios)
            for i in range(original_scenario_len):
                for angle in angles:
                    new_scenario = Geometry.rotate(scenarios[i], math.radians(angle), point1)
                    scenarios.append(new_scenario)

        for i, scenario in enumerate(scenarios):
            scenario = [b[1] for b in sorted(zip(first_sort, scenario), key=lambda e: e[0][0])]
            scenarios[i] = scenario

        return scenarios

    def get_second_point(self, point1):
        return Point(point1.x + DEFAULT_SIDE_LENGTH, point1.y)

    def get_third_points(self, point1, point2):
        side_length = Geometry.distance(point1, point2)
        third_points = []

        # Calculate the angles based on the desired isosceles triangle properties
        angles = [36, 72, 108, 144, 180, -36, -72, -108, -144]
        
        for angle in angles:
            third_points.append(Geometry.calculate_point_from_angle(math.radians(angle), point2, point1, side_length))
        
        return third_points

    def _verify_isosceles_triangle(self):
        if len(self._points) != 3:
            return False

        side1 = self._calculate_distance(self._points[0], self._points[1])
        side2 = self._calculate_distance(self._points[1], self._points[2])
        side3 = self._calculate_distance(self._points[2], self._points[0])

        if None in (side1, side2, side3):
            return False

        if math.isclose(side1, side2) or math.isclose(side2, side3) or math.isclose(side3, side1):
            if math.isclose(side1**2 + side2**2, side3**2) or math.isclose(side2**2 + side3**2, side1**2) or math.isclose(side3**2 + side1**2, side2**2):
                return True

        return False

    def _calculate_distance(self, point1, point2):
        if point1 is None or point2 is None:
            return None

        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
