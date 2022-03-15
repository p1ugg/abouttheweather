import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import open_weather_token, tk_bot
import requests
from icrawler.builtin import GoogleImageCrawler
import os
import shutil
from random import randint
import datetime



def download_image(name, dir='C:/Users/paket/yandexprojects/ботяра/ImageCrawler', count_parse=3):
    crawler = GoogleImageCrawler(storage={'root_dir': dir})
    crawler.crawl(keyword=name + ' город виды', max_num=count_parse)
    print('Фотографии по запросу', name + ' виды', 'созданы')
    upload = vk_api.VkUpload(vk)
    rand = randint(1, 3)
    photo_name = '00000' + str(rand)
    try:
        photo = upload.photo_messages(f'{dir}/{photo_name}.jpg')
    except:
        photo = upload.photo_messages(f'{dir}/{photo_name}.png')
    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    return attachment




def get_weat(city, cur_ccity, open_weather_token):
    smiles = {
        'Clear': "Ясно \U00002600",
        'Snow': "Снег \U0001F328",
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzle': 'Дождь \U00002614',
        'Thunderstorm': 'Гроза \U000026A1',
        'Mist': 'Туман \U0001F32B'
    }
    country_flag = {
        'AU': '🇦🇺',
        'AT': '🇦🇹',
        'AZ': '🇦🇿',
        'AL': '🇦🇱',
        'DZ': '🇩🇿',
        'AO': '🇦🇴',
        'AD': '🇦🇩',
        'AG': '🇦🇬',
        'AR': '🇦🇷',
        'AM': '🇦🇲',
        'AF': '🇦🇫',
        'BS': '🇧🇸',
        'BD': '🇧🇩',
        'BB': '🇧🇧',
        'BH': '🇧🇭',
        'BZ': '🇧🇿',
        'BY': '🇧🇾',
        'BE': '🇧🇪',
        'BJ': '🇧🇯',
        'BO': '🇧🇴',
        'BA': '🇧🇦',
        'BW': '🇧🇼',
        'BR': '🇧🇷',
        'BN': '🇧🇳',
        'BF': '🇧🇫',
        'BI': '🇧🇮',
        'BT': '🇧🇹',
        'VU': '🇻🇺',
        'VA': '🇻🇦',
        'GB': '🇬🇧',
        'HU': '🇭🇺',
        'VE': '🇻🇪',
        'TL': '🇹🇱',
        'VN': '🇻🇳',
        'GA': '🇬🇦',
        'HT': '🇭🇹',
        'GY': '🇬🇾',
        'GM': '🇬🇲',
        'GH': '🇬🇭',
        'GN': '🇬🇳',
        'GW': '🇬🇼',
        'DE': '🇩🇪',
        'HN': '🇭🇳',
        'PS': '🇵🇸',
        'GD': '🇬🇩',
        'GR': '🇬🇷',
        'GE': '🇬🇪',
        'DK': '🇩🇰',
        'CD': '🇨🇩',
        'DJ': '🇩🇯',
        'DM': '🇩🇲',
        'DO': '🇩🇴',
        'EG': '🇪🇬',
        'ZW': '🇿🇼',
        'IL': '🇮🇱',
        'IN': '🇮🇳',
        'ID': '🇮🇩',
        'JO': '🇯🇴',
        'IQ': '🇮🇶',
        'IR': '🇮🇷',
        'IE': '🇮🇪',
        'IS': '🇮🇸',
        'ES': '🇪🇸',
        'IT': '🇮🇹',
        'YE': '🇾🇪',
        'KZ': '🇰🇿',
        'KH': '🇰🇭',
        'CA': '🇨🇦',
        'CM': '🇨🇲',
        'CN': '🇨🇳',
        'KP': '🇰🇵',
        'CO': '🇨🇴',
        'CU': '🇨🇺',
        'LV': '🇱🇻',
        'LY': '🇱🇾',
        'LT': '🇱🇹',
        'MG': '🇲🇬',
        'MX': '🇲🇽',
        'MO': '🇲🇨',
        'NL': '🇳🇱',
        'AE': '🇦🇪',
        'PK': '🇵🇰',
        'PL': '🇵🇱',
        'PT': '🇵🇹',
        'KR': '🇰🇷',
        'RU': '🇷🇺',
        'RO': '🇷🇴',
        'RS': '🇷🇸',
        'SG': '🇸🇬',
        'US': '🇺🇸',
        'TJ': '🇹🇯',
        'TH': '🇹🇭',
        'TR': '🇹🇷',
        'TM': '🇹🇲',
        'UZ': '🇺🇿',
        'UA': '🇺🇦',
        'FI': '🇫🇮',
        'FR': '🇫🇷',
        'HR': '🇭🇷',
        'CZ': '🇨🇿',
        'SE': '🇸🇪',
        'JP': '🇯🇵'
    }

    try:
        req = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric'
        )
        data = req.json()

        cur_city = data['name']
        cur_weat = data['main']['temp']
        cur_humidity = data['main']['humidity']
        cur_status = data['weather'][0]['main']
        feels_weat = data['main']['feels_like']
        pressure_weat = data['main']['pressure']
        sunrise_weat = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_weat = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        country = data['sys']['country']
        if country in country_flag:
            country_smile = country_flag[country]
        else:
            country_smile = country
        if cur_status in smiles:
            wd = smiles[cur_status]
        else:
            wd = 'Посмотри в окно'
        return f'Город: {cur_city} {country_smile}\nТемпература: {cur_weat}°С, ощущается как {feels_weat} {wd}\nВлажность воздуха: {cur_humidity}%\nДавление: {pressure_weat} мм.рт.ст\nВосход солнца: {str(sunrise_weat).split()[1]}🌅\nЗакат солнца: {str(sunset_weat).split()[1]}🌇'

    except Exception as ex:
        print(ex)
        return 'Проверьте название города'


token = tk_bot
session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(session)
vk = session.get_api()

for event in longpoll.listen():
    if event.from_chat or event.to_me:
        try:
            msg = event.text.lower()
            textt = event.text
            user = event.user_id
        except:
            continue

        if msg.startswith('погода'):
            city = ''.join(msg.split()[1:])
            mes = get_weat(city, msg.split()[1],  open_weather_token)
            if event.from_chat:
                vk.messages.send(
                    chat_id=event.chat_id,
                    attachment=download_image(city) if mes != 'Проверьте название города' else 'photo622528023_457239094',
                    message=mes,
                    random_id=0
                )
            else:
                vk.messages.send(
                    user_id=event.user_id,
                    attachment=download_image(
                        city) if mes != 'Проверьте название города' else 'photo622528023_457239094',
                    message=mes,
                    random_id=0
                )

            path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                'C:/Users/paket/yandexprojects/ботяра/ImageCrawler')
            shutil.rmtree(path)
            print('Папка удалена.')
            os.mkdir('ImageCrawler')
            print('Новая директория создана.')
            print(msg.split())


