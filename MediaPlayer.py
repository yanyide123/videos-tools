import os
import time
import sys
import json
import subprocess
import shutil
import pandas as pd

import configparser
global gMessage
conf= configparser.ConfigParser()
# from myVideoWidget import myVideoWidget

FileName = os.path.basename(sys.argv[0])
FilePath = sys.argv[0].replace(FileName, "")
UiName = FileName.replace(".py", ".ui")
UiPath = FilePath + UiName
Ui_pyName = FilePath+"ui.py"
FileFlag = os.path.isfile(Ui_pyName)

if FileFlag == 0:
    sys_cmd = os.popen("pyuic5"+" -o "+Ui_pyName+" "+UiPath)
    time.sleep(1)
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from audio import audioWidget
from urlWidget import urlWidget
from ui import Ui_Form

config = {'playlist': [], 'playCurrent': {
    'index': 0, 'audio': 30, 'postion': 0}}
print(config)
# class myVideoWidget(QVideoWidget):
#     doubleClickedItem = pyqtSignal(str)  # 创建双击信号
#     def __init__(self,parent=None):
#         super(QVideoWidget,self).__init__(parent)
#     def mouseDoubleClickEvent(self,QMouseEvent):     #双击事件
#         self.doubleClickedItem.emit("double clicked")

# 复制原文件，到对应标签的文件夹
def copyfile(srcfile, dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist" % srcfile)
    else:
        f_path, f_name = os.path.split(dstfile)
        if not os.path.exists(f_path):
            os.makedirs(f_path)
        shutil.copyfile(srcfile, dstfile)
        print("copy %s -> %s" % (srcfile, dstfile))


class m_window(QWidget, Ui_Form):
    def __init__(self):
        super(m_window, self).__init__()  # 子类中调用父类同名构造方法/类似uic.loadUi()加载ui文件
        ############
        self.LoadCache()
        # conf.read('cache.conf')  # 文件路径
        # self.video1_path = conf.get("cache", "video_path")
        # print(self.video1_path)
        # self.texts_to_tag = conf.get("cache", "texts_to_tag")
        # self.result_path = conf.get("cache", "result_path")
        # self.tag_position = int(conf.get("cache", "tag_position"))
        # self.tag_position = 6
        
        self.setupUi(self)
        self.IconShow()
        # 获取配置文件夹下的所有文件
        self.GetVideoPath()

        # self.videoFullScreen = False   # 判断当前widget是否全屏
        # self.videoFullScreenWidget = myVideoWidget()   # 创建一个全屏的widget
        # self.videoFullScreenWidget.setFullScreen(1)
        # self.videoFullScreenWidget.hide()               # 不用的时候隐藏起来

        # self.show()
        self.videoframe = QVideoWidget(self)
        self.layout_videoframe.addWidget(self.videoframe)
        self.player = QMediaPlayer(self)
        self.player.setVideoOutput(self.videoframe)

        self.playrate = float(1)
        # self.pushButton_4.clicked.connect(lambda: self.FastForword())
        # self.pushButton_5.clicked.connect(lambda: self.Jog())

        # self.videoFullScreenWidget.doubleClickedItem.connect(self.videoDoubleClicked)  # 双击响应
        # self.wgt_video.doubleClickedItem.connect(self.videoDoubleClicked)  # 双击响应

        self.playListInit()
        self.connectBind()
        self.bindPlaylistAnddListWidget()
        self.initAudioAndFile()
        self.fileBtnMenuInit()
        self.cctvBtnInit()
        self.readConfig()
        self.startSltPlayStart()

        # self.tag_position = 0

        
    def IconShow(self):
        app.setWindowIcon(QIcon('./icon/play.png'))
        # self.pushButton.setIcon(QIcon('./icon/aiqiyi.png'))
        # self.pushButton_2.setIcon(QIcon('./icon/cctv.png'))
        self.pushButton_file.setIcon(QIcon('./icon/file.png'))
        # self.pushButton_setup.setIcon(QIcon('./icon/setting.png'))
    def LoadCache(self):
        conf.read('cache.conf')  # 文件路径
        self.video1_path = conf.get("cache", "video_path")
        self.texts_to_tag = conf.get("cache", "texts_to_tag")
        self.result_path = conf.get("cache", "result_path")
        self.tag_position = int(conf.get("cache", "tag_position"))
        
    def GetVideoPath(self):
        video_path = self.video1_path
        video_filname = os.listdir(video_path)
        # print(video_filname)
        for index, video in enumerate(video_filname):
            video_filepath = os.path.join(video_path, video)
            video_filename = video.split(".")[0]
            config["playlist"].append({"filepath": video_filepath, "filename": video_filename})
            # config["playlist"]["filename"] = video_filename
        with open("./config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        
    # 音频设置初始化，文件添加初始化
    def initAudioAndFile(self):
        self.urlWidget = urlWidget() #添加链接的类
        self.urlWidget.fileInfo_Signle.connect(self.sltUrlWidget) #信号
        self.audio = audioWidget()
        self.audio.hide()
        self.audio.setParent(self)
        self.audio.getSlider().valueChanged.connect(self.sltSetAudioValue)
        self.audio.getMuteBtn().clicked.connect(self.sltSetAudioMute)

    # 播放列表初始化 - 声明/定义/播放模式设置
    def playListInit(self):
        self.playList = QMediaPlaylist()
        self.player.setPlaylist(self.playList)
        self.playList.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
        self.player.positionChanged.connect(self.sltShowPlayTime)

        self.player.positionChanged.connect(self.PlayTime)

    # 信号槽绑定函数 -- 主要功能按键 播放/上一个/下一个/音频/文件/设置

    def connectBind(self):
        self.pushButton_play.clicked.connect(self.sltPlayState)
        self.pushButton_befor.clicked.connect(self.sltPlayBefore)
        self.pushButton_next.clicked.connect(self.sltPlayNext)
        # self.pushButton_AUDIO.clicked.connect(self.sltAudio)
        # self.pushButton_setup.clicked.connect(self.sltSetup)
        # self.pushButton.clicked.connect(self.aqiyi)
        self.pushButton.setText("标注进度:" + str(int(self.tag_position + 1)) + "/" + str(self.videos_quantity()))

        self.pushButton_3.clicked.connect(self.fast5)
        self.pushButton_6.clicked.connect(self.jog5)

        self.listWidget_playlist.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidget_playlist.customContextMenuRequested.connect(self.listWidgetRightMenu)

        # 进度条
        self.player.durationChanged.connect(self.getDuration)
        self.player.positionChanged.connect(self.getPosition)
        self.sld_duration.sliderMoved.connect(self.updatePosition)
    
    def startSltPlayStart(self):
        self.playList.setCurrentIndex(self.tag_position)
        self.player.stop()
    
    def sltPlayState(self):
        if self.player.state() == QMediaPlayer.StoppedState or self.player.state() == QMediaPlayer.PausedState:
            # self.playList.setCurrentIndex(self.tag_position)
            self.player.play()
            self.pushButton_play.setText("暂停")
        else:
            self.player.pause()
            # self.playList.setCurrentIndex(self.tag_position)
            self.pushButton_play.setText("播放")

    def sltPlayBefore(self):
        self.player.stop()
        # self.playList.setCurrentIndex(self.playList.currentIndex() - 1)
        self.playList.setCurrentIndex(
            (self.playList.currentIndex()-1 < 0) and 0 or self.playList.currentIndex()-1)
        self.pushButton.setText("标注进度:" + str(self.playList.currentIndex() + 1) + "/" + str(self.videos_quantity()))
        self.player.play()

    def sltPlayNext(self):
        self.player.stop()
        # self.playList.setCurrentIndex(self.playList.currentIndex() + 1)
        self.playList.setCurrentIndex((self.playList.currentIndex(
        ) + 1 == self.playList.mediaCount()) and 0 or (self.playList.currentIndex() + 1))
        self.pushButton.setText("标注进度:" + str(self.playList.currentIndex() + 1) + "/" + str(self.videos_quantity()))
        self.player.play()

    # 文件按钮绑定菜单/本地文件/网络资源
    def fileBtnMenuInit(self):
        btnMenu = QMenu(self)
        btnMenu.addAction("本地文件")
        # btnMenu.addAction("网络资源")
        self.pushButton_file.setMenu(btnMenu)
        btnMenu.triggered.connect(self.sltFile)

    # 添加本地文件
    def addLoadFile(self):
        # str = QFileDialog.getOpenFileName(
        #     self, "选择媒体文件", self.video1_path, "video files(*.avi *.mp4 *.wmv)")
        str = QFileDialog.getExistingDirectory(
            self, "选择媒体文件", self.video1_path)
        
        # print(str)
        filePath_all = str
        filePath = []
        fileName = []
        # fileName = (filePath.split('/')[-1]).split('.')[0]
        video_filename = os.listdir(filePath_all)
        # self.pushButton.setText("标注进度:" + str(self.playList.currentIndex() + 2) + "/" + str(len(video_filename)))
        for index, video in enumerate(video_filename):
            filePath.append(os.path.join(filePath_all, video))
            fileName.append(video.split(".")[0])
        # print(fileName)
        # print(filePath)
        return filePath, fileName, str
    
    def videos_quantity(self):
        video_path = self.video1_path
        video_filname = os.listdir(video_path)
        videos_len = len(video_filname)
        return videos_len
    
    # def GetFilename(self): # 获取文件名
    #     video_list = os.listdir("E:\\zidongbiaozhu\\pyqt5\\ll")
    #     for str in video_list:
    #         filePath = str
    #         fileName = str.split("\\")[-1].split(".avi")[0]
    #         # print(fileName)
    #         # print(filePath)
    #     return [filePath, fileName]

	#添加网络文件
    def addNetFile(self):
        self.urlWidget.show()

    def sltUrlWidget(self,list):
        config['playlist'].append({'filepath':list[0],'filename':list[1]})
        self.addFile(list[0],list[1])

    def sltUrlWidget(self,list):
    	config['playlist'].append({'filepath':list[0],'filename':list[1]})
    	self.addkoFile(list[0],list[1])

# 我自己的 akfhalifhaifhalifhlaffa

    def aqiyi(self):
        url, okPressed = QInputDialog.getText(
            self, "输入地址", "地址:", QLineEdit.Normal, "")
        if not okPressed:
            print('取消了输入')
        if url != '':
            cmd = ['you-get', '-p', 'mpv', url]
            subprocess.Popen(cmd)
        # 文件按钮绑定菜单/本地文件/网络资源

    def cctvBtnInit(self):
        texts_to_tag = self.texts_to_tag
        btnMenu = QMenu(self)
        for tag in texts_to_tag.split(","):
            btnMenu.addAction(tag)
        self.pushButton_2.setMenu(btnMenu)
        btnMenu.triggered.connect(self.classify)

    def classify(self, action):
        # sender = self.sender()
        # self.video_path = "./ll/"
        # # print(dir_path)
        # fileInfo = self.GetFilename()
        # print(fileInfo)
        # filepath = fileInfo[0]
        # filename = fileInfo[1]
        # print(filepath)
        # print(filename)
        # current_video_path = filepath
        # copyfile(self.video_path + current_video_path, dir_path + current_video_path)
        # self.setWindowTitle("当前是第 %d 个图片" % self.idx)
        
        # self.playList.setCurrentIndex(self.listWidget_playlist.row(self.currentItem))
        # print(self.playList.setCurrentIndex(self.listWidget_playlist.row(self.currentItem)))
        # print("==============================")
        # print(self.playList.currentIndex())
        # for i in range(0, self.playList.mediaCount()):
        #     print(i)
        #     path = ""
        #     if self.playList.media(i).canonicalUrl().isLocalFile():
        #         path = self.playList.media(i).canonicalUrl().toLocalFile()
        #         print(self.playList.media(i).canonicalUrl().isLocalFile())
        #         print(path)
        #     else:
        #         path = self.playList.media(i).canonicalUrl().toString()
        #         print(2222222222222222222)
        #         print(path)
        texts_to_tag = self.texts_to_tag
        videos_lable_list = []
        for tag in texts_to_tag.split(","):
            if action.text() == tag:
                videos_index = self.playList.currentIndex()
                path = self.playList.media(videos_index).canonicalUrl().toLocalFile()
                videos_lable_list.append([path.split("/")[-1], tag])
        # if action.text() == "标签2":
        #     videos_index = self.playList.currentIndex()
        #     path = self.playList.media(videos_index).canonicalUrl().toLocalFile()
        #     videos_lable_list.append([path, "标签2"])
        # if action.text() == "标签3":
        #     videos_index = self.playList.currentIndex()
        #     path = self.playList.media(videos_index).canonicalUrl().toLocalFile()
        #     videos_lable_list.append([path, "标签3"])
        # if action.text() == "标签4":
        #     videos_index = self.playList.currentIndex()
        #     path = self.playList.media(videos_index).canonicalUrl().toLocalFile()
        #     videos_lable_list.append([path, "标签4"])
        new_data = pd.DataFrame(videos_lable_list)
        new_data.to_csv(self.result_path + "/" + "file_result.csv", mode="a", header=False, encoding="utf-8",
                        index=False)
            
            

    

    # def cctvFile(self, action):
    #     if action.text() == "CCTV1":
    #         cctv1 = ['you-get', '-p', 'mpv',
    #                  'http://ivi.bupt.edu.cn/hls/cctv1hd.m3u8']
    #         subprocess.Popen(cctv1)
    #     elif action.text() == "CCTV3":
    #         cctv3 = ['you-get', '-p', 'mpv',
    #                  'http://ivi.bupt.edu.cn/hls/cctv3hd.m3u8']
    #         subprocess.Popen(cctv3)
    #
    #     elif action.text() == "CCTV5":
    #         cctv5 = ['you-get', '-p', 'mpv',
    #                  'http://ivi.bupt.edu.cn/hls/cctv5hd.m3u8']
    #         subprocess.Popen(cctv5)

        # elif action.text() == "CCTV6":
        #     cctv6 = ['you-get', '-p', 'mpv',
        #              'http://ivi.bupt.edu.cn/hls/cctv6hd.m3u8']
        #     subprocess.Popen(cctv6)

# 倍速播放、快进，快退
    def FastForword(self):
        self.player.pause()
        self.playrate += 0.2
        self.SetPlaybackRate(self.playrate)
        self.player.play()

    def Jog(self):
        self.player.pause()
        self.playrate -= 0.2
        self.SetPlaybackRate(self.playrate)
        self.player.play()

    def SetPlaybackRate(self, val):
        self.player.pause()
        self.player.setPlaybackRate(val)
        self.player.play()
        # print("playbackRate:",self.player.playbackRate())

    def PlayTime(self, postion):
        global t
        t = postion
    # 快进5秒

    def fast5(self):
        global t
        # self.player.pause()
        t += 1000
        self.player.setPosition(t)
        self.player.pause()
        # self.player.play()
    # 快退5秒

    def jog5(self):
        global t
        # self.player.pause()
        t -= 1000
        self.player.setPosition(t)
        self.player.pause()
        # self.player.play()

    # 视频总时长获取
    def getDuration(self, d):
        '''d是获取到的视频总时长（ms）'''
        self.sld_duration.setRange(0, d)
        self.sld_duration.setEnabled(True)
        # self.displayTime(d)
    # 视频实时位置获取
    def getPosition(self, p):
        self.sld_duration.setValue(p)
        # self.displayTime(self.ui.sld_duration.maximum()-p)       


    # 用进度条更新视频位置
    def updatePosition(self, v):
        self.player.setPosition(v)
        # self.displayTime(self.ui.sld_duration.maximum()-v)

    # 槽函数-添加文件

    def sltFile(self, action):
        if action.text() == "本地文件":
            try:
                fileInfo_path_list,  fileInfo_name_list, file_path = self.addLoadFile()
                file_list = os.listdir(self.video1_path)
                for i in range(len(file_list)):
                    self.playList.removeMedia(0)
                    self.listWidget_playlist.takeItem(0)
                self.video1_path = file_path
                self.tag_position = 0
                # self.playList.currentIndex = 0
                # conf.read("cache.conf")
                # conf.set("cache", "video_path", file_path)
                # conf.set("cache", "tag_position", str(0))
                # conf.write(open('cache.conf', 'w'))
                config = {'playlist': [], 'playCurrent': {
                    'index': 0, 'audio': 30, 'postion': 0}}
                for fileInfo_path, fileInfo_name in zip(fileInfo_path_list, fileInfo_name_list):
                    config['playlist'].append(
                        {'filepath': fileInfo_path, 'filename': fileInfo_name})

                # video_path = file_path
                # video_filname = os.listdir(video_path)
                # videos_len = len(video_filname)
                print(config)
                with open("./config.json", "w", encoding="utf-8") as f:
                    json.dump(config, f, ensure_ascii=False, indent=4)
                self.readConfig()
                self.pushButton.setText("标注进度:" + str(int(self.tag_position + 1)) + "/" + str(self.videos_quantity()))
            except:
                pass
            # self.removeMedia()
            # self.readConfig()
                # self.addFile(fileInfo_path, fileInfo_name)
        # elif action.text() == "网络资源":
        #     self.addNetFile()
    def DelFile(self, filePath, fileName):
        self.playList.removeMedia(QMediaContent(QUrl.fromLocalFile(filePath)))


    def addFile(self, filePath, fileName):
        self.playList.addMedia(QMediaContent(QUrl.fromLocalFile(filePath)))
        self.createItem(fileName)

    def addkoFile(self, filePath, fileName):
        self.playList.addMedia(QMediaContent(QUrl(filePath)))
        self.createItem(fileName)        

    # 音频设置
    def sltAudio(self):
        pos = self.pushButton_audio.mapTo(self, QPoint(0, 0))
        x = pos.x() + self.pushButton_audio.width()/2 - self.audio.width() / 2
        y = pos.y() - self.audio.height() - 6
        self.audio.move(int(x), int(y))
        if self.audio.isHidden() == True:
            self.audio.show()
        else:
            self.audio.hide()

    def sltSetAudioValue(self, value):
        self.player.setVolume(value)

    def sltSetAudioMute(self):
        self.player.setMuted(bool(1 - self.player.isMuted()))

    # 其他设置可设置弹窗，跳到另一个窗口
    def sltSetup(self):
        print("++++++++++")

    # def videoDoubleClicked(self, text):

    #     if self.player.duration() > 0:  # 开始播放后才允许进行全屏操作
    #         if self.videoFullScreen:
    #             self.player.pause()
    #             self.videoFullScreenWidget.hide()
    #             self.player.setVideoOutput(self.wgt_video)
    #             self.player.play()
    #             self.videoFullScreen = False
    #         else:
    #             self.player.pause()
    #             self.videoFullScreenWidget.show()
    #             self.player.setVideoOutput(self.videoFullScreenWidget)
    #             self.player.play()
    #             self.videoFullScreen = True

    def listWidgetRightMenu(self, point):
        self.menu = QMenu(self.listWidget_playlist)
        self.currentItem = self.listWidget_playlist.itemAt(point)
        play_action = QAction('播放')
        del_action = QAction('删除')
        self.menu.addAction(play_action)
        self.menu.addAction(del_action)
        play_action.triggered.connect(self.actionPlay)
        del_action.triggered.connect(self.actionDel)
        self.menu.exec(QCursor.pos())

    # 右键播放槽函数
    def actionPlay(self):
        self.player.stop()
        self.playList.setCurrentIndex(self.listWidget_playlist.row(self.currentItem))
        self.player.play()
        self.pushButton_play.setText("暂停")

    # 右键删除槽函数
    def actionDel(self):
        index = self.listWidget_playlist.row(self.currentItem)
        if index == self.playList.currentIndex():
            self.player.stop()
            self.pushButton_play.setText("播放")
        self.delCurrentIndex(index)

    def delCurrentIndex(self, index):
        current = self.playList.currentIndex()
        if current == index:
            self.playList.setCurrentIndex(0)
            self.player.stop()
        print(index)
        self.playList.removeMedia(index)
        self.listWidget_playlist.takeItem(index)
        del config['playlist'][index]

    # 创建QListWidgetItem
    def createItem(self, str):
        self.item = QListWidgetItem(str)
        self.listWidget_playlist.addItem(self.item)

    # 绑定QPlayList与QListWidget
    def bindPlaylistAnddListWidget(self):
        self.listWidget_playlist.itemDoubleClicked.connect(self.doublePressPlayMedia)

    def doublePressPlayMedia(self, item):
        self.player.stop()
        self.playList.setCurrentIndex(self.listWidget_playlist.row(item))
        self.player.play()
        self.pushButton_play.setText("暂停")

    # 显示播放时长
    def sltShowPlayTime(self, postion):
        self.lcdNumber_progress.display(round(postion/1000))

    # 配置文件初始化
    def readConfig(self):
        file = open("./config.json", "r+", encoding='utf-8')
        json_str_str = json.load(file)
        for fileInfo in json_str_str['playlist']:
            self.addFile(fileInfo["filepath"], fileInfo["filename"])
            config['playlist'].append(
                {'filepath': fileInfo["filepath"], 'filename': fileInfo["filename"]})
        self.playList.setCurrentIndex(json_str_str["playCurrent"]["index"])
        self.audio.getSlider().setValue(json_str_str["playCurrent"]["audio"])
        self.player.setVolume(json_str_str["playCurrent"]["audio"])
        self.player.setPosition(int(json_str_str["playCurrent"]["postion"] * 1000))
        
    # 写入配置文件
    def writeConfig(self):
        print("Write ConfigFile!")
        # os.remove("./config.json")
        for i in range(0, self.playList.mediaCount()):
            path = ""
            if self.playList.media(i).canonicalUrl().isLocalFile():
                path = self.playList.media(i).canonicalUrl().toLocalFile()
            else:
                path = self.playList.media(i).canonicalUrl().toString()
            config['playlist'][i]["filepath"] = path
            config['playlist'][i]["filename"] = self.listWidget_playlist.item(i).text()
        config['playCurrent']['index'] = self.playList.currentIndex()
        config['playCurrent']['audio'] = self.player.volume()
        config['playCurrent']['postion'] = self.player.position() / 1000
        # print(config)
        with open("./config.json", 'w',encoding='UTF-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)

    def closeEvent_config(self):
        print("写入配置文件")
        # print(self.playList.currentIndex())
        conf.read('cache.conf')  # 文件路径
        print(self.playList.currentIndex())
        conf.set("cache", "video_path", self.video1_path)  # 修改指定section 的option
        # conf.set("cache", "texts_to_tag", self.self.texts_to_tag)  # 修改指定section 的option
        conf.set("cache", "tag_position", str(self.playList.currentIndex()))  # 修改指定section 的option
        # conf.set("cache", "result_path", str(self.result_path))  # 修改指定section 的option
    
        conf.write(open('cache.conf', 'w'))

    # 关闭事件，再退出前重写config配置文件
    def closeEvent(self, event):
        self.writeConfig()
        self.closeEvent_config()


app = QApplication(sys.argv)
window = m_window()
window.show()
sys.exit(app.exec_())
