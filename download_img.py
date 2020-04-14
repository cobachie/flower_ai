# ImageNet からモデル生成用画像をダウンロードする
from urllib import request
import os, time
import requests
import json

def main():
    # ImageNet API
    # see: http://image-net.org/download-API
    IMG_LIST_URL = "http://www.image-net.org/api/text/imagenet.synset.geturls.getmapping?wnid={}"
    LIMIT_SIZE = 10

    wnid = 'n11712282'
    url = IMG_LIST_URL.format(wnid)
    r = requests.get(url)

    if r.status_code != requests.codes.ok:
        print('NG')
        exit(0)

    # 取得したファイル名とURLをそれぞれ配列に格納する
    data = r.text.split()
    names = data[::2]
    urls = data[1::2]

    # 画像ダウンロード
    STORAGE_DIR = '/Volumes/Photos2016/flower_ai/'
    url = "http://farm1.static.flickr.com/194/467227983_ce131cca2a.jpg"

    for i, name in enumerate(names):
        url = urls[i]
        if i > LIMIT_SIZE:
            break

        target_dir = STORAGE_DIR + wnid
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        filepath = target_dir + '/' + "{}.jpg".format(name)
        if os.path.exists(filepath): continue

        try:
            request.urlretrieve(url, filepath)
        except:
            continue

        time.sleep(1)


if __name__ == "__main__":
    main()

