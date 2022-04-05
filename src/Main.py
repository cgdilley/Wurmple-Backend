
from Data import *
from Game.Generate import Generator
from Lambda.Wrapper import Wrapper

import json
from typing import Tuple, Collection, Optional


INPUT = "./dex_clean.csv"


def main(event, context):
    with Wrapper(event, context) as w:
        w.add_cors_header()

        length: int = w.args.get_query("length", val_type=int, default=5)
        typing_limit: int = w.args.get_query("typing_limit", val_type=int, default=1)
        type_limit: int = w.args.get_query("type_limit", val_type=int, default=3)
        allow_monotype: bool = w.args.get_query("allow_monotype", val_type=bool, default=True)
        set_as_daily: bool = w.args.get_query("set_as_daily", val_type=bool, default=False)
        random_seed: Optional[int] = w.args.get_query("random_seed", val_type=int, default=None)

        print(f"LENGTH = {length}, TYPING_LIMIT = {typing_limit}, TYPE_LIMIT = {type_limit}, "
              f"ALLOW_MONOTYPE = {'True' if allow_monotype else 'False'}, "
              f"SET_AS_DAILY = {'True' if set_as_daily else 'False'}, "
              f"RANDOM_SEED = {random_seed}")

        generator = Generator(PokemonMap.load_from_csv(INPUT),
                              length=length,
                              typing_limit=typing_limit,
                              type_limit=type_limit,
                              allow_monotype=allow_monotype,
                              random_seed=random_seed)

        print("GENERATING SEQUENCE")

        seq = generator.generate()

        print(f"SEQUENCE:  {' -> '.join(p.name for p in seq)}")

        if set_as_daily:
            upload_sequence_as_daily(seq)

        w.set_result({"seq": [p.name for p in seq]})

    return w.result


#


def upload_sequence_as_daily(sequence: Collection[Pokemon]):
    pass


#


#


if __name__ == '__main__':
    main(dict(), dict())
