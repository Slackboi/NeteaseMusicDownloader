import requests
import json
import os
from urllib import parse
from bs4 import BeautifulSoup
import eyed3
import urllib.request
from tempfile import TemporaryDirectory

def download():
    # 获取播放列表
    #
    # 歌单链接 去掉连接中的 https://music.163.com/#/playlist?id=2127487363
    origin_link = "https://music.163.com/playlist?id=2902257447"
    header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/71.0.3578.98 Safari/537.36',
              'Remote Address': '59.111.181.35:443',
              'Referrer Policy': 'origin',
              'authority': 'music.163.com',
              'path': '/playlist?id=2902257447',
              'referer': 'https://music.163.com/',
              }

    # 存储音乐播放链接
    music_links = {}
    # 存储音乐下载链接
    music_download_links = []

    response = requests.get(origin_link, headers=header).content
    soup = BeautifulSoup(response, "lxml")
    songs = soup.ul.find_all('li')
    for song in songs:
        music_links[song.a.string] = 'https://music.163.com' + song.a.attrs['href']
    print(len(music_links))

    # 获取音乐下载链接
    post_url = "http://www.zhmdy.top/music/"

    # 更改为自己的项目路径
    mac_path = "/Users/a1/Downloads/"
    file_path = "/Users/a1/Downloads/downloads/"
    file_list = os.listdir(file_path)
    
#    创建临时工作目录
    with TemporaryDirectory() as temp_path:
        print('dirname is:', temp_path)
    
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    for song in music_links.values():
#         print(song)
#         exit(1)
        post_headeer = {
            'Host': 'zhmdy.top',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Origin': 'http://www.zhmdy.top',
            'X-Requested-With': 'XMLHttpRequest',
            # 'DNT': str(1),
            # 'Content-Length': str(83),
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'Referer': 'http://music.wandhi.com/?url=' + parse.urlencode(song),
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cookie': 'UM_distinctid=16c99678a2e34-0c61fe61a5015d-b781636-144000-16c99678a2f82; CNZZDATA1274607868=648588871-1565941677-null%7C156594710',
        }
        payload = {'input': song, 'filter': 'url', 'type': '_', 'page': 1}
        data = parse.urlencode(payload).encode('utf-8')
        resp = requests.post(post_url, data=data, headers=post_headeer).content
        soup2 = BeautifulSoup(resp, "lxml")
        content = soup2.p.string
        content = json.loads(str(content))
        artist = content['data'][0]['author'].replace('/', '').replace('?', '')
        album = 'Unknown Album'
        title = content['data'][0]['title'].replace('/', '').replace('?', '')
        album_art = urllib.request.urlopen(content['data'][0]['pic'].replace('?param=300x300', ''))
        name = artist + ' - ' + title
        music_download_link = content['data'][0]['url']
        final_path = file_path+artist+'/'+album+'/'
        
        if not os.path.exists(final_path):
                os.makedirs(final_path)
                
        if music_download_link is not None and name + '.mp3' not in final_path:
            music_download_links.append(music_download_link)
            
            print(
            '正在下载' +
            name
            + '.mp3'
#            content['data'][0]
#            , music_download_link
            )
            
            with open(final_path+name+'.mp3', 'wb') as fb:
                fb.write(requests.get(music_download_link).content)

            # 操作mp3文件
            stream = eyed3.load(final_path+name+'.mp3')
            
#            if (stream.tag == None):
            stream.initTag()
             
            temp_pic = album_art.read()
            with open(temp_path+'temppic.jpg', 'wb') as pic:
                pic.write(temp_pic)
            stream.tag.images.set(3, open(temp_path+'temppic.jpg', 'rb').read(), 'image/jpeg')
            stream.tag.save()
#            temp_pic = album_art.read()
#            with open(final_path+'temppic.jpg', 'wb') as pic:
#                pic.write(temp_pic)
#            print(temp_path+'/'+name+'.jpg')
#            stream.tag.images.set(3, open(final_path+'temppic.jpg', 'rb').read(), 'image/jpeg')
#            stream.tag.save()
        else:
            print(name + '.mp3 已经存在！')


if __name__ == '__main__':
    download()
