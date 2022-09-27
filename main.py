from PIL import Image
import numpy as np


def open_picture(path: str, size=None) -> np.ndarray:
    im = Image.open(path).convert('L')

    if size:
        im = im.resize(size)

    im = np.asanyarray(im)

    threshold = im.itemsize * np.iinfo(np.uint8).max / 2
    im_bool = im > threshold

    return im_bool


def save_picture(image: np.ndarray, path: str) -> None:
    Image.fromarray(image).save(path)


def make_nonogram(image: np.ndarray):
    nonograms = {'rows': {}, 'lines': {}}
    y, x = np.where(image == 0)

    # rows
    for i in set(y):
        indexes = np.uint(np.where(y == i))
        row_blacks = x[indexes[0][0]:indexes[0][-1] + 1]
        nonograms['rows'][i] = line_to_nonogram(row_blacks)

    # lines
    for i in set(x):
        indexes = np.uint(np.where(x == i))
        line_blacks = y[indexes[0][0]:indexes[0][-1] + 1]
        nonograms['lines'][i] = line_to_nonogram(line_blacks)

    return nonograms


def line_to_nonogram(indexes: np.array) -> list:
    if len(indexes) < 2:
        return [len(indexes)]

    nonogram = []
    for i in indexes:
        if i - 1 in indexes:
            nonogram[-1] += 1
        else:
            nonogram.append(1)

    return nonogram


def main():
    picture = open_picture('picture.jpg', size=(20, 20))
    nonograms = make_nonogram(picture)
    save_picture(picture, 'picture_grey.png')


if __name__ == '__main__':
    main()
