class Boat:
    def __init__(self, autonomy: int):
        self.autonomy = autonomy

    def reduce_autonomy(self, time: int) -> None:
        """
        This function takes the number of days to substract from the autonomy.

        Parameters:
        - time (int): Number of days.
        """
        self.autonomy -= time

    def increase_autonomy(self, time: int) -> None:
        """
        This function takes the number of days to add to the autonomy.

        Parameters:
        - time (int): Number of days.
        """
        self.autonomy += time
