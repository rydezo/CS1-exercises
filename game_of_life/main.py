#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["matplotlib>=3.10.7"]
# ///
from argparse import ArgumentParser
from pathlib import Path
import os
import sys
import tomllib
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def neighbors(grid: list[list[bool]], r: int, c: int) -> int:
    rows = len(grid)
    cols = len(grid[0])
    count = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            rr = r + dr
            cc = c + dc
            if 0 <= rr < rows and 0 <= cc < cols and grid[rr][cc]:
                count += 1
    return count


def step(grid: list[list[bool]]) -> list[list[bool]]:
    rows = len(grid)
    cols = len(grid[0])
    new = [[False] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            n = neighbors(grid, r, c)
            if grid[r][c]:
                new[r][c] = n == 2 or n == 3
            else:
                new[r][c] = n == 3
    return new


def load_grid(path: Path, name: str) -> list[list[bool]]:
    with open(path, "rb") as f:
        data = tomllib.load(f)

    patterns = data.get("patterns", {})
    if name not in patterns:
        raise ValueError(f"Unknown pattern: '{name}'")

    data = patterns[name]

    rows = data.get("rows")
    cols = data.get("cols")
    pattern = data.get("pattern")

    if not rows or not cols or not pattern:
        raise ValueError(f"{name} must define 'rows', 'cols', and 'pattern'")

    lines = pattern.splitlines()

    if len(lines) != rows:
        raise ValueError(f"Expected {rows} rows, got {len(lines)}")

    for i, line in enumerate(lines, 1):
        if len(line) != cols:
            raise ValueError(f"Line {i}: expected {cols}, got {len(line)} — {repr(line)}")

    grid = [[(ch in "O1#") for ch in line] for line in lines]

    return grid


def available_patterns(toml_file: Path) -> list[str]:
    with open(toml_file, "rb") as f:
        data = tomllib.load(f)

    patterns = data["patterns"]

    if not patterns:
        return []

    return patterns.keys()


def main(grid: list[list[bool]], fps: int):
    fig, ax = plt.subplots()
    ax.axis("off")  # type:ignore

    img = ax.imshow(grid, cmap="Greys", interpolation="nearest")  # type:ignore

    def update(_frame: None):
        nonlocal grid
        grid = step(grid)
        img.set_data(grid)
        return [img]

    interval = 1000 / fps

    _animation = animation.FuncAnimation(
        fig,
        update,
        interval=interval,
        blit=True,
        cache_frame_data=False,
    )

    try:
        plt.show()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    parser = ArgumentParser(description="Conway's Game of Life")
    parser.add_argument("--patterns", type=Path, default="patterns.toml", help="Path to TOML file with [patterns]")
    parser.add_argument("--list", action="store_true", help="list all available patterns")
    parser.add_argument("--fps", type=int, default=5, help="animation speed in frames per second")
    parser.add_argument("name", type=str, nargs="?", help="name of pattern to load: [patterns.name]")

    args = parser.parse_args()

    if not args.patterns.is_file() or not os.access(args.patterns, os.R_OK):
        print(f"{args.patterns} does not exist or is not readable", sys.stderr)
        sys.exit(1)

    if args.list:
        print(f"Patterns available in {args.patterns}:")
        for name in available_patterns(args.patterns):
            print(f"  - {name}")
        sys.exit(0)

    grid = load_grid(args.patterns, args.name)

    main(grid, args.fps)
