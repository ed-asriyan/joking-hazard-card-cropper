from PIL import Image
from sys import argv, stdout
from os import path


class CardCropper:
    _INIT_POINT = (585, 492)

    _LEFT_OFFSET = 1350
    _TOP_OFFSET = 1905

    _CARD_SIZE = (1244, 1804)

    _BORDER_WIDTH = 29
    _BORDER_RADIUS = 8

    def __init__(self, image):
        if type(image) == str:
            self._image = Image.open(image)
        else:
            self._image = image

    def get_cards(self, mode='border'):
        result = []
        for i in range(9):
            init_point = (
                CardCropper._INIT_POINT[0] + CardCropper._LEFT_OFFSET * (i % 3),
                CardCropper._INIT_POINT[1] + CardCropper._TOP_OFFSET * (i // 3),
            )

            if mode == 'border':
                init = (
                    init_point[0],
                    init_point[1],
                    init_point[0] + CardCropper._CARD_SIZE[0],
                    init_point[1] + CardCropper._CARD_SIZE[1]
                )
            elif mode == 'inner':
                init = (
                    init_point[0] + CardCropper._BORDER_WIDTH,
                    init_point[1] + CardCropper._BORDER_WIDTH,
                    init_point[0] - CardCropper._BORDER_WIDTH + CardCropper._CARD_SIZE[0],
                    init_point[1] - CardCropper._BORDER_WIDTH + CardCropper._CARD_SIZE[1]
                )
            elif mode == 'pure':
                init = (
                    init_point[0] + CardCropper._BORDER_WIDTH + CardCropper._BORDER_RADIUS,
                    init_point[1] + CardCropper._BORDER_WIDTH + CardCropper._BORDER_RADIUS,
                    init_point[0] - CardCropper._BORDER_WIDTH - CardCropper._BORDER_RADIUS +
                    CardCropper._CARD_SIZE[0],
                    init_point[1] - CardCropper._BORDER_WIDTH - CardCropper._BORDER_RADIUS +
                    CardCropper._CARD_SIZE[1],
                )
            else:
                raise Exception("Invalid mode argument. Supported: 'border', 'inner' and 'pure'.")

            result.append(self._image.crop(init))
        return result


def save_path(file_path, index):
    # directory = path.dirname(path)
    name, extension = path.splitext(file_path)
    name = path.basename(name)

    return name + '_' + str(index) + extension


def main():
    mode = 'border'
    for source in argv[1:]:
        if source[:5] == 'mode=':
            mode = source[5:]
            argv.remove(source)
            break

    for source in argv[1:]:
        for crop_index, crop in enumerate(CardCropper(source).get_cards(mode)):
            result_path = save_path(source, crop_index)
            print('Processing ' + result_path + '... ', end='')
            stdout.flush()
            crop.save(result_path)
            print('Done.')


if __name__ == '__main__':
    main()
