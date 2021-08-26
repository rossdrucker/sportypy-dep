# sportypy

This repository contains code necessary to draw scale versions of playing surfaces to visualize play-by-play data for NHL, MLB, NBA, NFL, and NCAA basketball games in **Python**. For the **R** version of this package, click [here](https://github.com/rossdrucker/sportyR).

## Installation

To install `sportypy` via `pip`, please run

```bash
pip install sportypy
```

## Usage

Totally customizable plots are possible by calling a class, then using the `.draw()` method of the class to create the plot. Here is an example:

```python
from sportypy import NCAACourt
NCAACourt(
    colors_dict = {
        'court_background': '#e8e0d7',
        'offensive_halfcourt': '#e8e0d7',
        'defensive_halfcourt': '#e8e0d7',
        'center_circle_outline': '#13294b',
        'center_circle_fill': '#e8e0d7',
        'division_line': '#13294b',
        'end_line': '#13294b',
        'side_line': '#13294b',
        'coaches_box': '#13294b',
        'substitution_area': '#13294b',
        'court_apron': '#e84a27',
        'three_point_line': '#13294b',
        'two_point_range': '#ffffff66',
        'free_throw_lane_boundary': '#ffffff',
        'free_throw_circle_outline': '#ffffff',
        'paint': '#e84a27',
        'restricted_arc': '#13294b',
        'backboard': '#13294b',
        'basket_ring': '#13294b',
        'net': '#ffffff',
        'amateur_blocks': '#ffffff',
        'defensive_box': '#13294b',
        'team_bench_area': '#13294b',
        'twenty_eight_foot_line': '#13294b'
    }
).draw()
```

## References

### MLB

- [MLB Rule Book](rule_books/mlb.pdf)

### NBA

- [NBA Rule Book](rule_books/nba.pdf)

### NCAA

- [NCAA Men's Basketball Rule Book](rule_books/ncaa_mbb.pdf)

- [NCAA Women's Basketball Rule Book](rule_books/ncaa_wbb.pdf)

- [NCAA Football](rule_books/ncaa_f.pdf)

- [NCAA Volleyball](rule_books/ncaa_vb.pdf)

### NHL

- [NHL Rule Book](rule_books/nhl.pdf)

### NFL

- [NFL Rule Book](rule_books/nfl.pdf)

### WNBA

- [WNBA Rule Book](rule_books/wnba.pdf)

## Author

- Ross Drucker

## Acknowledgements

- Federico Scivittaro (`helpers/scrapers/util.py`)
- Kevin McCurley (state boundaries in the Mercator Projection)

## License

This package is licensed under the terms of the INSERT LICENSE TYPE HERE license. See `LICENSE` for more information.
