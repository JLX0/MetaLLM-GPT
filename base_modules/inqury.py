import time
import openai


class GPT_turbo():

    def __init__(self, key, initial_start_time=0):
        self.previous_start = initial_start_time

        openai.api_key = key

    @staticmethod
    def find_string_in_the_middle(the_string):
        try:
            sub1 = "```python"
            idx1 = the_string.index(sub1)
        except:
            try:
                sub1 = "```"
                idx1 = the_string.index(sub1)
            except:
                sub1 = "``` python"
                idx1 = the_string.index(sub1)
        sub2 = "```"
        idx2 = the_string.index(sub2, idx1 + 1, )
        res = the_string[idx1 + len(sub1) + 1: idx2]
        return res

    def set_initial_time(self):
        self.previous_start = time.time()

    def control_inquiry_frequency(self, minimum_time_interval=20):

        current_start = time.time()
        time_left = minimum_time_interval - (current_start - self.previous_start)
        if time_left >= 0:
            time.sleep(time_left + 0.1)

        self.previous_start = time.time()
