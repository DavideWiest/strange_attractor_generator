from modules.coordinatesgenerator import CoordinatesGenerator, normalizeCoordinates
from modules.singulargrahvisualizer import SingularGraphVisualizer

# lambda_x = lambda x,y,z: x+0.01*y-0.02*z
# lambda_y = lambda x,y,z: x-y+z
# lambda_z = lambda x,y,z: x+y+z

lambda_x = lambda a,b: -0.772*a-1.008-0.569*b+0.831
lambda_y = lambda a,b: -0.067*a+0.276+1.261

if __name__ == "__main__":
    # gen = CoordinatesGenerator((lambda_x, lambda_x, lambda_z), (3,1,5))
    gen = CoordinatesGenerator((lambda_x, lambda_x), (0,0))

    coordinates = gen.generatePointsAsNumpyArray(200)
    coordinates = normalizeCoordinates(coordinates)

    visSettings = {}
    vis = SingularGraphVisualizer(visSettings)
    # vis.drawCoordinates3D(coordinates)
    vis.drawCoordinates2D(coordinates)
    vis.show()

