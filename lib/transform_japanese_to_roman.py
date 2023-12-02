import pykakasi

mode = 'kunrei'
kakasi = pykakasi.kakasi() # インスタンスの作成

def convert_to_roman(txt:str)-> str:
    """日本語の文字列をローマ字の文字列に変換する"""
    txt.replace("\n","。")
    conversions = kakasi.convert(txt)
    
    dst = "".join([conversion[mode] for conversion in conversions])
    
    print(dst)
    return dst