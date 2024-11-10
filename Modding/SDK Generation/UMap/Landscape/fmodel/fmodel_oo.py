import json
import os
from PIL import Image
from pprint import pprint
import numpy as np
from dataclasses import dataclass, field, fields
from dacite import from_dict
import matplotlib.pyplot as plt
from fmodel_classes import *
import math
from PIL import ImageDraw

class XeightMapProcessor():
    def __init__(self, json_path: str) -> None:
        self.json_path = json_path
        self.image_folder = os.path.dirname(json_path)
        self.output_image_path = os.path.join(self.image_folder, 'weightmap')
        self.tile_props = {} # type: dict[str,LandscapeComponentProperties]
        self.heightmap_tiles = {}
        self.weightmap_tiles = {}
        pass
    
    def objectname_short(self, ObjectName: str):
        return ObjectName.split('.')[-1][:-1]

    def pathname_short(self, ObjectName: str):
        return ObjectName.split('/')[-1][:-2]
    
    def rgbe_to_depth(self, img: Image):
        # Custom ue format, encodes 32 bit depth in 4xuint8 channels
        arr = np.array(img, dtype=np.float32) / 255.0
        k = np.array([1.0, 255.0, 65025.0 , 16581375.0])
        depth_image = np.dot(arr, 0xFFFF/k) # convert to uint16 range
        return depth_image.astype(np.uint16)

    def get_minmaxuv(self, v: LandscapeComponentProperties):
        return (v.HeightmapScaleBias.Z,
                v.HeightmapScaleBias.W,
                v.HeightmapScaleBias.Z + (v.SubsectionSizeQuads+1) * v.NumSubsections * v.HeightmapScaleBias.X - v.HeightmapScaleBias.X,
            v. HeightmapScaleBias.W + (v.SubsectionSizeQuads+1) * v.NumSubsections * v.HeightmapScaleBias.Y - v.HeightmapScaleBias.Y)
    
    def get_minmaxwuv(self, v: LandscapeComponentProperties):
        return (v.WeightmapScaleBias.Z,
                v.WeightmapScaleBias.W,
                v.WeightmapScaleBias.Z + (v.SubsectionSizeQuads+1) * v.NumSubsections * v.WeightmapScaleBias.X - v.WeightmapScaleBias.X,
            v. WeightmapScaleBias.W + (v.SubsectionSizeQuads+1) * v.NumSubsections * v.WeightmapScaleBias.Y - v.WeightmapScaleBias.Y)

    def get_midpoint(self, v: LandscapeComponentProperties):
        Min_x = v.SectionBaseX
        Min_y = v.SectionBaseY
        Max_x = v.SectionBaseX + self.ComponentSizeQuads2 
        Max_y = v.SectionBaseY + self.ComponentSizeQuads2 
        Max_x = v.SectionBaseX + v.ComponentSizeQuads 
        Max_y = v.SectionBaseY + v.ComponentSizeQuads 

        Dist = (v.ComponentSizeQuads + 1) // 2
        MidPoint = np.array([(float)(Min_x + Max_x) / 2.0, (float)(Min_y + Max_y) / 2.0])
        Min_x = math.floor(MidPoint[0]) - Dist
        Max_x = math.ceil(MidPoint[0]) + Dist
        Min_y = math.floor(MidPoint[1]) - Dist
        Max_y = math.ceil(MidPoint[1]) + Dist

        return MidPoint, np.array([Min_x, Min_y, Max_x, Max_y])

    def scalequad(self, val):
        return val + 2 * ((val // self.ComponentSizeQuads2)+1)
    
    def load_data(self):
        # Load JSON data
        with open(self.json_path, 'r') as file:
            data = json.load(file)
        self.tiles = [x for x in data if x["Type"] == 'LandscapeComponent'] # Landscape tiles
        self.ComponentSizeQuads2 = self.tiles[0]["Properties"]["ComponentSizeQuads"] + 2 # type: int
        root = [x["Properties"] for x in data if x["Name"] == 'RootComponent0' and "Landscape" in x["Outer"] ] # root transform
        self.root = {
            "RelativeLocation": Vector3D(**root[0]["RelativeLocation"]),
            "RelativeScale3D": Vector3D(**root[0]["RelativeScale3D"])
        }
        
        for tile in self.tiles:
            # exp = Export(**tile)
            exp = from_dict(data_class=Export, data=tile) # dacite
            self.tile_props[exp.Name] = exp.Properties
            # pprint(exp)
    
    def load_image(self, tex_name: str) -> Image:
        image_path = os.path.join(self.image_folder, f'{tex_name}.tga')    
        if os.path.exists(image_path):
            return Image.open(image_path)
        else:
            print(f"Warning: Image {tex_name}.tga not found.")
            return None

    def load_images(self):
        # load heightmaps and weightmaps
        for k, p in self.tile_props.items():
            ## load heightmap
            tex_name = self.objectname_short(p.HeightmapTexture.ObjectName)
            if tex_name not in self.heightmap_tiles:
                self.heightmap_tiles[tex_name] = self.load_image(tex_name)
            for idx, wt in enumerate(p.WeightmapTextures):
                tex_name = self.objectname_short(wt.ObjectName)
                # print(k, idx, tex_name)
                if tex_name not in self.weightmap_tiles:
                    self.weightmap_tiles[tex_name] =self.load_image(tex_name)

    def calc_bounds(self):
        default_tile_size = self.ComponentSizeQuads2 

        min_x = min([p.SectionBaseX for _, p in self.tile_props.items()])
        min_y = min([p.SectionBaseY for _, p in self.tile_props.items()])
        max_x = max([p.SectionBaseX for _, p in self.tile_props.items()]) + default_tile_size
        max_y = max([p.SectionBaseY for _, p in self.tile_props.items()]) + default_tile_size
        print(min_x, min_y, max_x, max_y)
        limits = np.array([min_x, min_y, max_x, max_y])
        max_x = int(max_x/(default_tile_size-2))*default_tile_size
        max_y = int(max_y/(default_tile_size-2))*default_tile_size
        print(limits)

        self.limits = limits
        return min_x, min_y, max_x, max_y
    
    def get_layer_names(self, prop: LandscapeComponentProperties) -> dict[str]:
        names = {}
        for i in prop.WeightmapLayerAllocations:
            names[f'{i.WeightmapTextureIndex}_{i.WeightmapTextureChannel}'] = (i.LayerInfo.ObjectPath.split('/')[-1][:-2])
        return names
    
    def Init(self):
        self.load_data()
        self.load_images()
        self.calc_bounds()

    def Extract_Heightmap(self):
        min_x, min_y, max_x, max_y = self.limits
        canvas = Image.new('RGBA', (max_x-min_x, max_y-min_y))

        for k, v in self.tile_props.items():
            tex_name = self.objectname_short(v.HeightmapTexture.ObjectName)
            w, h = self.heightmap_tiles[tex_name].size
            tile_uv_scaled = np.array(self.get_minmaxuv(v)) * [w,h,w,h] # in image coords

            mid, limits_local = self.get_midpoint(v) # midpoint and min/max of tile
            tile_halfsize = (v.ComponentSizeQuads + 2)/2
            start = mid - self.limits[:-2] - tile_halfsize # mid - minXY - tile_size/2
            # align 2^x
            start_aligned=np.ceil(np.array([start[0], start[1]])/tile_halfsize)*tile_halfsize
            # print(f'start: {start} start_aligned: {start_aligned}')
            
            crop = self.heightmap_tiles[tex_name].crop((tile_uv_scaled[0],tile_uv_scaled[1],tile_uv_scaled[2]+1,tile_uv_scaled[3]+1))
            
            tx, ty = np.asarray(start_aligned, dtype=int)
            canvas.paste(crop, (tx, ty))

        
        depth_image = self.rgbe_to_depth(canvas)

        # fig, axa =plt.subplots(1,2, figsize=(20,20))

        export = Image.fromarray(depth_image)
        # export.putdata()
        filename = os.path.join(self.image_folder, 'heightmap.png')
        export.save(os.path.join(self.image_folder, filename), cmap='reds')
        print(f'16-bit Heightmap: "{filename}"')
        # export.putdata()
        filename = os.path.join(self.image_folder, 'heightmap_rgbe.png')
        canvas.save(filename, cmap='reds')
        print(f'RGBE Heightmap: "{filename}"')
        # axa[1].imshow(canvas, cmap='gray')
        # axa[0].imshow(depth_image, cmap='gray') 
        return export, canvas   

    def Extract_Weightmaps(self):
        min_x, min_y, max_x, max_y = self.limits
        all_layer_names = []
        for k,v in self.tile_props.items():
            all_layer_names.extend(self.get_layer_names(v).values())
        all_layer_names = list(set(all_layer_names))
        
        canvases = {}
        for layer in all_layer_names:
            canvases[layer] = Image.new('L', (max_x, max_y))
            for k, v in self.tile_props.items():
                relevant = [x for x in v.WeightmapLayerAllocations if self.pathname_short(x.LayerInfo.ObjectPath) == layer]
                if not any(relevant):
                    # print(f'not relevant {layer} {k}')
                    continue
                
                # grab texture and channel
                wt_idx = relevant[0].WeightmapTextureIndex
                tex_name = self.objectname_short(v.WeightmapTextures[wt_idx].ObjectName)
                ch = relevant[0].WeightmapTextureChannel

                # tex_name = self.objectname_short(v.HeightmapTexture.ObjectName)
                w, h = self.weightmap_tiles[tex_name].size
                tile_uv_scaled = np.array(self.get_minmaxwuv(v)) * [w,h,w,h] # in image coords

                mid, limits_local = self.get_midpoint(v) # midpoint and min/max of tile
                tile_halfsize = (v.ComponentSizeQuads + 2)/2
                start = mid - self.limits[:-2] - tile_halfsize # mid - minXY - tile_size/2
                # align 2^x
                start_aligned=np.ceil(np.array([start[0], start[1]])/tile_halfsize)*tile_halfsize
                # print(f'start: {start} start_aligned: {start_aligned}')
                
                crop = self.weightmap_tiles[tex_name].crop((tile_uv_scaled[0],tile_uv_scaled[1],tile_uv_scaled[2]+1,tile_uv_scaled[3]+1))
                
                tx, ty = np.asarray(start_aligned, dtype=int)
                crop_splt = crop.split()
                canvases[layer].paste(crop_splt[ch], (tx, ty))
        
        # num_rows = int(len(all_layer_names) / 2 + 0.5)
        # fig, axa =plt.subplots(num_rows, 2, figsize=(20, 15 * num_rows))
        # axa = axa.flatten()

        for i, layer in enumerate(all_layer_names):
            filename = os.path.join(self.image_folder, layer+'.png')
            canvases[layer].save(filename, cmap='reds')
            print(f'{i}: "{layer}" -> "{filename}"')
        return canvases
            

json_paths = {
    # r'PrisonBreak\PrisonBreak_Landscape.json',
    # r'Tournament\TournamentGrounds_Terrain_02.json',
    # r'Stronghold\Stronghold_Landscape.json',
    # r'Karak\Karak_Landscape.json',
    # r'Coxwell\Coxwell_Terrain_V2.json',
    # r'Bridgetown\Bridgettown_Landscape.json',
    # r'CasaLoma\Lionspire_Landscape.json',
    # r'Bulwark\Bulwark_Landscape.json',
    # r'CastleSiege\CastleSiege_Terrain.json',
    # r'Darkforest\DarkForest_Landscape.json',
    # r'Courtyard\Courtyard_Landscape2.json', # weightmap scaling wtf (diff hmap wmap sizes),
#cant extract
    # r'Frontend\Frontend_Landscape.json',
    # r'Hippodrome\Hippodrome_Landscape.json',# bogus data, plane?
#spaces
    # r'Citadel\Citadel_Landscape.json',
    # r'Raid\Raid_Landscape.json',
    # r'FrozenLake\FrozenLake_Landscape_01.json',
    # r'Galencourt\Galencourt_Landscape.json',
}

#good
# json_path = r'h:\chivunpack\Output\Exports\TBL\Content\Maps\PrisonBreak\PrisonBreak_Landscape.json'
# json_path = r'h:\chivunpack\Output\Exports\TBL\Content\Maps\Tournament\TournamentGrounds_Terrain_02.json'
# json_path = r'h:\chivunpack\Output\Exports\TBL\Content\Maps\Stronghold\Stronghold_Landscape.json'
# json_path = r'h:\chivunpack\Output\Exports\TBL\Content\Maps\Karak\Karak_Landscape.json'
# json_path = r'h:\chivunpack\Output\Exports\TBL\Content\Maps\Coxwell\Coxwell_Terrain_V2.json'
# json_path = r'h:\chivunpack\Output\Exports\TBL\Content\Maps\Bridgetown\Bridgettown_Landscape.json'
# json_path = r'h:\chivunpack\Output\Exports\TBL\Content\Maps\CasaLoma\Lionspire_Landscape.json'
# json_path = r'h:\chivunpack\Output\Exports\TBL\Content\Maps\Bulwark\Bulwark_Landscape.json'
# json_path = r'h:\chivunpack\Output\Exports\TBL\Content\Maps\CastleSiege\CastleSiege_Terrain.json'
# json_path = r'h:\chivunpack\Output\Exports\TBL\Content\Maps\Darkforest\DarkForest_Landscape.json'
# json_path = r'h:\chivunpack\Output\Exports\TBL\Content\Maps\Courtyard\Courtyard_Landscape2.json' # weightmap scaling wtf (diff hmap wmap sizes)
#cant extract
# json_path = r'h:\chivunpack\Output\Exports\TBL\Content\Maps\Frontend\Frontend_Landscape.json'
# json_path = r'h:\chivunpack\Output\Exports\TBL\Content\Maps\Hippodrome\Hippodrome_Landscape.json'# bogus data, plane?
#spaces
# json_path = r'h:\chivunpack\Output\Exports\TBL\Content\Maps\Citadel\Citadel_Landscape.json'
# json_path = r'h:\chivunpack\Output\Exports\TBL\Content\Maps\Raid\Raid_Landscape.json'
# json_path = r'h:\chivunpack\Output\Exports\TBL\Content\Maps\FrozenLake\FrozenLake_Landscape_01.json'
# json_path = r'h:\chivunpack\Output\Exports\TBL\Content\Maps\Galencourt\Galencourt_Landscape.json'


if __name__ == "__main__":
    pc = XeightMapProcessor(json_path)
    pc.Init()
    pc.Extract_Heightmap()
    pc.Extract_Weightmaps()