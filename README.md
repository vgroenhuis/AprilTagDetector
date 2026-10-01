# AprilTag Detector

Browser-based live-camera detector for **tag16h5** AprilTags (ids 0-29), with pose/distance estimation and false-positive filtering.

**Live page:** https://vgroenhuis.github.io/AprilTagDetector/ (needs HTTPS for camera access, open it on your phone and tap *Start camera*).

- Tags are 40 mm squares with a 30 mm black square and 5 mm white margin. Enter **30** (black square) as the tag size.
- `tag16h5_cube_tags.pdf`: all 30 tags, print at 100% and cut on the grey lines. Regenerate with `make_tags_pdf.py`.
- Distance depends on the assumed camera FOV (slider); calibrate by holding a tag at a known distance.
- Robustness: decision margin, bit errors (hamming), geometry checks and multi-frame confirmation; tune with the sliders.

## Run locally

```
python -m http.server 8000
```
then open http://localhost:8000 (opening `index.html` directly does not work).

## Build notes

`apriltag_wasm.js/.wasm` is [arenaxr/apriltag-js-standalone](https://github.com/arenaxr/apriltag-js-standalone) (using current upstream [AprilRobotics/apriltag](https://github.com/AprilRobotics/apriltag), AprilTag 3, master as of 2026-08-07, commit b7c0ebe) compiled with emscripten for tag16h5, with the detection output extended by `hamming` and `margin`. The modified `src/apriltag_js.c` is `apriltag_js.patched.c`. Licences: see `LICENSE-apriltag-js-standalone` (BSD-style).
