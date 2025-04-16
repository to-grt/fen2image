from PIL import Image
from typing import List

from .constants import piece_to_filename, PATH_RESULT
from .utils import get_list_available_pieces, get_list_available_boards, get_dict_available_boards, get_dict_available_pieces


class BoardRepresentation:
    def __init__(
        self,
        board: List,
        color_turn: str,
        castling_rights: str,
        en_passant: str,
        half_move_count: int,
        full_move_count: int
    ):
        self.board: List = board
        self.color_turn: str = color_turn
        self.castling_rights: str = castling_rights
        self.en_passant: str = en_passant
        self.half_move_count: int = half_move_count
        self.full_move_count: int = full_move_count

    def create_image(self, pieces_design: str = "classic", board_design: str = "wood") -> Image:
        """
        Create an image of the board representation.

        :param pieces_design: The design of the pieces.
        :param board_design: The design of the board.
        """
        self._verify_designs(pieces_design, board_design)
        board_path = get_dict_available_boards()[board_design]
        pieces_path = get_dict_available_pieces()[pieces_design]

        board = Image.open(board_path).convert("RGBA")
        square_size = board.width // 8
        composite = board.copy()

        for index_row, row in enumerate(self.board):
            index_col = 0
            for char in row:
                if char.isdigit():
                    index_col += int(char)
                    continue
                elif char == ".":
                    index_col += 1
                    continue
                else:  # should be a piece
                    piece_path = pieces_path / piece_to_filename[char]
                    piece = Image.open(piece_path).convert("RGBA").resize((square_size, square_size), Image.LANCZOS)
                    position = ((index_col * square_size)-1, (index_row * square_size)-0)
                    composite.paste(piece, position, piece)
                    index_col += 1

        composite.save(PATH_RESULT / "result.png")
        return composite


    def _verify_designs(self, pieces_design: str, board_design: str) -> None:
        """
        Verify if the designs are available.

        :param pieces_design: The design of the pieces.
        :param board_design: The design of the board.
        """
        if pieces_design not in get_list_available_pieces():
            raise ValueError(f"Pieces design '{pieces_design}' is not available. Available designs are: {get_list_available_pieces()}")

        if board_design not in get_list_available_boards():
            raise ValueError(f"Board design '{board_design}' is not available. Available designs are: {get_list_available_boards()}")