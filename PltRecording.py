# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 13:37:03 2019

@author: Javier
"""
import sys
import os
from qtpy.QtWidgets import (QHeaderView, QCheckBox, QSpinBox, QLineEdit,
                            QDoubleSpinBox, QTextEdit, QComboBox,
                            QTableWidget, QAction, QMessageBox, QFileDialog,
                            QInputDialog, QTreeWidget, QTreeWidgetItem, 
                            QWidget)

from qtpy import QtWidgets, uic
from PhyREC.NeoInterface import NeoSegment, NeoSignal
import numpy as np
import PhyREC.PlotWaves as Rplt
import matplotlib.pyplot as plt


class PltRecording(QtWidgets.QMainWindow):

    
    
    aiChannels = (
#              'Ch01',
#              'Ch02',
#              'Ch03',
#              'Ch04',
              'Ch05',
              'Ch06',
              'Ch07',
              'Ch08',
#              'Ch09',
#              'Ch10',
#              'Ch11',
#              'Ch12',
              'Ch13',
              'Ch14',
              'Ch15',
              'Ch16',
              )
    
    doColumns = ('Col1',
                 'Col2',
                 'Col3',
                 'Col4',
                 'Col5',
                 'Col6',
                 'Col7',
                 'Col8',
                 )  

    def __init__(self, parent=None):

        QtWidgets.QMainWindow.__init__(self)
        uipath = os.path.join(os.path.dirname(__file__),
                              'PltRecording.ui')

        uic.loadUi(uipath, self)
        self.setWindowTitle('PltRecording')

        self.ButLoad.clicked.connect(self.LoadData)

    def LoadData(self):
        FileIn = 'T5-HippocampalPopulationSpike-Vd_0,03_Vg_0,2_NewModules_100kHz.h5'
        self.Rec = NeoSegment(FileIn)
        print('Loaded')
        self.UploadSignals()

#    def ConnectLst(self):
#        self.LstChNames.itemSelectionChannged.connect(self.LstChNames)

    def UploadSignals(self):
        print('UploadSignals')
        self.treeWidget.clear()
        self.treeWidget.resize(250, 650)

        SigNames = []
        for sig in self.Rec.Signals():
            SigNames.append(sig.name)

        self.treeWidget.setColumnCount(2)
        self.treeWidget.setHeaderLabels(['Channels Names', 'Properties'])
        self.LstSigNames(Lst=SigNames)
        
        self.UploadSlots()

    def UploadSlots(self):
        ChOrder = self.GetChOrder()

        fig, axs = plt.subplots(len(self.aiChannels),
                                len(self.doColumns),
                                sharex=True)

        Slots = []
        for sig in self.Rec.Signals():
            chname = sig.name
            Slots.append(Rplt.WaveSlot(sig,
                                       Units='mV',
                                       Ax=axs[ChOrder[chname]],
                                       Fig=fig))

        self.LstSlots(Lst=Slots)



    def GetChOrder(self):
        Chorder = {}
        for irow, row in enumerate(self.aiChannels):
            for icol, col in enumerate(self.doColumns):
                Chorder[row+col] = (irow, icol)

        return Chorder

    def LstSigNames(self, Lst):
        for i in range(len(Lst)):
            names = QTreeWidgetItem([Lst[i]])
            self.treeWidget.addTopLevelItem(names)

    def LstSlots(self, Lst):
        for i in range(len(Lst)):
            names = QTreeWidgetItem([Lst[i]])
            self.treeWidget.addTopLevelItem(names)


    def LstChNames(self):
        print('LstChNames')

#        self.treeWidget.setText(0, str('Test'))
#        self.treeWidget.addTopLevelItems(SigNames)
        
        

def main():

    app = QtWidgets.QApplication(sys.argv)
    w = PltRecording()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()


