from PySide2.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QMessageBox, QStatusBar
import sys
from PySide2.QtGui import QIcon, QPixmap

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.statusFlag = False
        self.newText = QLabel(self)
        
        self.setWindowTitle('LAZ')
        self.setGeometry(200, 100, 900, 800) # x, y, width, height отсчет х,у от верхнего левого угла
        self.setMinimumSize(250, 100) # w, h
        # self.setMaximumSize(1000, 800) # w, h
               
        self.setIcon()
        self.setButton()
        self.statusBar()
        
    
    def setIcon(self):
        '''Функция для установки иконки окна'''
        appIcon = QIcon('nha.png')
        self.setWindowIcon(appIcon)
        
    
    def setButton(self):
        '''Функция создания и обработки кнопок в окне'''
        self.connect_btn = QPushButton('Соединиться', self) # кнопка соединения с прибором
        # connect_btn.setText(f"{self.getConName()}")
        self.connect_btn.setGeometry(50, 50, 150, 50) # (x, y , w, h)
        
        self.quit_btn = QPushButton('Выйти', self) # кнопка выхода из программы
        self.quit_btn.setGeometry(800, 700, 150, 50) # (x, y , w, h)
        
        self.quit_btn.clicked.connect(self.quitApp)
        self.connect_btn.clicked.connect(self.con_clk)
        # connect_btn.clicked.connect(self.getConName)
        #  connect_btn.clicked().setText(f"{self.getText()}")
        
        
        self.test = QPushButton(parent=self)
        self.test.setGeometry(300,300, 150, 50)
        self.test.setText(f"{self.getConName()}")
    
    
    def getText(self):
        '''Функция изменения надписи на тестовой кнопке по изменению статуса прибора'''
        status = ['Не подключен', 'Подключен']
        print(status[self.statusFlag])               
        return status[self.statusFlag]    
    
    def statusBar(self):
        '''Функия создания полоски статуса прибора'''
        self.myStatus = QStatusBar()
        self.myStatus.showMessage('Здесь будут подсказки к действиям', 0)
        self.setStatusBar(self.myStatus)
        self.wcLabel = QLabel(f"{self.getDeviceStatus()}")
        self.myStatus.addPermanentWidget(self.wcLabel)
        # self.test.setText(f"{self.getText()}") # так надпись меняется 1 раз, больше не меняется
    
    
    def con_clk(self):
        '''Функция обработки клика по кнопке "Соединиться"'''
        self.setDeviceStatus()
        # self.statusBar() НЕ НАДО ПОСТОЯННО ПЕРЕСОЗДАВАТЬ СТАТУС, МЕНЯЙ УЖЕ СОЗДАННЫЙ
        self.wcLabel.setText(f"{self.getDeviceStatus()}")

        # self.setButton() НЕ НАДО СОЗДАВАТЬ НЕСКОЛЬКО КНОПОК ПРИ КАЖДОМ НАЖАТИИ
        # print('click')
        self.newText.setText(f"{self.getConName()}") # ПОЧЕМУ НЕ РАБОТАЕТ!!!!! вывод состояния прибора в окне для проверки 
        self.newText.setGeometry(100, 150, 150, 50)
        self.test.setText(f"{self.getConName()}") # вывод текста в окне работет, а текст на кнопке не меняется
        self.connect_btn.setText(f"{self.getConName()}")
   
   
    def setDeviceStatus(self):
        '''Функция задания статуса прибора'''
        self.statusFlag = ~self.statusFlag
        # if (self.statusFlag):
        #     self.statusFlag = False
        # else:
        #     self.statusFlag = True
        print(self.statusFlag)
    
    
    def getConName(self):
        conName = ['Соединиться', 'Отключиться']
        print(conName[self.statusFlag])
        return conName[self.statusFlag]
    
    def getDeviceStatus(self):
        '''Функция получения состояния прибора для отображения'''
        status = ['Не подключен', 'Подключен']               
        return status[self.statusFlag]
    
    
    def quitApp(self):
        '''Подтверждение выхода из программы'''
        userInfo = QMessageBox.question(self, "Подтверждение", \
                                        "Вы действительно хотите выйти?", \
                                        QMessageBox.Yes | QMessageBox.No)
        
        if userInfo == QMessageBox.Yes:
            myApp.quit()
            
        elif userInfo == QMessageBox.No:
            pass
        

myApp = QApplication(sys.argv)
window = Window()
window.show()

myApp.exec_()  
sys.exit(0)