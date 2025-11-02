import math

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z        
        
    def __sub__(self, no):
        return Point(self.x - no.x, self.y - no.y, self.z - no.z)     
        
    def dot(self, no):
        return self.x * no.x + self.y * no.y + self.z * no.z
        
    def cross(self, no):
        return Point(
            self.y * no.z - self.z * no.y,
            self.z * no.x - self.x * no.z,
            self.x * no.y - self.y * no.x
        )
        
    def absolute(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

def plane_angle(a, b, c, d):
    AB = b - a
    BC = c - b
    CD = d - c
    X = AB.cross(BC)
    Y = BC.cross(CD)
    cos_phi = X.dot(Y) / (X.absolute() * Y.absolute())
    angle = round(math.degrees(math.acos(cos_phi)))
    return angle

if __name__ == '__main__':
    coord = []
    for i in range(4):
        coord.append(list(map(int, input().split())))
    A = Point(coord[0][0], coord[0][1], coord[0][2])
    B = Point(coord[1][0], coord[1][1], coord[1][2])
    C = Point(coord[2][0], coord[2][1], coord[2][2])
    D = Point(coord[3][0], coord[3][1], coord[3][2])
    print(plane_angle(A, B, C, D))