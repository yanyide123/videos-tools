import json
import os
import pandas as pd
import configparser
global gMessage
conf= configparser.ConfigParser()
# config = {'playlist': [], 'playCurrent': {
#     'index': 0, 'audio': 30, 'postion': 0}}
# video_path = "E:\\zidongbiaozhu\\pyqt5\\ll"
# video_filname = os.listdir(video_path)
# # print(video_filname)
# for index, video in enumerate(video_filname):
#     print(index)
#     print(video)
#     video_filepath = os.path.join(video_path, video)
#     print(video_filepath)
#     video_filename = video.split(".avi")[0]
#     print(video_filename)
#     config["playlist"].append({"filepath":video_filepath, "filename": video_filename})
#     # config["playlist"]["filename"] = video_filename
# with open("./config1.json", "w", encoding="utf-8") as f:
#     json.dump(config, f, ensure_ascii=False, indent=4)

# videos_path = pd.read_csv("configuration_file.txt", encoding="utf-8", sep="\t", header="infer")
# print(videos_path)
# for i in videos_path:

conf.read('configuration_file.conf', encoding="utf-8")  # 文件路径
filePath = conf.get("cache", "video_path")
rulePath = conf.get("cache", "rulePath")
tag_position = conf.get("cache", "tag_position")
tag_len = conf.get("cache", "tag_len")
texts_to_tag = conf.get("cache", "texts_to_tag")
print(filePath)
print(rulePath)
print(tag_position)
print(tag_len)
print(texts_to_tag)
print(texts_to_tag.split(","))
for i in texts_to_tag.split(","):
    print(i)