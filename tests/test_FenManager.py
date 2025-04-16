import unittest
from fen_to_image.FenManager import FenManager

class TestFenManager(unittest.TestCase):
    def setUp(self):
        self.valid_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    def test_valid_fen(self):
        """Test that a valid FEN does not raise any errors."""
        FenManager("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        FenManager("r1bqkbnr/pppppppp/n7/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        FenManager("8/8/8/8/8/8/8/8 w - - 0 1")
        fm = FenManager(self.valid_fen)
        fm.verify_fen()

    def test_incorrect_number_of_fields(self):
        """Test that a FEN with an incorrect number of fields raises an error."""
        with self.assertRaises(ValueError) as context:
            FenManager("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0")  # only 5 fields
        self.assertIn("Incorrect number of fields", str(context.exception))

        with self.assertRaises(ValueError) as context:
            FenManager("8/8/8/8/8/8/8/8 w -")  # Only 3 fields
        self.assertIn("Incorrect number of fields", str(context.exception))

        with self.assertRaises(ValueError) as context:
            FenManager("8/8/8/8/8/8/8/8 w - - 0 1 extra")  # 7 fields
        self.assertIn("Incorrect number of fields", str(context.exception))

    def test_incorrect_rank_count(self):
        with self.assertRaises(ValueError) as context:
            FenManager("rnbqkbnr/pppppppp/8/8/8/PPPPPPPP w KQkq - 0 1")
        self.assertIn("Incorrect number of ranks", str(context.exception))

        with self.assertRaises(ValueError) as context:
            FenManager("rnbqkbn/pppppppp/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.assertIn("Incorrect number of ranks", str(context.exception))

        with self.assertRaises(ValueError) as context:
            FenManager("rnbqkbnrr/pppppppp/8/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.assertIn("Incorrect number of ranks", str(context.exception))

        with self.assertRaises(ValueError) as context:
            FenManager("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNX w KQkq - 0 1")
        self.assertIn("Incorrect characters in rank", str(context.exception))

    def test_invalid_active_color(self):
        """Test that a FEN with an invalid active color raises an error."""
        with self.assertRaises(ValueError) as context:
            FenManager("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR x KQkq - 0 1")
        self.assertIn("Incorrect active color", str(context.exception))

        with self.assertRaises(ValueError) as context:
            FenManager("8/8/8/8/8/8/8/8 W - - 0 1")
        self.assertIn("Incorrect active color", str(context.exception))

    def test_invalid_castling_rights_character(self):
        """Test that a FEN with an illegal character in the castling rights field raises an error."""
        invalid_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQXq - 0 1"
        with self.assertRaises(ValueError) as context:
            FenManager(invalid_fen)
        self.assertIn("Incorrect castling rights", str(context.exception))

    def test_invalid_castling_rights_hyphen_usage(self):
        """
        Test that a FEN with a castling rights field containing '-' along with
        other characters raises an error.
        """
        with self.assertRaises(ValueError) as context:
            FenManager("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQ-q - 0 1")
        self.assertIn("Incorrect castling rights", str(context.exception))

        with self.assertRaises(ValueError) as context:
            FenManager("8/8/8/8/8/8/8/8 w QQ - 0 1")  # wrong because double Q
        self.assertIn("Incorrect castling rights", str(context.exception))

        # Valid castling rights
        FenManager("8/8/8/8/8/8/8/8 w - - 0 1")
        FenManager("8/8/8/8/8/8/8/8 w KQkq - 0 1")

    def test_en_passant_target_length(self):
        """Test that an en passant field with a string of incorrect length raises an error."""
        with self.assertRaises(ValueError) as context:
            FenManager("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq ee3 0 1")
        self.assertIn("Incorrect en passant target square. Expected a field of size 2", str(context.exception))

        # Valid en passant target squares
        FenManager("8/8/8/8/8/8/8/8 w - - 0 1")
        FenManager("8/8/8/8/8/8/8/8 w - e3 0 1")

    def test_invalid_en_passant_target_square(self):
        """Test that an en passant target square outside valid board coordinates raises an error."""
        with self.assertRaises(ValueError) as context:
            FenManager("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq i9 0 1")
        self.assertIn("Incorrect en passant target square. Must be a correct square", str(context.exception))

        with self.assertRaises(ValueError) as context:
            FenManager("8/8/8/8/8/8/8/8 w - h9 0 1")
        self.assertIn("Incorrect en passant target square. Must be a correct square", str(context.exception))

        with self.assertRaises(ValueError) as context:
            FenManager("8/8/8/8/8/8/8/8 w - z3 0 1")
        self.assertIn("Incorrect en passant target square. Must be a correct square", str(context.exception))

    def test_halfmove_clock_non_digit(self):
        """Test that a non-digit halfmove clock raises an error."""
        with self.assertRaises(ValueError) as context:
            FenManager("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - abc 1")
        self.assertIn("Incorrect half-move clock", str(context.exception))

        with self.assertRaises(ValueError) as context:
            FenManager("8/8/8/8/8/8/8/8 w - - x 1")
        self.assertIn("Incorrect half-move clock", str(context.exception))

        # Valid halfmove clocks
        FenManager("8/8/8/8/8/8/8/8 w - - 0 1")

    def test_invalid_halfmove_clock_negative(self):
        """Test that a negative halfmove clock raises an error."""
        with self.assertRaises(ValueError) as context:
            FenManager("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - -1 1")
        self.assertIn("Incorrect half-move clock", str(context.exception))

        with self.assertRaises(ValueError) as context:
            FenManager("8/8/8/8/8/8/8/8 w - - -100 1")
        self.assertIn("Incorrect half-move clock", str(context.exception))

    def test_fullmove_number_non_digit(self):
        """Test that a non-digit fullmove number raises an error."""
        with self.assertRaises(ValueError) as context:
            FenManager("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 abc")
        self.assertIn("Incorrect full-move number", str(context.exception))

        with self.assertRaises(ValueError) as context:
            FenManager("8/8/8/8/8/8/8/8 w - - 0 x")
        self.assertIn("Incorrect full-move number", str(context.exception))

        # Valid fullmove numbers
        FenManager("8/8/8/8/8/8/8/8 w - - 0 1")

    def test_invalid_fullmove_number_less_than_one(self):
        """Test that a fullmove number less than 1 raises an error."""
        with self.assertRaises(ValueError) as context:
            FenManager("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0")
        self.assertIn("Incorrect full-move number", str(context.exception))

        with self.assertRaises(ValueError) as context:
            FenManager("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 -100")
        self.assertIn("Incorrect full-move number", str(context.exception))

    def test_change_fen_valid(self):
        """
        Test that change_fen updates the FEN string and all associated attributes
        correctly when provided a valid new FEN.
        """
        fm = FenManager(self.valid_fen)
        valid_new_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 1 2"
        try:
            fm.change_fen(valid_new_fen)
        except ValueError:
            self.fail("change_fen() raised ValueError unexpectedly on valid FEN")
        self.assertEqual(fm.fen, valid_new_fen)
        self.assertEqual(fm.second_field, "b")

    def test_change_fen_invalid(self):
        """
        Test that change_fen raises a ValueError when provided an invalid new FEN.
        After calling change_fen with an invalid FEN, the instance's fen attribute is updated,
        but verify_fen should raise an error.
        """
        fm = FenManager(self.valid_fen)
        invalid_new_fen = "invalid_fen_value"
        with self.assertRaises(ValueError) as context:
            fm.change_fen(invalid_new_fen)
        self.assertIn("Invalid FEN", str(context.exception))
        self.assertEqual(fm.fen, invalid_new_fen)

if __name__ == '__main__':
    unittest.main()
