from lib import get_audio
from pathlib import Path

def test_get_audio():
    savename = "test_record"
    get_audio.record(savename=savename)
    assert Path("out_audio").joinpath(savename+".wav").exists() == True
    return
