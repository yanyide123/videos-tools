# 前言
这里时基于pyqt5写的一个视频标注系统，在步入AI时代的大环境中，CV技术目前很成熟，并且很多项目都可以落地使用，用于工业化中，之前写过关于图像分类的介绍，兴趣的朋友可以去首页看。

星光不问赶路人，时光不负有心人！

---

# 一、本文介绍
本文代码：

本文介绍：[基于python的库pyqt5短视频标注系统_TF666666的博客-CSDN博客](https://blog.csdn.net/TF666666/article/details/123688287?spm=1001.2014.3001.5502)

 本文先介绍一下视频分类前视频标注的一个小工具，将自己本地未标注的视频通过自定义标签，将视频人工进行分类，为后面视频分类提供数据集。目前最火的模型Video-Swin-Transformer，用于做视频分类。
 官方git：https://github.com/SwinTransformer/Video-Swin-Transformer

# 二、PYQT5介绍
PyQt5 是Digia的一套Qt5应用框架与python的结合，同时支持2.x和3.x，官方网站：www.riverbankcomputing.co.uk/news。
具体库介绍：（大佬的总结）https://blog.csdn.net/weixin_39568659/article/details/111459320
# 三、使用步骤
## 1.引入库
代码如下（示例）：

```c
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
```
具体根据自己的使用进行引入对应的库，这里只是举一个例子

## 2.使用
当前文件夹运行：
```c
python MediaPlayer.py
```
当然也可以在工具中单独运行MediaPlayer.py

## 2.界面展示
![在这里插入图片描述](https://img-blog.csdnimg.cn/4536c1cacb07482bb93c39db5a56f59c.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAVEY2NjY2NjY=,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)

文件：可以选择本地文件，现在代码支持.avi视频，其他的没有尝试，刚刚试验了.mp4没有打开，后面我在找问题，如果有修改后可以的，可以对代码进行更改，欢迎维护。
标签：问价夹里面有一个cache.conf配置文件，可以texts_to_tag更改自己标签，注意标签与标签用英文逗号隔开，后面希望在界面添加标签。
上一帧，下一帧：可以看每一帧的图片
上一个，下一个：切换图片
注意：添加文件直接添加文件夹就可以，自动取文件夹里去读取视频，选择的时候不会有提示，也不会有其他展示，最好把不是视频文件的其他全部删除掉。
cache.conf：配置文件中result_path保存的是标注后的结果，结果的保存形式是视频文件名+名称

# 参考文献
https://www.haolizi.net/example/key_pyqt5_2.html
https://blog.csdn.net/weixin_39568659/article/details/111459320
https://github.com/SwinTransformer/Video-Swin-Transformer