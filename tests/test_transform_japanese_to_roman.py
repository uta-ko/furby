from lib import transform_japanese_to_roman
from time import time
def test_convert_to_roman():
    japanese = "こんにちは"
    roman = transform_japanese_to_roman.convert_to_roman(japanese)

    assert roman != ""
    return

def test_convert_to_roman():
    japanese = "こんにちは"
    start_time = time()
    roman = transform_japanese_to_roman.convert_to_roman(japanese)
    end_time = time()
    print("spend time: ",end_time - start_time)
    assert roman != ""
    return