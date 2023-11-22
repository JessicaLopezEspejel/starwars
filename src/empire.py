from typing import Dict, List, Union


class Empire:
    def __init__(
        self, countdown: int, bounty_hunters: List[Dict[str, Union[str, int]]]
    ):
        self.countdown = countdown
        self.bounty_hunters = bounty_hunters

    def update_countdown(self, time: int) -> bool:
        self.countdown -= time
        if self.countdown < 0:  # TODO - maybe == 0?
            # print("fail --- " , self.countdown)
            return True
        return False
