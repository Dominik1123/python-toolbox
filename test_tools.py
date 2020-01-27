import pytest

from tools import map_except


class TestMapExcept:
    def test_no_exception(self):
        m = map_except(int, '123', fallback={})
        assert tuple(m) == (1, 2, 3)

    def test_fallback(self):
        m = map_except(int, ['1', 'oops', '3'], fallback={ValueError: 'n/a'})
        assert tuple(m) == (1, 'n/a', 3)

    def test_multiple_fallback(self):
        m = map_except(int, ['1', 'oops', (2, 3)], fallback={ValueError: 'n/a',
                                                             TypeError: 'wrong type'})
        assert tuple(m) == (1, 'n/a', 'wrong type')

    def test_escaping_exception(self):
        m = map_except(int, ['1', (2, 3)], fallback={ValueError: 'n/a'})
        with pytest.raises(TypeError):
            tuple(m)
