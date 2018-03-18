from mongoengine import *
import extendfilter.searchfilter as sf
import pytest

class TestSearch():

    def test_ranges(self):
        with pytest.raises(Exception) as e_info:
            sf.Product.objects.ranges(800, 700)

        with pytest.raises(Exception) as e_info:
            sf.Product.objects.ranges('dfg', 700)

        sf.Product.objects.ranges(200,)

