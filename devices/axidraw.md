# AxiDraw/iDraw

## Hardware

Most of the operation is intuitive, but here are some notes:

- invest in spacers for reliably adjusting pens and paper
- shouldn't need lubrication
- belt can be tightened if it gets looser over time
- pen lift servo motors wear out regularly
- prints can get better if you stack several sheets of paper
- the "path" extension has a "convert to dashes" function, which can transform path styles to actual paths

## Software

Again, the Inkscape plugin is mostly intuitive, but there's some mildly hidden stuff.

**Layers** can be used A LOT:

- Hidden layers will not be plotted
- Name your layers according to pens to be used, starting with numbers ("1 - red squares", "1 - red lines", "2 - blue
  lines"), then use the layer tab to set a number to be plotted. Start plotting with Apply.
- Layers starting with % are documentation layers and will never be printed.
- Layer names can also be used for speed and pen control with the [AxiDraw Layer
  Control](https://wiki.evilmadscientist.com/AxiDraw_Layer_Control) language

Suggested speeds are 30% drawing, 75% pen movement, standard acceleration for regular work, 15% drawing, 60% pen
movement, slow acceleration for precision work, and 90/100/max for fast stuff.

Use plugin plot optimization for regular stuff, or just vpype all the way. Note that this action modifies the file (eg
removing groups, reversing directions), so maybe use  backup (and then, you might as well use vpype, if we're being
honest).

## Resources

- [User Manual](https://cdn.evilmadscientist.com/dl/ad/public/AxiDraw_Guide_v501b.pdf)
