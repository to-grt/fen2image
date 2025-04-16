from .Fen import Fen
from PIL import Image


def fen_to_image(fen: str) -> Image:
    """
    Convert a FEN string to an image.

    :param fen: the FEN string
    :return: the image
    """

    fen = Fen(fen)
    print(f"fen: {fen}")
    board = fen.to_board_representation()
    return board.create_image()