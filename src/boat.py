class Boat:
    def __init__(self, autonomy: int):
        self.autonomy = autonomy

    def reduce_autonomy(self, time: int) -> None:
        self.autonomy -= time

    def increase_autonomy(self, time: int) -> None:
        self.autonomy += time
