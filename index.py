from PIL import Image
from sys import argv


class CardCropper:
    _INIT_POINT = (585, 492)

    _LEFT_OFFSET = 1350
    _TOP_OFFSET = 1905

    _CARD_SIZE = (1244, 1804)

    _BORDER_WIDTH = 10
    _BORDER_RADIUS = 10

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


def main():
    path = argv[1]

    for index, result in enumerate(CardCropper(path).get_cards()):
        result.save(str(index) + '.jpg')


if __name__ == '__main__':
    main()
