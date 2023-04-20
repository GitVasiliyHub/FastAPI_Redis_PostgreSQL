from fastapi import FastAPI
import uvicorn
from starlette.background import BackgroundTasks

from db.postgres import download_data
from utils.replace_image import base_loader
from utils.utils import subdirectories
from utils.simple_image_download import main as download_img
from config import config


api = FastAPI(title="FastAPI_Redis_PostgreSQL")


@api.patch("/download", status_code=200)
async def download(
        limit: int,
        category: str,
        background_tasks: BackgroundTasks
):
    background_tasks.add_task(download_img, limit=limit, tag=category)

    return 'ok'


@api.patch('/categories', status_code=200)
async def categories():
    sub = subdirectories(path=config.stock)

    return [p.name for p in sub]


@api.patch("/base_loader", status_code=200)
async def run_base_loader(
        category: str,
        background_tasks: BackgroundTasks
):
    background_tasks.add_task(
        base_loader,
        stock=config.stock,
        category=category
    )

    return 'ok'


@api.patch('/show_table', status_code=200)
async def show_table(category: str,):
    dataframe = download_data(sql=f'SELECT * FROM {category}')

    return dataframe.to_json()


if __name__ == "__main__":
    uvicorn.run("app:api", port=8000, host="0.0.0.0", reload=True)
