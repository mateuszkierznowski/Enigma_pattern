from flickrapi import FlickrAPI
import os
import requests
import uuid
from PIL import Image
import numpy as np


def save_photo(photo_name, tag):
    file = open(os.path.join(tag, tag + '_' + str(uuid.uuid4()) + '.jpg'), 'wb')
    file.write(photo_name.content)


def check_directory(dir_path):
    os.mkdir(dir_path) if os.path.exists(dir_path) is False else None


# Function set client and download images to created/existing folder
def set_client(tag_name, stop, key, s_key):
    flickr = FlickrAPI(key, s_key)
    photos = flickr.walk(text=tag_name,
                         tag_mode='all',
                         tags=tag_name,
                         extras='url_o',
                         per_page=50)
    iterator = 0
    ulr_lst = []
    for photo in photos:
        url = photo.get('url_o')
        print(url)
        ulr_lst.append(url)
        if iterator == stop:
            break
        iterator += 1
    check_directory(tag_name)
    clean_url_lst = [link for link in ulr_lst if str(link).endswith('jpg')]
    links = [requests.get(link) for link in clean_url_lst]
    [save_photo(link, tag_name) for link in links]


def get_credentials():
    if os._exists('credentials.txt') is True:
        return True


def main():
    if 'credentials.txt' not in os.listdir(os.getcwd()):
        key = str(input('Type key: '))
        s_key = str(input('Type secret key: '))
        with open('credentials.txt', 'w') as f:
            f.write('key:' + key + '\n'
                    's_key:' + s_key + '\n')
            f.close()
    tag = str(input('Type tag: '))
    stop = int(input('How many links want you to download ?: '))

    with open('credentials.txt', 'r') as f:
        cred = f.readlines()
        f.close()
    key = [key[4:-1] for key in cred]

    set_client(tag, stop, key[0], key[1])


# Function finds most red photo and return it's name
def find_most_red_photo(tag):
    pic_lst = os.listdir(os.path.join(os.getcwd(), tag))
    r_lst = [red_score(img) for img in pic_lst]
    max = np.argmax(r_lst)
    return pic_lst[max]


def red_score(photo):
    img = Image.open(os.path.join('house', photo))
    array = np.asarray(img)
    r_array = np.asarray(array)
    return np.mean(r_array)


if __name__ == '__main__':
    main()
