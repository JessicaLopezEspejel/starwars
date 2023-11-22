from typing import Dict, List, Tuple, Union


class Path:
    def __init__(self) -> None:
        self._path: List[Tuple[str, int]] = []
        self._k: int = 0
        self._date: int = 0
        self._fail_prob: float = 0.0

    def set_fail_prob(self, prob: float) -> None:
        self._fail_prob = prob

    def get_fail_prob(self) -> float:
        return self._fail_prob

    def add_stop(self, stop: Tuple[str, int]) -> None:
        self._path.append(stop)

    def pop(self) -> None:
        _ = self._path.pop()

    def get_all(self) -> List[Tuple[str, int]]:
        return self._path

    def get_planet_names(self) -> List[str]:
        return [element[0] for element in self._path]

    def update_date(self, time: int) -> None:
        self._date += time

    def update_probability(
        self, dst: str, bounty_hunters: List[Dict[str, Union[str, int]]]
    ) -> None:
        for element in bounty_hunters:
            planet, day = element["planet"], element["day"]

            if dst == planet and self._date == day:
                self._fail_prob += (9**self._k) / (10 ** (self._k + 1))
                self._k += 1
                return
