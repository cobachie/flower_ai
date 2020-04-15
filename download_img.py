from urllib import request
import os, sys, time
import requests
import json

from flickrapi import FlickrAPI

DATA_DIR = '/Volumes/Photos/flower_ai/'
# CATEGORIES = ['tulip', 'garbera', 'anemone',
#               'rose', 'cherryblossom', 'viola',
#               'daisy', 'poppy', 'carnation']
CATEGORIES = ['tulip', 'garbera', 'rose']

# Flickr 接続情報
FLICKR_KEY = ''
FLICKR_SECRET = ''

PER_PAGE = 400

def main():
    for category in CATEGORIES:
        # Flickrを検索して写真の情報を取得する
        keyword = "{} flower".format(category)
        photos = flickr_photos(keyword)

        # 写真を保存するディレクトリ
        target_dir = DATA_DIR + category + '/'
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # 写真をダウンロードする
        for photo in photos['photo']:
            url_q = photo['url_q']
            img_path = target_dir + photo['id'] + '.jpg'
            if os.path.exists(img_path): continue

            request.urlretrieve(url_q, img_path)

            time.sleep(1)


def flickr_photos(keyword):
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


if __name__ == "__main__":
    main()
