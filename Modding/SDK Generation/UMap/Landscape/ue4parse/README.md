## Landscape tile stitcher script
- Stitches tiles exported by [LandscapeExtractor](https://github.com/Knutschbert/CUE4Parse/blob/master/README.md)
- produces heightmaps (16bit G) and weightmaps (8bit G) + json metadata
- Tested with ue 4.15-4.27 games

## Process
1. Extract tiles using LandscapeExtractor (`LandscapeExtractor.exe -p "C:\Game\XYZ\Content\Paks" -u 4_25 -o "output"`)
2. Run this script
3. UE Editor: Import heightmaps from png as a new Landscape. Import weightmaps as layer info

## Usage
```bash
usage: stitch.py [-h] [--input INPUT] [--preview PREVIEW] [--noviz NOVIZ]
UE4 Asset processing script.
optional arguments:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
                        Base directory with LandscapeExtractor processed files
  --preview PREVIEW, -p PREVIEW
                        Preview heightmaps during processing
  --noviz NOVIZ         Don't produce visualization output (normalized, rgbe, tiling)
```

## Output structure
```
I:.
│   Main_Level.json <- from LandscapeExtractor
│   VIZ_Main_Level_hist_eq_cmap.png
│   VIZ_Main_Level_RGBE.png
│   VIZ_Main_Level_tiling.png
│   VIZ_Main_Level_weight_height_overlay.png
│
├───Heightmaps              <- from LandscapeExtractor
│       Texture2D_167.png
│       Texture2D_175.png
│
├───Main_Level              <- <Map_Name>, output, contains heightmaps and weightmaps for UE
│       grass_ground_LayerInfo.png
│       grass_LayerInfo.png
│       ground_LayerInfo.png
│       Main_Level_Heightmap.png
│       Main_Level_LandscapeInfo.json
│
└───Weightmaps              <- from LandscapeExtractor
        Texture2D_0.png
        Texture2D_1.png
```

## Vizualization
When launching without `--noviz False` produces following additional files:
#### VIZ_<Map_Name>_weight_height_overlay.png
Combined heightmap + weightmap layers. Arbitrary colors

![image](https://github.com/user-attachments/assets/a5da7c64-48cd-4702-b40f-c791c073c776)

#### VIZ_<Map_Name>_hist_eq_cmap.png
Histogram equalization + color map

![image](https://github.com/user-attachments/assets/91030431-b5f0-4867-a792-dd5c934e577e)

#### VIZ_<Map_Name>_RGBE.png
Original stitched texture in RGBE format (before depth conversion)

![image](https://github.com/user-attachments/assets/6917f9e3-9ffd-44d2-af29-011ed3acc4f3)

#### VIZ_<Map_Name>_tiling.png
Tile assignment + Landscape component name index

![image](https://github.com/user-attachments/assets/12ce7760-f9d9-45b8-814d-44804c5599e3)



