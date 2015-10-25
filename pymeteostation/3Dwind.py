# -*- coding: utf-8 -*-

import sys
from vispy import scene
from vispy.scene.visuals import Text

from colorsys import hsv_to_rgb
import numpy as np

canvas = scene.SceneCanvas(keys='interactive')
canvas.size = 1200, 600 

text_color = 'white'

N = 23

color = np.ones((N, 4), dtype=np.float32)
color[:, 0] = np.linspace(0, 1, N)
color[:, 1] = color[::-1, 0]

# This is the top-level widget that will hold three ViewBoxes, which will
# be automatically resized whenever the grid is resized.
grid = canvas.central_widget.add_grid()


# Create two ViewBoxes, place side-by-side
# First ViewBox uses a 2D pan/zoom camera
#box_temp = scene.widgets.ViewBox(name='vb1', border_color='yellow',
#                            parent=canvas.scene)
box_temp = grid.add_view(row=0, col=0)
box_temp.border_color = 'yellow'
box_temp.camera.rect = (-0.5, -5), (11, 10)
box_temp.border = (1, 0, 0, 1)

grid_temp = scene.visuals.GridLines(parent=box_temp.scene)

# Second ViewBox uses a 2D pan/zoom camera
#box_press = scene.widgets.ViewBox(name='vb1', border_color='yellow',
#                            parent=canvas.scene)
box_press = grid.add_view(row=1, col=0)
box_press.border_color = 'red'
box_press.camera.rect = (-10, -5), (15, 10)
box_press.border = (1, 1, 1, 1)

grid_press = scene.visuals.GridLines(parent=box_press.scene)

# Third ViewBox uses a 3D orthographic camera
#box_wind = scene.widgets.ViewBox(name='vb2', border_color='blue',
#                            parent=canvas.scene)
box_wind = grid.add_view(row=0, col=1, row_span = 2 )
box_wind.border_color = 'blue'
box_wind.border = (1, 0, 0, 1)
box_wind.camera.rect = (-5, -5), (10, 10)
box_wind.set_camera('turntable',
                        mode='ortho',
                        elevation=0, 
                        azimuth=0, 
                        up='y',
                        distance=10)

#l2 = scene.visuals.Tube(axis,
#                        color=['red', 'green', 'blue'],
#                        shading='smooth',
#                        tube_points=8,
#                        parent=box_wind)


wind_vectors = scene.visuals.Line(
                        connect='segments',
                        color=color,
                        mode='gl',
                        width=5,
                        antialias=True,
                        parent= box_wind.scene)
wind_vectors.transform = scene.transforms.PolarTransform()

visual_wind_title = scene.visuals.Text(text = 'Wind parameters',
                                            color = text_color, 
                                            pos = (0,5), 
                                            font_size = 30,
                                            parent=box_wind.scene)

visual_wind_direction = scene.visuals.Text(text = 'Wind direction',
                                                color = text_color,
                                                pos = (-3,-5),
                                                font_size = 20,
                                                parent=box_wind.scene)

visual_wind_speed = scene.visuals.Text(text = 'Wind speed',
                                            color = text_color,
                                            pos = (3,-5),
                                            font_size = 20,
                                            parent=box_wind.scene)

visual_temperature = scene.visuals.Text(text = 'Air temperature:',
                                            color = text_color,
                                            pos = (0.2,0.5),
                                            font_size = 12,
                                            parent = box_temp.scene)

#visual_temp_graph = scene.visuals.Line(pos=Air_temperature, color='blue', antialias=True,        width=1,mode='gl', parent=box_temp.scene)
visual_temp_graph = scene.visuals.Line(color=color,
                                            mode='gl',
                                            antialias=False,
                                            name='line1',
                                            parent=box_temp.scene)

visual_QFE = scene.visuals.Text(text = 'QFE:',
                                    color = text_color,
                                    pos = (0.3,0.4),
                                    font_size = 12,
                                    parent=box_press.scene)

visual_QNH = scene.visuals.Text(text = 'QNH:',
                                    color = text_color,
                                    pos = (0.3,0.3),
                                    font_size = 12,
                                    parent=box_press.scene)
canvas.show()

timer = app.Timer(connect=redraw())
timer.start(0.016)

def redraw(self):

    #points = np.random.rand(30,2)
    points = WAD_wind[:,[0,2]]
    points[:,[0, 1]] = points[:,[1, 0]]

    #points = np.multiply(points, [360,1])
    time = np.split(np.linspace(0.0, 10.0, num=points.shape[0]),points.shape[0])
    points = np.hstack((points,time))

    center_points = np.zeros((points.shape[0],2))
    center_points = np.hstack((center_points,time))
    lines = np.empty((points.shape[0]+center_points.shape[0],points.shape[1]))
    lines[::2,:] = points
    lines[1::2,:] = center_points
    lines[1::2,:] = center_points

#       self.wind_vectors.pos= lines
    axis=np.array([[0,0,0],[0,0,1]])




    self.visual_temperature.text = 'Air temperature: %s °C' % float(Air_temperature[Air_temperature.shape[0]-1])

    pos = np.empty((self.N, 2), np.float32)
    pos[:, 0] = np.linspace(-1., 1., self.N)
    pos[:, 1] = np.random.normal(0.0, 0.5, size=self.N)
    pos[:20, 1] = -0.5  # So we can see which side is down


    self.visual_QFE.text = 'QFE: %s hPa' % float(QFE[QFE.shape[0]-1])

    self.visual_QNH.text = 'QNH: %s hPa' % float(QNH[QNH.shape[0]-1])


if __name__ == '__main__':
    win = Canvas()
    import sys
    if sys.flags.interactive != 1:
        app.run()
