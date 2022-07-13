import tanjun
from pathlib import Path

@tanjun.as_loader
def load(client: tanjun.Client = tanjun.injected(type=tanjun.Client)) -> None:
    for x in Path("modules").glob("*.py"):
        if x.stem != "__init__":
            client.load_modules(f"modules.{x.stem}")
    return