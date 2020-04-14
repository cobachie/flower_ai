# ImageNet からモデル生成用画像をダウンロードする
from urllib import request
import os, sys, time
import requests
import json

from flickrapi import FlickrAPI

def main():
    keyword = sys.argv[1]

    photos = flickr_photos(keyword)

    # 画像を保存するディレクトリ
    STORAGE_DIR = '/Volumes/Photos/flower_ai/'
    target_dir = STORAGE_DIR + keyword + '/'
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for i, photo in enumerate(photos['photo']):
        if not save_image(photo, target_dir): continue


def flickr_photos(keyword):
    # Flickr 接続情報
    FLICKR_KEY = ''
    FLICKR_SECRET = ''

    # 取得件数
    PER_PAGE = 300

    flickr = FlickrAPI(FLICKR_KEY, FLICKR_SECRET, format='parsed-json')

    result = flickr.photos.search(
        text=keyword,
        per_page=PER_PAGE,
        media='photos',
        sort='relevance',
        safe_search=1,
        extras='url_q, licence'
    )

    photos = result['photos']

    return photos


def save_image(photo, dir):
    url_q = photo['url_q']
    img_path = dir + photo['id'] + '.jpg'
    if os.path.exists(img_path): return False

    request.urlretrieve(url_q, img_path)

    time.sleep(1)


if __name__ == "__main__":
    main()

