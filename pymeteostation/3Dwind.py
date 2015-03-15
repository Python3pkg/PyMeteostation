# -*- coding: utf-8 -*-
import sys
import os
import numpy as np

statinfo = os.stat('./minicom.log')
f = open('./minicom.log', 'rb')
msg = ["" for x in range(1000)]
msg_index = 0

WAD_wind = np.zeros((1,3))
Air_temperature = np.zeros((1,1))
QFE = np.zeros((1,1))
QNH = np.zeros((1,1))

def process_data(threadName, q):
    while not exitFlag:
        for b in range(statinfo.st_size):
            f.seek(b)
            byte = f.read(1)
            if ord(byte) == 0x1E:
                msg = f.read(9)

                if msg[0] == 'A':                    # Analog input 
                    a = msg[1:7]
                    if a == '    --':
                        a = float('NaN')
                    else:
                        a = int(a)/10.0
                    sys.stdout.write(" Temperature: %3.1f C\n" % (a))
                    Air_temperature = np.append(Air_temperature,[[a]], axis=0)

                elif msg[0] == 'B':                    # Analog input 
                    b = int(msg[1:7])/10.0
                    sys.stdout.write(" Pressure: %3.1f hPa \n" % (b))
                elif msg[0] == 'C':                    # Analog input 
                    c = int(msg[1:7])/10.0
                    sys.stdout.write(" QFE: %4.1f hPa\n" % (c))
                    QFE = np.append(QFE,[[c]], axis=0)

                elif msg[0] == 'D':                    # Analog input 
                    d = int(msg[1:7])/10.0
                    sys.stdout.write(" QNH: %4.1f hPa\n" % (d))
                    QNH = np.append(QNH,[[d]], axis=0)
                    
                elif msg[0] == 'E':                    # precipitation input
                    precipitation = int(msg[1:7])
                    
                elif msg[0] == 'G':                    # wind speed and direction
                    wind_direction =  int(msg[1:3]) * 10
                    wind_speed =  int(msg[3:7])/10.0
                    wind = (wind_speed), (wind_direction)
                    sys.stdout.write(" Windspeed: %3.1f kt Winddirection: %d \n" % (wind_speed,wind_direction))
                    
                elif msg[0] == 'H':                    # wind speed and direction (2 minutes sliding average)
                    wind_direction =  int(msg[1:3]) * 10
                    wind_speed =  int(msg[3:7])/10.0
                    wind_2min = (wind_speed), (wind_direction)
                    sys.stdout.write(" Windspeed: %3.1f kt Winddirection: %d  2 minutes average \n" % (wind_speed,wind_direction))

                elif msg[0] == 'I':                    # wind speed and direction (10 minutes sliding average)
                    wind_direction =  int(msg[1:3])* 10
                    wind_speed =  int(msg[3:7])/10.0
                    wind_10min = (wind_speed), (wind_direction )
                    sys.stdout.write(" Windspeed: %3.1f kt Direction: %d knots 10 minutes average.\n" % (wind_speed,wind_direction))

                elif msg[0] == 'L':                    # Dewpoint temperature
                    dewpoint = msg[1:7]
                    if dewpoint == '    --':
                        dewpoint = float('NaN')
                    else:
                        dewpoint = int(dewpoint)/10.0
                    sys.stdout.write(" Dewpoint: %3.1f \n" % (dewpoint))

                elif msg[0] == 'M':                    # 3hours pressure trend
                    pressure_3h = int(msg[1:7])/10.0
                    sys.stdout.write(" Pressure %4.1f hPa 3 hours trend.\n" % (pressure_3h))

                elif msg[0] == 'Q':                    # power status in % (0-100% is internal power capacity) if external power supply present value is greater than 100
                    power = int(msg[1:7])
                    sys.stdout.write(" Power %d \% \n" % (power))

                elif msg[0] == 'R':                    # alarm or relay status
                    alarm = int(msg[1:7])
                    sys.stdout.write(" Alarm status %d \n" % (alarm))

                elif msg[0] == 'S':                    # atmospheric stability
                    atmosphere_stability = int(msg[1:7])
                    sys.stdout.write(" Atmospheric stability  %d \n" % (atmosphere_stability))

                elif msg[0] == 'W':                    # WAD software special format
                    wind_direction = 10*(16*(ord(msg[1]) & 0x0F) + (ord(msg[2]) & 0x0F))
                    wind_speed =  256*(16*(ord(msg[3]) & 0x0F) + (ord(msg[4]) & 0x0F)) + 16*(ord(msg[5]) & 0x0F) + (ord(msg[6]) & 0x0F)
                    wind_speed_ms = wind_speed / 37.38932004
                    wind_speed_kt = wind_speed_ms * 1.943844492
                    WAD_wind = np.append(WAD_wind,[[wind_speed_ms, wind_speed_kt, wind_direction]], axis=0)
                    sys.stdout.write(" WAD Winddirection %d %3.1f m/s %3.1f kt \n" % (wind_direction, wind_speed_ms, wind_speed_kt))

                elif msg[0] == 'X':                    # WAD software special format 2 minutes average
                    wind_WAD_2min = msg[1:7]
                    sys.stdout.write(" WAD %s 2min\n" % (wind_WAD_2min))

                elif msg[0] == 'Y':                    # WAD software special format 10 minutes average
                    wind_WAD_10min = msg[1:7]
                    sys.stdout.write(" WAD %s 10min\n" % (wind_WAD_10min))                
        f.close()



import sys
from vispy import app
from vispy import scene
from vispy.geometry.torusknot import TorusKnot

from colorsys import hsv_to_rgb
import numpy as np


class Canvas(scene.SceneCanvas):
    def __init__(self):
        self.canvas = scene.SceneCanvas(keys='interactive')
        self.canvas.size = 1200, 600 
        
        self.text_color = 'white'

        self.N = 23

        self.color = np.ones((self.N, 4), dtype=np.float32)
        self.color[:, 0] = np.linspace(0, 1, self.N)
        self.color[:, 1] = self.color[::-1, 0]

        # This is the top-level widget that will hold three ViewBoxes, which will
        # be automatically resized whenever the grid is resized.
        self.grid = self.canvas.central_widget.add_grid()


        # Create two ViewBoxes, place side-by-side
        # First ViewBox uses a 2D pan/zoom camera
        #box_temp = scene.widgets.ViewBox(name='vb1', border_color='yellow',
        #                            parent=canvas.scene)
        self.box_temp = self.grid.add_view(row=0, col=0)
        self.box_temp.border_color = 'yellow'
        self.box_temp.camera.rect = (-0.5, -5), (11, 10)
        self.box_temp.border = (1, 0, 0, 1)

        self.grid_temp = scene.visuals.GridLines(parent=self.box_temp.scene)

        # Second ViewBox uses a 2D pan/zoom camera
        #box_press = scene.widgets.ViewBox(name='vb1', border_color='yellow',
        #                            parent=canvas.scene)
        self.box_press = self.grid.add_view(row=1, col=0)
        self.box_press.border_color = 'red'
        self.box_press.camera.rect = (-10, -5), (15, 10)
        self.box_press.border = (1, 1, 1, 1)

        self.grid_press = scene.visuals.GridLines(parent=self.box_press.scene)

        # Third ViewBox uses a 3D orthographic camera
        #box_wind = scene.widgets.ViewBox(name='vb2', border_color='blue',
        #                            parent=canvas.scene)
        self.box_wind = self.grid.add_view(row=0, col=1, row_span = 2 )
        self.box_wind.border_color = 'blue'
        self.box_wind.border = (1, 0, 0, 1)
        self.box_wind.camera.rect = (-5, -5), (10, 10)
        self.box_wind.set_camera('turntable',
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


        self.wind_vectors = scene.visuals.Line(
                                connect='segments',
                                color=self.color,
                                mode='gl',
                                width=5,
                                antialias=True,
                                parent= self.box_wind.scene)
        self.wind_vectors.transform = scene.transforms.PolarTransform()

        self.visual_wind_title = scene.visuals.Text(text = 'Wind parameters',
                                                    color = self.text_color, 
                                                    pos = (0,5), 
                                                    font_size = 30,
                                                    parent=self.box_wind.scene)

        self.visual_wind_direction = scene.visuals.Text(text = 'Wind direction',
                                                        color = self.text_color,
                                                        pos = (-3,-5),
                                                        font_size = 20,
                                                        parent=self.box_wind.scene)

        self.visual_wind_speed = scene.visuals.Text(text = 'Wind speed',
                                                    color = self.text_color,
                                                    pos = (3,-5),
                                                    font_size = 20,
                                                    parent=self.box_wind.scene)

        self.visual_temperature = scene.visuals.Text(text = 'Air temperature:',
                                                    color = self.text_color,
                                                    pos = (0.2,0.5),
                                                    font_size = 12,
                                                    parent = self.box_temp.scene)

        #visual_temp_graph = scene.visuals.Line(pos=Air_temperature, color='blue', antialias=True,        width=1,mode='gl', parent=box_temp.scene)
        self.visual_temp_graph = scene.visuals.Line(color=self.color,
                                                    mode='gl',
                                                    antialias=False,
                                                    name='line1',
                                                    parent=self.box_temp.scene)

        self.visual_QFE = scene.visuals.Text(text = 'QFE:',
                                            color = self.text_color,
                                            pos = (0.3,0.4),
                                            font_size = 12,
                                            parent=self.box_press.scene)

        self.visual_QNH = scene.visuals.Text(text = 'QNH:',
                                            color = self.text_color,
                                            pos = (0.3,0.3),
                                            font_size = 12,
                                            parent=self.box_press.scene)
        self.canvas.show()

        self.timer = app.Timer(connect=self.redraw())
        self.timer.start(0.016)

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
