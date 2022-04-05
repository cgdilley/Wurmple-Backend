import pickle
import csv
from typing import Dict, List, Collection, Union, Iterable, Tuple
import json

from Data.Pokemon import PokemonType, Pokemon, Typing, PokemonMap

INPUT = "./dex.csv"
OUTPUT_PICKLE = "./dex.pickle"
OUTPUT_CSV = "./dex_clean.csv"
OUTPUT_JS = "./dex.js"


def main():
    data = load()
    data = simplify(data)
    save(data)


#


def load() -> List[Dict[str, str]]:
    with open(INPUT, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, next(f).strip().split(","))
        return [x for x in reader]


#


def simplify(data: Iterable[Dict[str, str]]) -> PokemonMap:
    return PokemonMap(*(Pokemon(item["Pokémon"],
                                Typing(*(PokemonType(t) for t in (item["Type 1"], item["Type 2"]))),
                                int(item["Dex #"]))
                        for item in data))


#


def save(data: PokemonMap) -> None:
    with open(OUTPUT_PICKLE, "wb") as f:
        pickle.dump(data, f)
    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, ["Name", "Type1", "Type2", "Dex#"])
        writer.writeheader()
        for p in data:
            types = list(p.typing)
            writer.writerow({"Name": p.name,
                             "Type1": types[0].name,
                             "Type2": types[1].name if len(types) > 1 else types[0].name,
                             "Dex#": p.dex_number})
    with open(OUTPUT_JS, "w", encoding="utf-8") as f:
        f.write("const DEX=" + json.dumps([{"n": p.name.upper(),
                                            "t": [p.name for p in p.typing],
                                            "d": p.dex_number}
                                           for p in data],
                                          separators=(",", ":")))


#


#


if __name__ == '__main__':
    main()
