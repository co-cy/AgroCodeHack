from sklearn.metrics.pairwise import cosine_similarity
from pydantic import BaseModel
from fastapi import APIRouter
import numpy as np
import pickle

router = APIRouter()


class Coordinate(BaseModel):
    x: int
    y: int


class MapRequest(BaseModel):
    scale: int
    corners: list[Coordinate]
    pixels: list[Coordinate]


@router.post('/getMap')
def get_map(req: MapRequest):
    data = None
    top_left_x = 0
    top_left_y = 0
    size = 1
    if req.scale == 32:
        with open('./chunks/0_0__4095_4095_32', 'rb') as f:
            data = pickle.load(f)
    elif req.scale == 8:
        top_left_chunk_top_left_x = req.corners[0].x // 1024 * 1024
        top_left_chunk_top_left_y = req.corners[0].y // 1024 * 1024

        bottom_right_chunk_top_left_x = req.corners[1].x // 1024 * 1024
        bottom_right_chunk_top_left_y = req.corners[1].y // 1024 * 1024
        top_left_x = top_left_chunk_top_left_x
        top_left_y = top_left_chunk_top_left_y
        if top_left_chunk_top_left_x == bottom_right_chunk_top_left_x and top_left_chunk_top_left_y == bottom_right_chunk_top_left_y:
            with open(
                    f'./chunks/{top_left_chunk_top_left_x}_{top_left_chunk_top_left_y}__{top_left_chunk_top_left_x + 1023}_{top_left_chunk_top_left_y + 1023}_{req.scale}',
                    'rb') as f:
                data = pickle.load(f)
        else:
            size = 4
            with open(
                    f'./chunks/{top_left_chunk_top_left_x}_{top_left_chunk_top_left_y}__{top_left_chunk_top_left_x + 1023}_{top_left_chunk_top_left_y + 1023}_{req.scale}',
                    'rb') as f:
                data = pickle.load(f)
            top_right_chunk = None
            with open(
                    f'./chunks/{top_left_chunk_top_left_x + 1024}_{top_left_chunk_top_left_y}__{top_left_chunk_top_left_x + 2047}_{top_left_chunk_top_left_y + 1023}_{req.scale}',
                    'rb') as f:
                top_right_chunk = pickle.load(f)
            bottom_left_chunk = None
            with open(
                    f'./chunks/{top_left_chunk_top_left_x}_{top_left_chunk_top_left_y + 1024}__{top_left_chunk_top_left_x + 1023}_{top_left_chunk_top_left_y + 2047}_{req.scale}',
                    'rb') as f:
                bottom_left_chunk = pickle.load(f)
            bottom_right_chunk = None
            with open(
                    f'./chunks/{bottom_right_chunk_top_left_x}_{bottom_right_chunk_top_left_y}__{bottom_right_chunk_top_left_x + 1023}_{bottom_right_chunk_top_left_y + 1023}_{req.scale}',
                    'rb') as f:
                bottom_right_chunk = pickle.load(f)
            data = np.concatenate((data, top_right_chunk), axis=1)
            bottom_left_chunk = np.concatenate((bottom_left_chunk, bottom_right_chunk), axis=1)
            data = np.concatenate((data, bottom_left_chunk), axis=0)
    elif req.scale == 1:
        top_left_chunk_top_left_x = req.corners[0].x // 128 * 128
        top_left_chunk_top_left_y = req.corners[0].y // 128 * 128

        bottom_right_chunk_top_left_x = req.corners[1].x // 128 * 128
        bottom_right_chunk_top_left_y = req.corners[1].y // 128 * 128
        top_left_x = top_left_chunk_top_left_x
        top_left_y = top_left_chunk_top_left_y
        if top_left_chunk_top_left_x == bottom_right_chunk_top_left_x and top_left_chunk_top_left_y == bottom_right_chunk_top_left_y:
            with open(
                    f'./chunks/{top_left_chunk_top_left_x}_{top_left_chunk_top_left_y}__{top_left_chunk_top_left_x + 127}_{top_left_chunk_top_left_y + 127}_{req.scale}',
                    'rb') as f:
                data = pickle.load(f)
        else:
            size = 4
            with open(
                    f'./chunks/{top_left_chunk_top_left_x}_{top_left_chunk_top_left_y}__{top_left_chunk_top_left_x + 127}_{top_left_chunk_top_left_y + 127}_{req.scale}',
                    'rb') as f:
                data = pickle.load(f)
            top_right_chunk = None
            with open(
                    f'./chunks/{top_left_chunk_top_left_x + 128}_{top_left_chunk_top_left_y}__{top_left_chunk_top_left_x + 255}_{top_left_chunk_top_left_y + 127}_{req.scale}',
                    'rb') as f:
                top_right_chunk = pickle.load(f)
            bottom_left_chunk = None
            with open(
                    f'./chunks/{top_left_chunk_top_left_x}_{top_left_chunk_top_left_y + 128}__{top_left_chunk_top_left_x + 127}_{top_left_chunk_top_left_y + 255}_{req.scale}',
                    'rb') as f:
                bottom_left_chunk = pickle.load(f)
            bottom_right_chunk = None
            with open(
                    f'./chunks/{bottom_right_chunk_top_left_x}_{bottom_right_chunk_top_left_y}__{bottom_right_chunk_top_left_x + 127}_{bottom_right_chunk_top_left_y + 127}_{req.scale}',
                    'rb') as f:
                bottom_right_chunk = pickle.load(f)
            data = np.concatenate((data, top_right_chunk), axis=1)
            bottom_left_chunk = np.concatenate((bottom_left_chunk, bottom_right_chunk), axis=1)
            data = np.concatenate((data, bottom_left_chunk), axis=0)
        pass
    else:
        raise ValueError()

    pixels_data = []
    for pixel in req.pixels:
        top_left_chunk_top_left_x = pixel.x // 128 * 128
        top_left_chunk_top_left_y = pixel.y // 128 * 128
        with open(
                f'./chunks/{top_left_chunk_top_left_x}_{top_left_chunk_top_left_y}__{top_left_chunk_top_left_x + 127}_{top_left_chunk_top_left_y + 127}_1',
                'rb') as f:
            pixels_data.append(pickle.load(f)[pixel.x % 128][pixel.y % 128])

    sim = cosine_similarity(pixels_data, data.reshape(-1, data.shape[-1]))
    sim[sim < 0] = 0
    sim = sim.mean(axis=0)
    sim = sim.reshape(data.shape[0], data.shape[1])
    for x in range(data.shape[0]):
        for y in range(data.shape[1]):
            if data[x][y][0] == 0:
                sim[x][y] = -1
            elif data[x][y][7] == 1:
                sim[x][y] = 2
            elif data[x][y][1] == 7:
                sim[x][y] = -2

    return {
        "data": sim.tolist(),
        "params": {
            "top_left_coords": {
                "x": top_left_x,
                "y": top_left_y
            },
            "size": size
        }
    }
