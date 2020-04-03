# @Author: Johnathon Frocillo
#
# CIS 457: Data Communications
# Project 2
# April 3, 2020
#
# GUI implemented with PyQt5

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtGui import QColor
import socket
import selectors
import os
from time import sleep
import threading

#Global vars
userName = "hello"
sendMessageHost = False
sendMessageConnect = False
identifier = 0 #0 for the host, 1 for the connecter

class Ui_MainWindow(object):
	#method is used to create the GUI
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(620, 600)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
		self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 591, 571))
		self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
		self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout.setObjectName("verticalLayout")
		self.horizontalLayout = QtWidgets.QHBoxLayout()
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.hostOrConnect = QtWidgets.QLabel(self.verticalLayoutWidget)
		font = QtGui.QFont()
		font.setPointSize(16)
		self.hostOrConnect.setFont(font)
		self.hostOrConnect.setObjectName("hostOrConnect")
		self.horizontalLayout.addWidget(self.hostOrConnect)
		self.hostRadioButton = QtWidgets.QRadioButton(self.verticalLayoutWidget)
		self.hostRadioButton.setObjectName("hostRadioButton")
		self.horizontalLayout.addWidget(self.hostRadioButton)
		self.connectRadioButton = QtWidgets.QRadioButton(self.verticalLayoutWidget)
		self.connectRadioButton.setObjectName("connectRadioButton")
		self.horizontalLayout.addWidget(self.connectRadioButton)
		self.applyButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
		self.applyButton.setObjectName("applyButton")
		self.horizontalLayout.addWidget(self.applyButton)
		self.verticalLayout.addLayout(self.horizontalLayout)
		self.divideLine1 = QtWidgets.QFrame(self.verticalLayoutWidget)
		self.divideLine1.setEnabled(True)
		font = QtGui.QFont()
		font.setBold(False)
		font.setWeight(50)
		self.divideLine1.setFont(font)
		self.divideLine1.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.divideLine1.setLineWidth(2)
		self.divideLine1.setFrameShape(QtWidgets.QFrame.HLine)
		self.divideLine1.setObjectName("divideLine1")
		self.verticalLayout.addWidget(self.divideLine1)
		self.messageFeedTextEdit = QtWidgets.QTextEdit(self.verticalLayoutWidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.messageFeedTextEdit.sizePolicy().hasHeightForWidth())
		self.messageFeedTextEdit.setSizePolicy(sizePolicy)
		self.messageFeedTextEdit.setReadOnly(True)
		self.messageFeedTextEdit.setObjectName("messageFeedTextEdit")
		self.verticalLayout.addWidget(self.messageFeedTextEdit)
		self.divideLine2 = QtWidgets.QFrame(self.verticalLayoutWidget)
		self.divideLine2.setLineWidth(2)
		self.divideLine2.setFrameShape(QtWidgets.QFrame.HLine)
		self.divideLine2.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.divideLine2.setObjectName("divideLine2")
		self.verticalLayout.addWidget(self.divideLine2)
		spacerItem = QtWidgets.QSpacerItem(20, 25, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
		self.verticalLayout.addItem(spacerItem)
		self.messageTextEdit = QtWidgets.QTextEdit(self.verticalLayoutWidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.messageTextEdit.sizePolicy().hasHeightForWidth())
		self.messageTextEdit.setSizePolicy(sizePolicy)
		self.messageTextEdit.setMaximumSize(QtCore.QSize(16777215, 50))
		self.messageTextEdit.setObjectName("messageTextEdit")
		self.verticalLayout.addWidget(self.messageTextEdit)
		self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_2.setObjectName("horizontalLayout_2")
		spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout_2.addItem(spacerItem1)
		self.sendMessageButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.sendMessageButton.sizePolicy().hasHeightForWidth())
		self.sendMessageButton.setSizePolicy(sizePolicy)
		self.sendMessageButton.setFlat(False)
		self.sendMessageButton.setObjectName("sendMessageButton")
		self.horizontalLayout_2.addWidget(self.sendMessageButton)
		spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout_2.addItem(spacerItem2)
		self.verticalLayout.addLayout(self.horizontalLayout_2)
		MainWindow.setCentralWidget(self.centralwidget)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

#********************** Logic and Socket Code starts here **********************************************
		
		#Alert box to get users name that will appear in chat
		global userName
		msg = QInputDialog()
		text, ok = QInputDialog.getText(msg, 'Text Input Dialog', 'Enter your name that will appear in chat:')
		if ok and text:
			userName = text
		else:
			sys.exit()

		#Make certain buttons unavailable at the start
		self.sendMessageButton.setEnabled(False)
		self.applyButton.setEnabled(False)

		#ADD ACTION LISTENERS FOR BUTTONS
		self.applyButton.clicked.connect(self.applyButton_clicked)
		self.sendMessageButton.clicked.connect(self.sendMessageButton_clicked)
		self.hostRadioButton.clicked.connect(self.enableApplyButton)
		self.connectRadioButton.clicked.connect(self.enableApplyButton)



	def applyButton_clicked(self):
		global identifier
		if self.hostRadioButton.isChecked():
			self.messageFeedTextEdit.append("You are now the HOST\n")
			identifier = 0

			hostThread = threading.Thread(target=self.host)
			hostThread.daemon = True
			hostThread.start()

		elif self.connectRadioButton.isChecked():
			self.messageFeedTextEdit.append("You are now CONNECTED\n")
			identifier = 1

			connectThread = threading.Thread(target=self.connect)
			connectThread.daemon = True
			connectThread.start()
		
		self.applyButton.setEnabled(False)
		self.hostRadioButton.setEnabled(False)
		self.connectRadioButton.setEnabled(False)
		self.sendMessageButton.setEnabled(True)

	def sendMessageButton_clicked(self):
		global sendMessageHost
		global sendMessageConnect
		global identifier
		if self.messageTextEdit.toPlainText() == "":
			self.messageTextEdit.setPlaceholderText("Enter a valid message!")
		else:
			if identifier == 0:
				sendMessageHost = True
			elif identifier == 1:
				sendMessageConnect = True

		#Asynchronous code. Give time for socket threads to work
		sleep(0.25)

		self.messageTextEdit.clear()
		self.messageTextEdit.setFontPointSize(12)
		self.messageTextEdit.setPlaceholderText("Enter your message here and then click send!")

	def enableApplyButton(self):
		if not (self.applyButton.isEnabled()):
			self.applyButton.setEnabled(True)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "Peer To Peer Chat"))
		self.hostOrConnect.setText(_translate("MainWindow", "Would you like to host or connect?"))
		self.hostRadioButton.setText(_translate("MainWindow", "Host"))
		self.connectRadioButton.setText(_translate("MainWindow", "Connect"))
		self.applyButton.setText(_translate("MainWindow", "Apply"))
		self.messageTextEdit.setPlaceholderText(_translate("MainWindow", "Enter your message here and then click Send!"))
		self.sendMessageButton.setText(_translate("MainWindow", "Send Message"))

	def host(self):
		global sendMessageHost
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(('127.0.0.1', 12345))
		s.listen()

		while True:
			conn, addr = s.accept()
			
			hostSendMsgThread = threading.Thread(target=self.hostSendMsgThread, args=(conn,))
			hostSendMsgThread.daemon = True
			hostSendMsgThread.start()

			while True:
				data = conn.recv(1024)
				if not data:
					break
				colorMsg = data.decode().split(':')
				self.messageFeedTextEdit.setTextColor(QColor(255,0,0))
				self.messageFeedTextEdit.append(colorMsg[0] + ":")
				self.messageFeedTextEdit.setTextColor(QColor(255,255,255))
				self.messageFeedTextEdit.append(colorMsg[1])

	def hostSendMsgThread(self, conn):
		global sendMessageHost
		global userName
		while True:
			if sendMessageHost == True:
				conn.send((userName + ":  " + self.messageTextEdit.toPlainText()).encode())
				self.messageFeedTextEdit.setTextColor(QColor(50,50,255))
				self.messageFeedTextEdit.append(userName + ":")
				self.messageFeedTextEdit.setTextColor(QColor(255,255,255))
				self.messageFeedTextEdit.append("  " + self.messageTextEdit.toPlainText())
				sendMessageHost = False

	def connect(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(('127.0.0.1',12345))
		
		connectSendMsgThread = threading.Thread(target=self.connectSendMsgThread, args=(s,))
		connectSendMsgThread.daemon = True
		connectSendMsgThread.start()

		while True:
			data = s.recv(1024)
			if not data:
				break
			colorMsg = data.decode().split(':')
			self.messageFeedTextEdit.setTextColor(QColor(255,0,0))
			self.messageFeedTextEdit.append(colorMsg[0] + ":")
			self.messageFeedTextEdit.setTextColor(QColor(255,255,255))
			self.messageFeedTextEdit.append(colorMsg[1])

	def connectSendMsgThread(self, s):
		global sendMessageConnect
		global userName
		while(True):
			if sendMessageConnect == True:
				s.send((userName + ":  " + self.messageTextEdit.toPlainText()).encode())
				self.messageFeedTextEdit.setTextColor(QColor(50,50,255))
				self.messageFeedTextEdit.append(userName + ":")
				self.messageFeedTextEdit.setTextColor(QColor(255,255,255))
				self.messageFeedTextEdit.append("  " + self.messageTextEdit.toPlainText())
				sendMessageConnect = False


if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())
