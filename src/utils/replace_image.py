from threading import Thread
from pathlib import Path
from io import BytesIO

import pandas as pd
from PIL import Image

from config import config
from db.postgres import engine
from db.redis import RedisClient
from utils.utils import file_paths, time_now, delete_folder


class ImageLoader:
    def __init__(
            self,
            stock: Path,
            category: str = None
    ):
        self.category = category
        self.stock = stock
        self.redis_client = RedisClient()

    def __call__(self):
        if self.category:
            self.stock = self.stock / self.category

        with self.redis_client.client as client:

            for file_path in file_paths(self.stock):
                img_byte_arr = BytesIO()
                image = Image.open(file_path)
                image.save(img_byte_arr, format=image.format)

                client.lpush('images', img_byte_arr.getvalue())
                img_byte_arr.close()
                print('saved')

        delete_folder(self.stock)
        print(f'Директория {self.stock} удалена')
        self.redis_client.close_connection()


class ImageDownloader:
    def __init__(self, category: str):
        self.redis_client = RedisClient()
        self.pg_engine = engine
        self.category = category

    def __call__(self):
        create = True

        with self.redis_client.client as client:
            while True:
                img_byte_arr = client.brpop('images', 3)

                if img_byte_arr is None:
                    print('Время ожидания истекло')
                    return

                image = Image.open(BytesIO(img_byte_arr[1]))

                dataframe = pd.DataFrame({
                    'datetime': [time_now()],
                    'size': [image.size],
                    'format': [image.format]
                })
                if create:
                    status = 'replace'
                    create = False
                else:
                    status = 'append'
                print(dataframe)
                dataframe.to_sql(
                    self.category,
                    con=engine,
                    if_exists=status,
                    index=False
                )
                print('download')


def base_loader(stock, category):
    thread1 = Thread(target=ImageLoader(stock=stock, category=category))
    thread2 = Thread(target=ImageDownloader(category=category))

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()


if __name__ == '__main__':
    base_loader(stock=config.stock, category='cats')
