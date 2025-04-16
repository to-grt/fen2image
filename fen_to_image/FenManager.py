class FenManager:

    def __init__(self, fen: str) -> None:
        """
        Initializes the FenManager with a FEN string.

        :param fen: The FEN string to be managed.
        """
        self.fen = fen
        self.verify_fen()

    def change_fen(self, new_fen: str) -> None:
        """
        Change the fen attributes to the new_fen parameter, then checks new_fen integrity.
        Even if an error is raised during this verification, the new invalid fen will replace to old one.

        :param new_fen: The new FEN string to be managed
        :return:
            None if everything went well, raise an error otherwise
        """
        self.fen = new_fen
        self.verify_fen()

    def verify_fen(self) -> None:
        """
        Verifies the FEN string.

        :return:
            None if all checks passed, raise an error otherwise
        """
        try:
            self._initialize_fields()
            self._check_first_field()
            self._check_second_field()
            self._check_third_field()
            self._check_fourth_field()
            self._check_fifth_field()
            self._check_sixth_field()
        except ValueError as e:
            raise ValueError(e)

    def _initialize_fields(self) -> None:
        """
        Checks the number of fields in the FEN string. A correct FEN must have 6 fields separated by a white space.
        If the number is correct, each field is stored in an attribute

        :return:
            None if the number of fields is correct, raise an error otherwise.
        """
        split_fen = self.fen.split(" ")
        if len(split_fen) != 6:
            raise ValueError(f"Invalid FEN: Incorrect number of fields. Expected 6, got {len(split_fen)}.")
        self.first_field = split_fen[0]
        self.second_field = split_fen[1]
        self.third_field = split_fen[2]
        self.fourth_field = split_fen[3]
        self.fifth_field = split_fen[4]
        self.sixth_field = split_fen[5]


    def _check_first_field(self) -> None:
        """
        Checks the first field of the FEN string. The first field must contain 8 ranks separated by a "/" character.

        :return:
            None if the first field is correct, raise an error otherwise.
        """
        ranks = self.first_field.split("/")
        if len(ranks) != 8:
            raise ValueError(f"Invalid FEN: Incorrect number of ranks. Expected 8, got {len(ranks)}. Field: {self.first_field}")
        correct_characters = "rnbqkpRNBQKP12345678/"
        for char in self.first_field:
            if char not in correct_characters:
                raise ValueError(f"Invalid FEN: Incorrect characters in rank. Expected characters from {correct_characters}, got {char}")


    def _check_second_field(self) -> None:
        """
        Checks the second field of the FEN string. The second field must be either "w" or "b".

        :return:
            None if the second field is correct, raise an error otherwise.
        """
        if self.second_field not in ["w", "b"]:
            raise ValueError(f"Invalid FEN: Incorrect active color. Expected 'w' or 'b', got {self.second_field}")

    def _check_third_field(self) -> None:
        """
        Checks the third field of the FEN string. The third field must be a valid castling rights string.

        :return:
            None if the third field is correct, raise an error otherwise.
        """
        valid_castling_rights = ["K", "Q", "k", "q", "-"]
        if len(self.third_field) > 4:
            raise ValueError(f"Invalid FEN: Incorrect castling rights. Expected rights of the form 'KQkq' or '-', got {self.third_field}")
        if len(set(self.third_field)) != len(self.third_field):
            raise ValueError(f"Invalid FEN: Incorrect castling rights. Castling rights must be unique, got {self.third_field}")
        for char in self.third_field:
            if char not in valid_castling_rights:
                raise ValueError(f"Invalid FEN: Incorrect castling rights. Expected rights of the form 'KQkq' or '-', got {self.third_field}")
        if "-" in self.third_field and self.third_field != "-":
            raise ValueError(f"Invalid FEN: Incorrect castling rights. Expected rights of the form 'KQkq' or '-', got {self.third_field}")

    def _check_fourth_field(self) -> None:
        """
        Checks the fourth field of the FEN string. The fourth field must be a valid en passant target square.

        :return:
            None if the fourth field is correct, raise an error otherwise.
        """
        en_passant_target = self.fourth_field
        if en_passant_target == "-":
            return
        if len(en_passant_target) != 2:
            raise ValueError(f"Invalid FEN: Incorrect en passant target square. Expected a field of size 2, got {len(en_passant_target)}: {en_passant_target}")
        if en_passant_target[0] not in 'abcdefgh' or en_passant_target[1] not in '12345678':
            raise ValueError(f"Invalid FEN: Incorrect en passant target square. Must be a correct square, got {en_passant_target}")

    def _check_fifth_field(self) -> None:
        """
        Checks the fifth field of the FEN string. The fifth field must be a valid halfmove clock.

        :return:
            None if the fifth field is correct, raise an error otherwise.
        """
        if not self.fifth_field.isdigit() or int(self.fifth_field) < 0:
            raise ValueError(f"Invalid FEN: Incorrect half-move clock. Expected a digit superior or equal to 0, got {self.fifth_field}")

    def _check_sixth_field(self) -> None:
        """
        Checks the sixth field of the FEN string. The sixth field must be a valid fullmove number.

        :return:
            True if the sixth field is correct, raise an error otherwise.
        """
        if not self.sixth_field.isdigit() or int(self.sixth_field) < 1:
            raise ValueError(f"Invalid FEN: Incorrect full-move number. Expected a digit superior to 0, got {self.sixth_field}")