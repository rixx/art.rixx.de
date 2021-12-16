---
name: Kaffee mit Mama
tags:
- postcard
- fediverse
plot:
  length: 1334.2
  device:
    name: iDraw
    settings:
      speed: 15%
  pens:
  - brand: Sharpie
    name: Fine Point Permanent Marker
    color: light blue
  paper:
    name: postcard
---

Postcard for Fedi.

[occult](https://github.com/LoicGoulefert/occult) continues to be great, when it works. Sometimes, Shapely has problems
with parts of the geometry and just refuses to parse it. I practiced manual occlusion in Inkscape for a bit:

- Select the upper (?) element, copy and paste-in-place
- Add the other element to selection
- Perform path division, which will remove the copied element
- Select only the to-be-occluded path and delete it

The sharpie worked well, but could have used some more speed – the hatched areas nearly bled through to the back of the
postcard.

Some part of vpype generated annoying artefacts, but I couldn't be bothered to figure out which one, and instead just
deleted them. It would be nice to have some kind of plot preview to see overlapping mini paths like that.
