from typing import Dict, List, Tuple, Union


class Path:
    def __init__(self) -> None:
        self._path: List[Tuple[str, int]] = []
        self._k: int = 0
        self._date: int = 0
        self._fail_prob: float = 0.0

    def set_fail_prob(self, prob: float) -> None:
        """
        This function takes a probability and set it to the current path.

        Parameters:
        - prob (float): Probability.
        """
        self._fail_prob = prob

    def get_fail_prob(self) -> float:
        """
        This function returns the fail probability of the current path.

        Returns:
        float: fail probability of the current path.
        """
        return self._fail_prob

    def add_stop(self, stop: Tuple[str, int]) -> None:
        """
        This function takes a stop as input and append it to the current path

        Parameters:
        - stop (Tuple[str, int]): Stop (planet, travel_time).
        """
        self._path.append(stop)

    def pop(self) -> None:
        """
        This function pops the first stop in the current path.
        """
        _ = self._path.pop()

    def get_all(self) -> List[Tuple[str, int]]:
        """
        This function returns all the current path.

        Returns:
        List[Tuple[str, int]]: all the current path (list of (planet, travel_time)).
        """
        return self._path

    def get_planet_names(self) -> List[str]:
        """
        This function returns all the planet names of the path

        Returns:
        List[str]: all the planet names of the path.
        """
        return [element[0] for element in self._path]

    def update_date(self, time: int) -> None:
        """
        This function updates the date in the current path with a given number of days.

        Parameters:
        - time (int): number of days.
        """

        self._date += time

    def update_probability(
        self, dst: str, bounty_hunters: List[Dict[str, Union[str, int]]]
    ) -> None:
        """
        This function takes as input a planet name and bounty hunters dictionary
        and updates the probability of millinium being catched in the current path

        Parameters:
        - dst (str): name of planet.
        - bounty_hunters (List[Dict[str, Union[str, int]]]): dictionary of bounty hunters
        """

        for element in bounty_hunters:
            planet, day = element["planet"], element["day"]

            if dst == planet and self._date == day:
                self._fail_prob += (9**self._k) / (10 ** (self._k + 1))
                self._k += 1
                return
