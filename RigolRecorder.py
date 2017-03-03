from pyqtgraph.Qt import QtGui, QtCore
from PyQt5.QtCore import pyqtSlot
import pyqtgraph as pg
from datetime import datetime
import numpy as np
import instruments
import RigolRecorderGUI as gui




# scope = instruments.BM857(comport='COM22')

# QtGui.QApplication.setGraphicsSystem('raster')
app = QtGui.QApplication([])

# mw = QtGui.QMainWindow()

mw = gui.Ui_MainWindow()
mw.setupUi(mw)

mw.show()

mw.setWindowTitle('Rigol Recorder')




pw = pg.PlotWidget(name='Plot1')  ## giving the plots names allows us to link their axes together

mw.gridLayout_2.addWidget(pw, 0, 4, 2, 1)

## Create an empty plot curve to be filled later, set its pen
p1 = pw.plot()
p1.setPen((20, 200, 50))



## Add in some extra graphics
# rect = QtGui.QGraphicsRectItem(QtCore.QRectF(0, 0, 1, 5e-11))
# rect.setPen(pg.mkPen(100, 200, 100))
# pw.addItem(rect)
pw.setTitle('Rigol Recorder')
pw.setLabel('left', 'Value', units='V')
pw.setLabel('bottom', 'Time', units='s')

# pw.setXRange(0, 1400)
# pw.setYRange(0, 255)

record = []
state = 'LIVE'
frame = 0


def rec():
    global state
    state = 'REC'
    scope.run_single()
    t.start(100)
    mw.pauseButton.setEnabled(True)
    mw.playButton.setDisabled(True)
    mw.liveButton.setDisabled(True)
    mw.recButton.setDisabled(True)


def play():
    global state
    global frame
    scope.run_single()
    state = 'PLAY'
    t.start(mw.spinBox_2.value())
    mw.pauseButton.setEnabled(True)
    mw.recButton.setDisabled(True)
    mw.liveButton.setDisabled(True)



def pause():
    global state
    global frame
    state = 'PAUSE'
    t.stop()
    if mw.listWidget.count() > 0:
        mw.playButton.setEnabled(True)
    mw.pauseButton.setDisabled(True)
    mw.recButton.setEnabled(True)
    mw.liveButton.setEnabled(True)


def live():
    global state
    global frame
    # scope.run_single()
    state = 'LIVE'
    t.start(40)
    mw.pauseButton.setEnabled(True)
    mw.playButton.setDisabled(True)
    mw.recButton.setDisabled(True)
    mw.liveButton.setDisabled(True)

wave_data = []
def updateData():
    global frame
    global wave_data
    timestamp = str(datetime.now())
    if state == 'LIVE' or state == 'REC':

        meas = scope.data[0]['Value']

        print(meas)
        wave_data.append(meas)

        print(len(wave_data))

        p1.setData(y=wave_data)





## Start a timer to rapidly update the plot in pw
t = QtCore.QTimer()
t.timeout.connect(updateData)


mw.playButton.clicked.connect(play)
mw.recButton.clicked.connect(rec)
mw.liveButton.clicked.connect(live)
mw.pauseButton.clicked.connect(pause)
mw.spinBox_2.valueChanged.connect(t.setInterval)
mw.listWidget.currentRowChanged.connect(updateData)
# updateData()





## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
