import requests
from pprint import pprint
import os
import json

TOKEN_VK = 
TOKEN_YA =
TOKEN_OK =

class VkUser:

    url = "https://api.vk.com/method/"
    def __init__(self, token, version):
        self.params = {
            "access_token": token,
            "v": version
        }

    def get_picture_info(self, user_id=None, count=5):
        metod_url = self.url + "photos.get"
        metod_params = {
            "owner_id":user_id,
            "album_id":"profile",
            "rev":"1",
            "extended":"1",
            "count":str(count)
        }
        res = requests.get(metod_url, params={**self.params, **metod_params}).json()
        return res

    def get_json_info(self, user_id=None, count=5):
        info = vk_client.get_picture_info(user_id=user_id, count=count)
        json_list = []
        for i in info["response"]["items"]:
            height = 0
            width = 0
            picture_info_dict = {}
            picture_info_dict["file_name"] = (str(i["likes"]["count"]) + ".jpg")
            for j in i["sizes"]:
                if j["height"] >= height and j["width"] >= width:
                    height = j["height"]
                    width = j["width"]
                    picture_info_dict["size"] = (j["type"])
            json_list.append(picture_info_dict)
        with open('VK.json', 'w', encoding='utf-8') as f:
            json.dump(json_list, f, indent=4)

    def get_picture_url(self, user_id=None, count=5):
        info = vk_client.get_picture_info(user_id=user_id, count=count)
        picture_url_dict = {}
        for i in info["response"]["items"]:
            height = 0
            width = 0
            for j in i["sizes"]:
                if j["height"] >= height and j["width"] >= width:
                    height = j["height"]
                    width = j["width"]
                picture_url_dict["VK" + str(i["id"])] = j["url"]             #Имена фото лучше давать по id из ВК, так как лайки могут повторятся, а id - уникально.
        return picture_url_dict

class OkUser:

    url = "https://api.ok.ru/fb.do"
    def __init__(self, token):
        url = "https://api.ok.ru/fb.do"
        self.params = {
        "application_key": token["application_key"],
        "access_token": token["access_token"],
        }

    def get_picture_info(self, user_id=None, count=5):
        metod_url = self.url + "photos.get"
        metod_params = {
            "format": "json",
            "count": count,
            "method": "photos.getPhotos"
        }
        res = requests.get(self.url, params={**self.params, **metod_params}).json()
        return res

    def get_json_info(self, user_id=None, count=5):                                    #ЭТО НЕ РАБОТАЕТ! ПОЧЕМУ? FieldSets?
        info = ok_client.get_picture_url(user_id=user_id, count=count)
        json_list = []
        for i in info.keys():
            metod_params = {"photo_id": i[2:], "method": "photos.getPhotos", "fields": "like"}
            res = requests.get(self.url, params={**self.params, **metod_params}).json()
            pprint(res)
        with open('OK.json', 'w', encoding='utf-8') as f:
            json.dump(json_list, f, indent=4)

    def get_picture_url(self, user_id=None, count=5):
        info = ok_client.get_picture_info(user_id=user_id, count=count)
        picture_url_dict = {}
        for i in info["photos"]:
            picture_url_dict["OK" + str(i["id"])] = i["pic640x480"]
        return picture_url_dict

class YaUploader:

    url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    def __init__(self, token):
        self.headers = {
            "Accept" : "application/json",
            "Authorization" : f"OAuth {token}"
        }

    def create_dir(self):
        path_to_file = "Сохраненные фотографии"
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {"path": path_to_file}
        upload = requests.put(url, headers=self.headers, params=params)
        return path_to_file

    def upload(self, picture_url_dict):
        path_to_file = ya_uploader.create_dir()
        i = 0
        for name, url in picture_url_dict.items():
            upload_path = path_to_file + f"/{name}.jpg"
            test = requests.get(self.url, headers=self.headers, params={"path": upload_path})
            i += 1
            if test.json().get("error", "") == "DiskResourceAlreadyExistsError":
                print(f"Изображение {name} уже сохранено на Яндекс.Диск! Прогресс: {i}/{len(picture_url_dict)}")
            else:
                params = {"path": upload_path, "url": f"{url}"}
                upload = requests.post(self.url, headers=self.headers, params=params)
                print(f"Изображение {name} успешно загружено. Прогресс: {i}/{len(picture_url_dict)}")

if __name__ == '__main__':

    vk_client = VkUser(TOKEN_VK, '5.131')
    ok_client = OkUser(TOKEN_OK)
    ya_uploader = YaUploader(TOKEN_YA)
    vk_client.get_picture_url()
    vk_client.get_json_info()
    ok_client.get_picture_url()
    ok_client.get_json_info()
    ya_uploader.upload(vk_client.get_picture_url())
    ya_uploader.upload(ok_client.get_picture_url())
