"""
test_logic.py
"""

from logic import print_time

def test_print_time(capsys, freezer):
    # Arrange
    freezer.move_to('2017-05-20 00:00:01')

    # Act
    print_time()

    captured = capsys.readouterr()
    # Assert
    assert captured.out == '2017-05-20 00:00:01\n'