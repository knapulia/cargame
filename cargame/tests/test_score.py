import time
import json
from cargame.score import ScoreManager
import os


def test_score_timing(tmp_path, monkeypatch):
    fake_file = tmp_path / "fake_score.json"
    monkeypatch.setattr("cargame.score.DATA_FILE", str(fake_file))

    s = ScoreManager("easy")
    s.start()
    time.sleep(0.1)
    s.update()
    assert s.score >= 0.1

    s.save_best_score()
    assert os.path.exists(fake_file)
    with open(fake_file) as f:
        data = json.load(f)
        assert "easy" in data
        assert isinstance(data["easy"], float)
