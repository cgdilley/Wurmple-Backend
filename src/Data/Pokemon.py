from __future__ import annotations

from typing import List, Dict, Collection, Set, Tuple, Union, Optional, Iterable, Iterator, Hashable, Callable
from enum import Enum
import random
import csv

from Utilty.DictUtils import add_or_append


class PokemonType(Enum):
    NORMAL = "Normal"
    FIRE = "Fire"
    WATER = "Water"
    GRASS = "Grass"
    ELECTRIC = "Electric"
    ICE = "Ice"
    FIGHTING = "Fighting"
    POISON = "Poison"
    GROUND = "Ground"
    FLYING = "Flying"
    PSYCHIC = "Psychic"
    BUG = "Bug"
    ROCK = "Rock"
    GHOST = "Ghost"
    DARK = "Dark"
    DRAGON = "Dragon"
    STEEL = "Steel"
    FAIRY = "Fairy"


class Typing(Hashable, Iterable[PokemonType]):

    def __init__(self, *types: PokemonType):
        self.types = tuple(sorted(set(types), key=lambda t: t.name))
        if not (0 < len(self.types) <= 2):
            raise Exception(f"Invalid typing: [{','.join(t.name for t in self.types)}]")

    def __eq__(self, other) -> bool:
        return isinstance(other, Typing) and self.types == other.types

    def __hash__(self) -> int:
        return hash(self.types)

    def __contains__(self, t: PokemonType) -> bool:
        return t in self.types

    def __iter__(self) -> Iterator[PokemonType]:
        return iter(self.types)

    def __len__(self) -> int:
        return len(self.types)

    def __str__(self) -> str:
        return ",".join(str(t) for t in self.types)

    def __repr__(self) -> str:
        return str(self)

#


class Pokemon:

    def __init__(self, name: str, typing: Typing, dex_number: int):
        self.name = name.upper()
        self.typing = typing
        self.dex_number = dex_number

    def has_type(self, t: PokemonType) -> bool:
        return t in self.typing

    def __str__(self) -> str:
        return self.name


class PokemonMap(Iterable[Pokemon]):

    def __init__(self, *pokemon: Pokemon):
        self.name_map: Dict[str, Pokemon] = dict()
        self.typing_map: Dict[Typing, List[Pokemon]] = dict()
        self.type_map: Dict[PokemonType, List[Pokemon]] = dict()
        self.dex_map: Dict[int, List[Pokemon]] = dict()
        self.add(*pokemon)

    def add(self, *pokemon: Pokemon) -> None:
        for p in pokemon:
            self.name_map[p.name] = p
            add_or_append(self.typing_map, p.typing, p)
            for t in p.typing:
                add_or_append(self.type_map, t, p)
            add_or_append(self.dex_map, p.dex_number, p)

    def __iter__(self) -> Iterator[Pokemon]:
        return iter(self.name_map.values())

    def __len__(self) -> int:
        return len(self.name_map)

    def name(self, name: str) -> Optional[Pokemon]:
        return self.name_map[name] if name in self.name_map else None

    def typing(self, *typing: Typing) -> List[Pokemon]:
        return [x for t in typing for x in self.typing_map[t] if t in self.typing_map]

    def type(self, *pokemon_type: PokemonType) -> List[Pokemon]:
        return [x for t in pokemon_type for x in self.type_map[t] if t in self.type_map]

    def dex_num(self, *dex: int) -> List[Pokemon]:
        return [x for d in dex for x in self.dex_map[d] if dex in self.dex_map]

    @staticmethod
    def load_from_csv(path: str) -> PokemonMap:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, next(f).strip().split(","))
            return PokemonMap(*(Pokemon(p["Name"],
                                        Typing(PokemonType[p["Type1"]], PokemonType[p["Type2"]]),
                                        p["Dex#"]) for p in reader))
