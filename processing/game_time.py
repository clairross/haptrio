import time


class GameTime:
    __previous_time: int = 0
    __elapsed_game_time: int = 0
    __total_game_time: int = 0

    @staticmethod
    def get_elapsed_game_time():
        current_time = time.perf_counter_ns()
        GameTime.__elapsed_game_time = current_time - GameTime.__previous_time
        GameTime.__previous_time = current_time
        GameTime.__total_game_time += GameTime.__elapsed_game_time
        return GameTime.__elapsed_game_time
