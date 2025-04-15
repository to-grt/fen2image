import unittest
from fen_to_image.FenManager import FenManager

class TestFenManager(unittest.TestCase):
    def setUp(self):
        # A valid FEN string
        self.valid_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    def test_valid_fen(self):
        """Test that a valid FEN does not raise any errors."""
        # Should not raise an exception
        fm = FenManager(self.valid_fen)
        # Calling verify_fen() explicitly should also pass without error.
        fm.verify_fen()

    def test_incorrect_number_of_fields(self):
        """Test that a FEN with an incorrect number of fields raises an error."""
        invalid_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0"  # only 5 fields
        with self.assertRaises(ValueError) as context:
            FenManager(invalid_fen)
        self.assertIn("Incorrect number of fields", str(context.exception))

    def test_incorrect_rank_count(self):
        """Test that a FEN whose first field does not contain exactly 8 ranks is invalid."""
        # First field has only 7 ranks
        invalid_first_field = "rnbqkbnr/pppppppp/8/8/8/PPPPPPPP"
        # Fill in the rest with valid dummy data.
        fen = f"{invalid_first_field} w KQkq - 0 1"
        with self.assertRaises(ValueError) as context:
            FenManager(fen)
        self.assertIn("Incorrect number of ranks", str(context.exception))

    def test_invalid_active_color(self):
        """Test that a FEN with an invalid active color raises an error."""
        invalid_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR x KQkq - 0 1"
        with self.assertRaises(ValueError) as context:
            FenManager(invalid_fen)
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
        invalid_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQ-q - 0 1"
        with self.assertRaises(ValueError) as context:
            FenManager(invalid_fen)
        self.assertIn("Incorrect castling rights", str(context.exception))

    def test_invalid_en_passant_target_length(self):
        """Test that an en passant field with a string of incorrect length raises an error."""
        invalid_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq ee3 0 1"  # Length != 2
        with self.assertRaises(ValueError) as context:
            FenManager(invalid_fen)
        self.assertIn("Incorrect en passant target square. Expected a field of size 2", str(context.exception))

    def test_invalid_en_passant_target_square(self):
        """Test that an en passant target square outside valid board coordinates raises an error."""
        invalid_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq i9 0 1"
        with self.assertRaises(ValueError) as context:
            FenManager(invalid_fen)
        self.assertIn("Incorrect en passant target square. Must be a correct square", str(context.exception))

    def test_invalid_halfmove_clock_non_digit(self):
        """Test that a non-digit halfmove clock raises an error."""
        invalid_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - abc 1"
        with self.assertRaises(ValueError) as context:
            FenManager(invalid_fen)
        self.assertIn("Incorrect half-move clock", str(context.exception))

    def test_invalid_halfmove_clock_negative(self):
        """Test that a negative halfmove clock raises an error."""
        invalid_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - -1 1"
        with self.assertRaises(ValueError) as context:
            FenManager(invalid_fen)
        self.assertIn("Incorrect half-move clock", str(context.exception))

    def test_invalid_fullmove_number_non_digit(self):
        """Test that a non-digit fullmove number raises an error."""
        invalid_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 abc"
        with self.assertRaises(ValueError) as context:
            FenManager(invalid_fen)
        self.assertIn("Incorrect full-move number", str(context.exception))

    def test_invalid_fullmove_number_less_than_one(self):
        """Test that a fullmove number less than 1 raises an error."""
        invalid_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0"
        with self.assertRaises(ValueError) as context:
            FenManager(invalid_fen)
        self.assertIn("Incorrect full-move number", str(context.exception))

    def test_change_fen_valid(self):
        """
        Test that change_fen updates the FEN string and all associated attributes
        correctly when provided a valid new FEN.
        """
        fm = FenManager(self.valid_fen)
        valid_new_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 1 2"
        # Using change_fen on an instance with a valid initial FEN.
        try:
            fm.change_fen(valid_new_fen)
        except ValueError:
            self.fail("change_fen() raised ValueError unexpectedly on valid FEN")
        # Assert that the FEN is updated.
        self.assertEqual(fm.fen, valid_new_fen)
        # Also check that dependent fields are updated (e.g., active color).
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
        # Optionally, ensure that the object's fen attribute now holds the invalid FEN.
        self.assertEqual(fm.fen, invalid_new_fen)


if __name__ == '__main__':
    unittest.main()
