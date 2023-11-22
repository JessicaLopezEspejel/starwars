from typing import Dict, List, Union


class Empire:
    def __init__(
        self, countdown: int, bounty_hunters: List[Dict[str, Union[str, int]]]
    ):
        self.countdown = countdown
        self.bounty_hunters = bounty_hunters

    def update_countdown(self, time: int) -> bool:
        """
        This function takes the number of days to substract from the countdown.
        It returns True if the countdown is negative (failure of the path)
        and False if it is possible to continue navigating it.

        Parameters:
        - time (int): Number of days.

        Returns:
        bool: Failure (True) or not (False).
        """

        self.countdown -= time
        if self.countdown < 0:
            return True
        return False
