# (WIP) Generate Heightmaps and Weightmaps from .umap Landscapes
1. Extract json + texture pngs from a .umap containing a Landscape using https://fmodel.app/
2. run `fmodel_tkgui.py` for GUI version or set `json_path` in `fmodel_oo.py` and run it

Creates png files:
- 1x 16-bit Heightmap
- 1x RGBE Heightmap
- 1x 8bit Weightmap per layer

## requirements (10.11.24)
```bash
pip install dacite
pip install matplotlib
pip install pprint
pip install pillow
pip install tk
```


## GUI

![image](https://github.com/user-attachments/assets/bd85e560-e46c-4052-88b1-f251055fa95f)
![image](https://github.com/user-attachments/assets/6857f8d5-ba49-4aa9-9ed0-432e3d7f3ef2)


## example usage

```py
from fmodel_oo import *
json_path = r'h:\chivunpack\Output\Exports\TBL\Content\Maps\Galencourt\Galencourt_Landscape.json'
pc = XeightMapProcessor(json_path)
pc.Init()
pc.Extract_Heightmap() # heightmap.png, heightmap_rgbe.png
pc.Extract_Weightmaps() # 3x png
```

