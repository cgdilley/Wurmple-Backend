
from typing import Tuple, Dict, Optional, List, Iterable, Callable, Collection
import random

from Data import *


class Generator:

    def __init__(self, data: PokemonMap,
                 length: int,
                 typing_limit: int,
                 type_limit: int,
                 allow_monotype: bool,
                 random_seed: Optional[int] = None):
        self._data = data
        self._length = length
        self._typing_limit = typing_limit
        self._type_limit = type_limit
        self._allow_monotype = allow_monotype
        self._rand = random.Random() if random_seed is None else random.Random(random_seed)
        if self._length <= 0:
            raise Exception("Invalid sequence length")

    #

    def generate(self) -> Tuple[Pokemon, ...]:
        seq = self._finish_sequence(tuple())
        if seq is None:
            raise Exception("Could not generate a valid sequence with the generator's criteria.")
        return seq

    #

    def _finish_sequence(self, sequence: Tuple[Pokemon, ...]) -> Optional[Tuple[Pokemon, ...]]:
        if len(sequence) >= self._length:
            return sequence

        if len(sequence) > 0:
            pok = sequence[-1]
            matches = [p for p in self._data.type(*pok.typing) if self._meets_criteria(p, sequence)]
        else:
            matches = [p for p in self._data if self._meets_criteria(p, [])]
        self._rand.shuffle(matches)

        for match in matches:
            seq = self._finish_sequence(sequence + (match,))
            if seq is not None:
                return seq

        return None

    #

    def _meets_criteria(self, pokemon: Pokemon, sequence: Collection[Pokemon]):
        if not self._allow_monotype and len(pokemon.typing) == 1:
            return False
        if 0 < self._typing_limit <= [x.typing for x in sequence].count(pokemon.typing):
            return False
        for pokemon_type in pokemon.typing:
            if 0 < self._type_limit <= [t for x in sequence for t in x.typing].count(pokemon_type):
                return False
        return True
