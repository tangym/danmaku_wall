#!/usr/bin/python3
# -- encoding: utf8 --
# author: TYM
# date: 2015-3-15
import sys
import time
from threading import Thread, Lock
from PyQt4.QtGui import *
from PyQt4 import QtCore
import uuid
import logging
import json
from channel import Channel
import shorten_id as sid
import config

class InputWidget(QWidget):
    def __init__(self, label='', line_edit=''):
        QWidget.__init__(self)
        self.label = QLabel(label)
        self.line_edit = QLineEdit(line_edit)
        self.setLayout(QBoxLayout(QBoxLayout.LeftToRight))
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.line_edit)


class DanmakuWidget(QWidget):
    _wall = []

    def __init__(self):
        QWidget.__init__(self)
        self.setLayout(QBoxLayout(QBoxLayout.TopToBottom))
        for i in range(config.WALL_LENGTH):
            self._wall += [QLabel()]
            self.layout().addWidget(self._wall[i])
            self._wall[i].setWordWrap(True)


    def refresh_wall(self, danmakus):
        if len(danmakus) < config.WALL_LENGTH:
            danmakus += [{'content': ''} for i in range(config.WALL_LENGTH)]
        danmakus = danmakus[:config.WALL_LENGTH]

        for i in range(config.WALL_LENGTH):
            font = QFont()
            size = 40 + 0.2 * (config.DANMAKU_LENGTH['max']
                                    - len(danmakus[i]['content']))
            font.setPixelSize(size)
            self._wall[i].setFont(font)
            self._wall[i].setText(danmakus[i]['content'])


class ExamWidget(QWidget):
    _channel = None
    _danmakus = []
    _lock = Lock()
    _refresh_signal = QtCore.pyqtSignal()

    def __init__(self):
        QMainWindow.__init__(self)

        self.channel_widget = InputWidget(label='频道', line_edit='demo')
        self.sub_passwd_widget = InputWidget(label='播放密码', line_edit='')
        self.sub_passwd_widget.line_edit.setEchoMode(QLineEdit.Password)
        self.uuid_widget = InputWidget(label='uuid',
                line_edit=sid.shorten(uuid.uuid1().bytes))
        self.uuid_widget.button = QPushButton('生成')
        self.uuid_widget.layout().addWidget(self.uuid_widget.button)
        self.connect_button = QPushButton('走你')
        self.danmaku_widget = DanmakuWidget()

        self.uuid_widget.button.clicked.connect(lambda :
                self.uuid_widget.line_edit.setText(sid.shorten(uuid.uuid1().bytes)))
        self.connect_button.clicked.connect(self.connect_channel)
        self._refresh_signal.connect(self.refresh)

        self.setLayout(QBoxLayout(QBoxLayout.TopToBottom))
        self.layout().addWidget(self.channel_widget)
        self.layout().addWidget(self.sub_passwd_widget)
        self.layout().addWidget(self.uuid_widget)
        self.layout().addWidget(self.connect_button)
        self.layout().addWidget(self.danmaku_widget)

        self.uuid_widget.setVisible(False)
        self.danmaku_widget.setVisible(False)
        self.setWindowTitle('弹幕墙')


    @QtCore.pyqtSlot()
    def connect_channel(self):
        for w in [self.layout().itemAt(i).widget()
                    for i in range(self.layout().count())]:
            w.setVisible(False)
        self.danmaku_widget.setVisible(True)
        self.showFullScreen()

        channel_name = self.channel_widget.line_edit.text().strip()
        sub_passwd = self.sub_passwd_widget.line_edit.text().strip()
        uid = self.uuid_widget.line_edit.text().strip()

        self._channel = Channel(channel_name, uid, sub_passwd)
        get_danmaku_thread = Thread(target=self.get_danmakus, daemon=True)
        get_danmaku_thread.start()

        refresh_thread = Thread(target=self.refresh_wall, daemon=True)
        refresh_thread.start()


    def keyPressEvent(self, event):
        if event.key() == config.HOTKEY['exit']:
            QApplication.quit()
        elif event.key() == config.HOTKEY['next']:
            self._refresh_signal.emit()


    def refresh_wall(self):
        while True:
            self._refresh_signal.emit()
            time.sleep(config.REFRESH_INTERVAL)

    @QtCore.pyqtSlot()
    def refresh(self):
        self._lock.acquire()
        self.danmaku_widget.refresh_wall(
                self._danmakus[:config.WALL_LENGTH])
        #for i in range(len(self._danmakus)):
        #    del self._danmakus[i]
        if len(self._danmakus) > config.WALL_LENGTH:
            del self._danmakus[0]
        self._lock.release()


    def get_danmakus(self):
        if self._channel:
            while True:
                danmakus = self._channel.get_danmaku()
                if danmakus:
                    self._lock.acquire()
                    self._danmakus += \
                            [{
                                'content': danmaku['text'],
                                'position': danmaku['position'],
                                'color': danmaku['style']
                            } for danmaku in danmakus]
                    self._lock.release()


if __name__ == '__main__':
    #log = config.logger

    app = QApplication(sys.argv)
    main = ExamWidget()
    main.show()

    sys.exit(app.exec_())
