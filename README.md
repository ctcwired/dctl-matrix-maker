# dctl-matrix-maker
Python script that uses the colourscience.org library to intake source and target image files (such as EXRs) containing a visible ColorChecker, solve for a 3x3 matrix, and output a usable DaVinci Resolve DCTL file that performs the 3x3 operation.

Inspired by [this forum post](https://www.liftgammagain.com/forum/index.php?threads/tool-to-match-macbeth-charts-with-3x3-matrix-without-nuke.17074/#post-164536).

YouTube demo [here](https://youtu.be/inLKBxAnlzU)

# Install & Use

- Install Python
- pip install --user colour-science
- pip install --user colour-checker-detection
- python -c "import imageio;imageio.plugins.freeimage.download()"
- Then run this script with arguments, for example:
```
dctl-matrix-maker.py source.exr target.exr result.dctl
```
