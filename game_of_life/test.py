import unittest

from game_of_life import update_state

class GameOfLifeTest(unittest.TestCase):
    def test_check_update_state(self):
        init_state = [
            [0,0,1],
            [0,1,1],
            [0,0,0]
        ]
        expected_next_state = [
            [0,1,1],
            [0,1,1],
            [0,0,0]
        ]
        init_state_2 = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        expected_next_state_2 = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        self.assertEqual(update_state(init_state), expected_next_state)
        self.assertEqual(update_state(init_state_2), expected_next_state_2)

if __name__ == '__main__':
    unittest.main()
