#@title Библиотеки

#!pip install torch torchvision
#!pip install -U git+https://github.com/luca-medeiros/lang-segment-anything.git



#!pip install ultralytics

from IPython import display
display.clear_output()
#import ultralytics
#ultralytics.checks()
#from ultralytics import YOLO

#import moviepy
#from moviepy.editor import *
#from moviepy.editor import VideoFileClip
from IPython.display import display, clear_output, Image
import os
#import gdown
import zipfile

#from lang_sam import LangSAM

from PIL import Image as ImagePIL
import matplotlib.pyplot as plt
#import cv2
import numpy as np
import glob

# YOLO =================================================

def load_video_i(url):
    output = "video.zip"

    # Проверяем, существует ли архив ves.zip
    if os.path.exists(output):
        # Если архив существует, удаляем его
        os.remove(output)

    # Скачиваем zip архив
    #gdown.download(url, output, quiet=False)

    # Распаковываем архив в текущую директорию
    with zipfile.ZipFile(output, 'r') as zip_ref:
        zip_ref.extractall()


def load_weights(url):
    output = "ves.zip"

    # Проверяем, существует ли архив ves.zip
    if os.path.exists(output):
        # Если архив существует, удаляем его
        os.remove(output)

    # Скачиваем zip архив
    #gdown.download(url, output, quiet=False)

    # Распаковываем архив в текущую директорию
    with zipfile.ZipFile(output, 'r') as zip_ref:
        zip_ref.extractall()

    print("\n Веса загружены!")


def load_dataset(url):

    output = "archive.zip"

    # Проверяем, существует ли архив archive.zip
    if os.path.exists(output):
        # Если архив существует, удаляем его
        os.remove(output)

    # Скачиваем zip архив
    #gdown.download(url, output, quiet=False)

    # Распаковываем архив в текущую директорию
    with zipfile.ZipFile(output, 'r') as zip_ref:
        zip_ref.extractall()

    print("\n Датасет загружен!")

'''
#люди и машины
def yolo_detect_person():
    !yolo task=detect mode=predict model=yolov8n.pt conf=0.6 source=/content/IMG_luki.mp4 save=True

#пешеходные переходы
def yolo_detect_perehod():
    !yolo task=detect mode=predict model=/content/best_perehod_segment.pt conf=0.2 source=/content/IMG_20231028_151652_597.mp4 save=True

#тротуары
def yolo_detect_trotuar():
    !yolo task=detect mode=predict model=/content/best_trotuar_500_150ep_m.pt conf=0.5 source=/content/IMG_20231028_150852_876.mp4 save=True


#тротуары
def yolo_detect_trotuar_asfalt():
    !yolo task=detect mode=predict model=/content/best_trotuar_500_150ep_m.pt conf=0.5 source=/content/IMG_20231028_013203_037.mp4 save=True
'''

#!pip install ultralytics

from IPython import display
display.clear_output()

#import ultralytics
#ultralytics.checks()

from IPython.display import display, Image

#from ultralytics import YOLO



# SAM ===============================

#!pip install torch torchvision
#!pip install -U git+https://github.com/luca-medeiros/lang-segment-anything.git




#model = LangSAM()

def segment_LangSAM(image_path, text_prompt, random_color=False):

    def display_results(image, masks, random_color):

        def show_mask(mask, ax, random_color):
            if random_color:
                color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
            else:
                color = np.array([30/255, 144/255, 255/255, 0.6])
            h, w = mask.shape[-2:]
            mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
            ax.imshow(mask_image)

        plt.figure(figsize=(16, 16))
        source_img_ax, segmented_img_ax = plt.subplot(1, 2, 1), plt.subplot(1, 2, 2)

        source_img_ax.set_title('Исходное изображение')
        source_img_ax.axis('off')
        source_img_ax.imshow(image)

        segmented_img_ax.set_title('Сегментированное изображение')
        segmented_img_ax.axis('off')
        segmented_img_ax.imshow(image)

        for mask in masks:
            show_mask(mask, plt.gca(), random_color)

    image_PIL = ImagePIL.open(image_path).convert("RGB")
    #masks, boxes, phrases, logits = model.predict(image_PIL, text_prompt)

    #image_bgr = cv2.imread(image_path)
    #image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    #display_results(image_rgb, masks, random_color)

    return 0 #masks, boxes, phrases, logits


test_prompt = 'sidewalk.crosswalk.person.car.bus stop.bus.urn.pothole.address plate' # тротуар.переход.человек.автомобиль.автобусная остановка.автобус.урна.выбоина.адресная табличка
'''
# sidewalk

!wget -q https://narodfm.ru/images/novosti/medium/cb10d9f5d6a57f582b37706624029ba4.jpg -O sidewalk_1.jpg
sidewalk_1_path = '/content/sidewalk_1.jpg'

!wget -q https://img3.teletype.in/files/2f/12/2f1297cb-bd1d-48b4-940d-5ae47ebbe3b3.jpeg -O sidewalk_2.jpg
sidewalk_2_path = '/content/sidewalk_2.jpg'

!wget -q https://vr-vyksa.ru/media/images/DSC_0797_RuFxVFe.width-1600.watermark-lb-10x10-0.6.jpg -O sidewalk_3.jpg
sidewalk_3_path = '/content/sidewalk_3.jpg'

!wget -q https://upload.wikimedia.org/wikipedia/commons/6/60/Sidewalk_with_bike_path.JPG -O sidewalk_4.jpg
sidewalk_4_path = '/content/sidewalk_4.jpg'

!wget -q https://st1.stpulscen.ru/images/product/040/380/958_medium2.jpg -O sidewalk_5.jpg
sidewalk_5_path = '/content/sidewalk_5.jpg'

sidewalk = [sidewalk_1_path, sidewalk_2_path, sidewalk_3_path, sidewalk_4_path, sidewalk_5_path]

# crosswalk

!wget -q https://www.shadr.info/news/2020/05/03/17023-img-ylo5kh-680x453.jpg -O crosswalk_1.jpg
crosswalk_1_path = '/content/crosswalk_1.jpg'

!wget -q https://s0.rbk.ru/v6_top_pics/media/img/2/17/756368150320172.jpg -O crosswalk_2.jpg
crosswalk_2_path = '/content/crosswalk_2.jpg'

!wget -q https://www.avtovzglyad.ru/media/article/0_Hv9w5tB.jpg.740x555_q85_box-0%2C0%2C980%2C735_crop_detail_upscale.jpg -O crosswalk_3.jpg
crosswalk_3_path = '/content/crosswalk_3.jpg'

!wget -q https://vlpravda.ru/wp-content/uploads/2022/04/99_full-735x400.jpg -O crosswalk_4.jpg
crosswalk_4_path = '/content/crosswalk_4.jpg'


crosswalk = [crosswalk_1_path, crosswalk_2_path, crosswalk_3_path, crosswalk_4_path]

# person

!wget -q https://s0.rbk.ru/v6_top_pics/media/img/1/66/756401567970661.jpg -O person_1.jpg
person_1_path = '/content/person_1.jpg'

!wget -q https://ss.sport-express.ru/userfiles/materials/169/1696394/volga.jpg -O person_2.jpg
person_2_path = '/content/person_2.jpg'

!wget -q https://admnvrsk.ru/upload/resize_cache/iblock/47b/865_497_2/euyeqnevrqlv01177vxvbzk2kxco87ee.jpg -O person_3.jpg
person_3_path = '/content/person_3.jpg'

!wget -q https://riamo.ru/files/image/04/63/76/gallery!6n7.png -O person_4.jpg
person_4_path = '/content/person_4.jpg'

person = [person_1_path, person_2_path, person_3_path, person_4_path]

# car

!wget -q https://sanantonioreport.org/wp-content/uploads/2022/03/nickwagner-pedestrians-sidewalk-san-pedro-ave-09MAR22-2.jpg -O car_1.jpg
car_1_path = '/content/car_1.jpg'

!wget -q https://assets.bwbx.io/images/users/iqjWHBFdfxIU/iPrDvyGApPiI/v1/1200x1202.jpg -O car_2.jpg
car_2_path = '/content/car_2.jpg'

!wget -q https://newyorkparkingticket.com/wp-content/uploads/2019/12/Myrna-NYC-sidewalk-parking-ticket2.jpeg -O car_3.jpg
car_3_path = '/content/car_3.jpg'

!wget -q https://nacto.org/wp-content/themes/sink_nacto/views/design-guides/retrofit/urban-street-design-guide/images/sidewalks/carousel//retail-sidewalk.jpg -O car_4.jpg
car_4_path = '/content/car_4.jpg'


car = [car_1_path, car_2_path, car_3_path, car_4_path]

# bus_stop

!wget -q https://test.merdi.ru/upload/userfiles/22092020/images/f154836a13f1d413ed1d81bc1e43cc46.jpg -O bus_stop_1.jpg
bus_stop_1_path = '/content/bus_stop_1.jpg'

!wget -q https://static.tildacdn.com/tild3162-6635-4530-a438-663462613038/atw1e8ej6ee.jpg -O bus_stop_2.jpg
bus_stop_2_path = '/content/bus_stop_2.jpg'

!wget -q https://i.ytimg.com/vi/8ebqyFMxVE4/maxresdefault.jpg -O bus_stop_3.jpg
bus_stop_3_path = '/content/bus_stop_3.jpg'

!wget -q https://www.oknamedia.ru/system/uploads/photo/photo/484/48415/wallpaper_Screenshot_1.jpg -O bus_stop_4.jpg
bus_stop_4_path = '/content/bus_stop_4.jpg'

bus_stop = [bus_stop_1_path, bus_stop_2_path, bus_stop_3_path, bus_stop_4_path]

# bus

!wget -q https://upload.wikimedia.org/wikipedia/commons/0/03/LiAZ-5292_Ryazan.jpg -O bus_1.jpg
bus_1_path = '/content/bus_1.jpg'

!wget -q https://arbuztoday.ru/wp-content/uploads/2022/12/2022-12-18-12-12-34.jpg -O bus_2.jpg
bus_2_path = '/content/bus_2.jpg'

!wget -q https://msknovosti.ru/wp-content/uploads/2021/11/img_0768-870x400.jpg -O bus_3.jpg
bus_3_path = '/content/bus_3.jpg'

!wget -q https://cdn.iportal.ru/news/2015/99/preview/aa9ea7e236411206416b005445248d8b08b363e3_2048_1365_c.jpg -O bus_4.jpg
bus_4_path = '/content/bus_4.jpg'

bus = [bus_1_path, bus_2_path, bus_3_path, bus_4_path]


# urn

!wget -q https://riamo.ru/files/image/14/95/61/-gallery!0d4n.jpeg -O urn_1.jpg
urn_1_path = '/content/urn_1.jpg'

!wget -q https://gorodmaf.ru/wp-content/uploads/2023/06/zhhzhzhzhz.jpg -O urn_2.jpg
urn_2_path = '/content/urn_2.jpg'

!wget -q https://hozotdel.ru/wa-data/public/shop/products/07/48/4807/images/19798/19798.970.jpg -O urn_3.jpg
urn_3_path = '/content/urn_3.jpg'

!wget -q https://italianet23.ru/wp-content/uploads/2020/10/urna-dlya-musora-kil-04.jpg -O urn_4.jpg
urn_4_path = '/content/urn_4.jpg'


urn = [urn_1_path, urn_2_path, urn_3_path, urn_4_path]


# pothole

!wget -q http://www.razruha.org/data/media/55/1497131081e8b.jpg -O pothole_1.jpg
pothole_1_path = '/content/pothole_1.jpg'

!wget -q http://www.razruha.org/data/media/55/16607260462f8.jpg -O pothole_2.jpg
pothole_2_path = '/content/pothole_2.jpg'

!wget -q https://24.kg/files/media/267/267981.JPG -O pothole_3.jpg
pothole_3_path = '/content/pothole_3.jpg'

!wget -q https://pravdapfo.ru/sites/default/files/0_83411_a35b8b06_xl.jpg -O pothole_4.jpg
pothole_4_path = '/content/pothole_4.jpg'


pothole = [pothole_1_path, pothole_2_path, pothole_3_path, pothole_4_path]

# address_plate

!wget -q https://ugra.ru/pics-newtambov.ru/storage/taisia/2016/02/IMG_7050.jpg -O address_plate_1.jpg
address_plate_1_path = '/content/address_plate_1.jpg'

!wget -q https://foto.cheb.ru/foto/foto.cheb.ru-254664.jpg -O address_plate_2.jpg
address_plate_2_path = '/content/address_plate_2.jpg'

!wget -q https://upload.cheb.ru/uploads/397716/PkB61tY5ciN2F8f4y2yX8A==/fullview/img_8943.jpg -O address_plate_3.jpg
address_plate_3_path = '/content/address_plate_3.jpg'

!wget -q https://foto.cheb.ru/foto/foto.cheb.ru-252159.jpg -O address_plate_4.jpg
address_plate_4_path = '/content/address_plate_4.jpg'
'''

#address_plate = [address_plate_1_path, address_plate_2_path, address_plate_3_path, address_plate_4_path]