import pytest


class TestCase():
    @pytest.mark.dependency()
    def test001(self):
        assert 1 == 2

    @pytest.mark.dependency(depends=["TestCase:test001"])
    # @pytest.mark.dependency()
    def test002(self):
        assert 1 == 1

    @pytest.mark.dependency(depends=["TestCase:test001"])
    # @pytest.mark.dependency()
    def test003(self):
        assert 1 == 1


if __name__ == '__main__':
    pytest.main(['-vs', __file__])
