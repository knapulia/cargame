import time
import json
import os
import pygame


DATA_FILE = "score_data.json"


class ScoreManager:
    def __init__(self, level):
        self.level = level
        self.start_time = None
        self.score = 0
        self.best_score = self.load_best_score()
        self.font = pygame.font.Font(None, 36)

    def start(self):
        self.start_time = time.time()

    def update(self):
        if self.start_time:
            self.score = round(time.time() - self.start_time, 1)

    def reset(self):
        self.start_time = None
        self.score = 0

    def save_best_score(self):
        try:
            data = self._load_data()
            if self.level not in data or self.score > data[self.level]:
                data[self.level] = self.score
                with open(DATA_FILE, "w") as f:
                    json.dump(data, f)
        except Exception as e:
            print("Error saving score:", e)

    def load_best_score(self):
        try:
            data = self._load_data()
            return data.get(self.level, 0)
        except Exception:
            return 0

    def _load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        return {}

    def draw_score(self, surface):
        score_text = self.font.render(
            f"Score: {self.score}s", True,
            (255, 255, 255)
        )
        best_text = self.font.render(
            f"Best: {self.best_score}s", True,
            (255, 255, 0)
        )
        surface.blit(score_text, (10, 10))
        surface.blit(best_text, (10, 40))
