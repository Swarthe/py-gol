# Rules

[Wikipedia](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)

 - Live cell with 2 | 3 neighbours: survives
 - Dead cell with 3 live neigbours: becomes alive
 - All other cells become or stay dead

# Notes

## Backend

- Found out that Python can simulate enumerations with the `enum` module.
- Ran into problem with deep and shallow copies etc., difficult to locate exact
  source of bugs. This is why the `Cell` class exists, because enums can only be
  passed by value in Python.
- Tests were very useful to detect bugs.
- Implementing Game of Life was overall simpler than expected, because the rules
  are very simple.
- Randomisation required some basic probability maths.

## Frontend

- Quite easy overall.
- Required some basic maths with pixels and cell numbers to display the cell
  grid properly.
- Possible improvement: making it possible to edit cells as the game runs and
  pause.
- Class based code structure and generally good programming practices made this
  easier, fewer weird and unexpected bugs.
- Good aspect ratios and sizes required some basic division maths.
