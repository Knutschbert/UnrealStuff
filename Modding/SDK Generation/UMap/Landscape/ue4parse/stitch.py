# Nihi (Knutschbert) 2024

import multiprocessing.pool
import os
import argparse
import glob
import json
import math
import multiprocessing
from functools import partial
import numpy as np
from PIL import Image
from PIL import ImageDraw
from dataclasses import asdict
from dacite import from_dict
from tqdm import tqdm
from export_classes import *
import matplotlib.pyplot as plt

class ImageHelpers:
    def load_PIL_image( tex_name: str) -> Image: 
        image_path = f'{tex_name}.png' 
        if os.path.exists(image_path):
            return Image.open(image_path)
        else:
            print(f"Warning: Image {tex_name}.png not found.")
        return None

    # Custom ue format, encodes 32 bit depth in 4xuint8 channels
    def rgbe_to_depth(img: Image):
        arr = np.array(img, dtype=np.float32) / 255.0
        k = np.array([1.0, 255.0, 65025.0 , 16581375.0])
        depth_image = np.dot(arr, 0xFFFF/k) ## convert to uint16 range
        return depth_image.astype(np.uint16)

    # from http://www.janeriksolem.net/histogram-equalization-with-python-and.html
    def image_histogram_equalization(image: Image, number_bins=256):
        image = np.asarray(image)
        image_histogram, bins = np.histogram(image.flatten(), number_bins, density=True)
        # image_histogram[0] = 0
        cdf = image_histogram.cumsum() # cumulative distribution function
        cdf = (number_bins-1) * cdf / cdf[-1] # normalize

        # use linear interpolation of cdf to find new pixel values
        image_equalized = np.interp(image.flatten(), bins[:-1], cdf)

        return image_equalized.reshape(image.shape), cdf
    
    def get_limits(comp_positions_sorted: list[tuple[tuple,str]]):# -> tuple[tuple[int, int], np.ndarray[2]]:
        """get image limits from tile positions"""
        def minmax(func, X: bool):
            return func([x[not X] for x,_ in comp_positions_sorted])
        min_x = minmax(np.min, True)
        min_y = minmax(np.min, False)
        max_x = minmax(np.max, True) 
        max_y = minmax(np.max, False)
        limits = np.asarray([min_x, min_y, max_x, max_y], dtype=np.int32)
        max_start = limits[2:] - limits[:2]
        return (min_x, min_y), max_start ## verts - 1 = max_start  

valid_types = {
    "LandscapeComponent": LSCExport,
    "Texture2D": Texture2DExport,
    "SceneComponent": SceneComponentExport,
    "LandscapeMaterialInstanceConstant": LMICExport,
    # "Landscape": LandscapeExport
}   

@dataclass
class LandscapeParams:
    MapName: str
    Heightmap: str
    LandscapeMaterial: str
    ComponentSizeQuads: int
    SubsectionSizeQuads: int
    NumSubsections: int
    NumComponents: Vector2D
    HeightmapSize: Vector2D
    RootOffset: Vector2D
    RelativeLocation: Vector3D
    RelativeRotation: Rotator
    RelativeScale3D: Vector3D
    Components: dict[str, Vector2D]
    LayerInfo: list[str]
    LayerNames: list[str]
    LandscapeGuid: str = None


class LandscapeStitcher:
    tqdm_iter = None # type: tqdm
    save_queue = multiprocessing.Queue()
    input_dir = 'output'
    preview_active = False
    produce_viz = True
    current_file = ''

    def __init__(self, input_dir, preview_active=False, produce_viz=True):
        self.input_dir = input_dir
        self.preview_active = preview_active
        self.produce_viz = produce_viz
        pass

    def image_saver_worker(queue):
        while True:
            item = queue.get() # type: tuple[str, Image.Image]
            if item is None:
                break
            path, image_data = item
            image_data.save(path)
            # print(f'Saved {path}')

    def get_tile_locations_scaled(lp: LandscapeParams):

        tile_sz = int(2 ** math.log2(lp.ComponentSizeQuads + lp.NumSubsections))

        comp_locs = np.array([comp.ndarr[:2] for comp in lp.Components.values()])
        comp_locs_steps = comp_locs / lp.ComponentSizeQuads
        min, max = np.min(comp_locs_steps, axis=0).astype(np.uint32), np.max(comp_locs_steps, axis=0).astype(np.uint32)
        comp_locs_scaled = comp_locs_steps * tile_sz
        min_s, max_s = min * tile_sz, max * tile_sz

        return tile_sz, min_s, max_s, dict(zip(lp.Components.keys(), comp_locs_scaled))

    def get_xeightmap_offset(bias: Vector4D, tile_sz: int, W: int, H: int):
        tex_offset_hm = np.array([math.floor(bias.Z * W), math.floor(bias.W * H)])
        return np.hstack([tex_offset_hm, tex_offset_hm + (tile_sz, tile_sz)])       

    def populate_params(file: str, lscs: dict):
        def tovector2d(x,y):
            return Vector2D(X=x, Y=y)
        landscape = lscs["Landscape"][0] # type: LandscapeExport
        root_component = lscs["SceneComponent"][0] # type: SceneComponentExport
        landc = lscs["LandscapeComponent"] # type: list[LSCExport]
        lmics = lscs["LandscapeMaterialInstanceConstant"] # type: list[LMICExport]
        lp = landscape.Properties
        sqds = lp.ComponentSizeQuads 
        # tile_sz = math.ceil(sqds/64)*64 ## clamp to nearest
        # tile_sz = int(2 ** math.log2(lp.ComponentSizeQuads + lp.NumSubsections))

        # get LS component positions and span
        comp_positions = [(tuple(comp.Properties.SectionBase.ndarr) , comp.Name)  for comp in lscs["LandscapeComponent"]]
        comp_positions_sorted = list(sorted(comp_positions, key=lambda x: (x[0][1],x[0][0]))) # type: list[tuple[tuple,str]] ## sorted by Y

        ## FIXME: this is duplicated rn in stitchmaps
        ### do calc here and shove into params
        tile_sz = int(2 ** math.log2(lp.ComponentSizeQuads + lp.NumSubsections))
        comp_locs = np.array([comp.ndarr[:2] for comp in {v : tovector2d(*k) for k, v in comp_positions_sorted}.values()])
        comp_locs_steps = comp_locs / lp.ComponentSizeQuads
        min, max = np.min(comp_locs_steps, axis=0).astype(np.uint32), np.max(comp_locs_steps, axis=0).astype(np.uint32)
        min_global, max_start = min * tile_sz, max * tile_sz
        
        canvas_sz = (max_start - min_global) + tile_sz
        ###

        # get layerinfo to layer name map
        layerinfo_names = []
        layerinfo_names2 = {}
        assetnames = set()
        paraminfonames = set()
        for c in landc:
            asset_name = [al.LayerInfo.AssetName for al in c.Properties.WeightmapLayerAllocations]
            ma_names = [ma.AssetName for ma in c.Properties.MaterialInstances]
            mats = [x.Properties.VectorParameterValues for x in lmics if x.Name in ma_names and x.Properties.VectorParameterValues]
            assert len(mats) <= 1, 'More params nooo'
            assetnames.update(asset_name)
            paraminfonames.update([x.ParameterInfo.Name for m in mats for x in m])

        base_name = os.path.basename(file).split(".")[0]
        dir_name = os.path.dirname(file)
        file_dir = os.path.join(dir_name, base_name)

        lp = LandscapeParams(
            MapName=file,
            Heightmap = os.path.abspath(os.path.join(file_dir, f'{base_name}_Heightmap.png')).replace('\\', '/'),
            LandscapeMaterial = lp.LandscapeMaterial.ObjectPath,
            ComponentSizeQuads = lp.ComponentSizeQuads,
            SubsectionSizeQuads = lp.SubsectionSizeQuads,
            NumSubsections = lp.NumSubsections,
            NumComponents = tovector2d(*tuple((canvas_sz/tile_sz).astype(int))),
            HeightmapSize = tovector2d(*tuple(canvas_sz)),  ## add square size
            RootOffset = tovector2d(*min_global),
            RelativeLocation = root_component.Properties.RelativeLocation,
            RelativeRotation = root_component.Properties.RelativeRotation,
            RelativeScale3D = root_component.Properties.RelativeScale3D,
            Components = {v : tovector2d(*k) for k, v in comp_positions_sorted},
            LayerInfo = list(paraminfonames),
            LayerNames = list(assetnames),
            LandscapeGuid = '{'+lp.LandscapeGuid+'}'
        )
        return lp

    def load_js_data(file:str) -> tuple[str, dict, LandscapeParams]:
        """Load valid object types from UAssetAPI json"""
        with open(file, 'r') as f:
            uasset_json = json.load(f)

            # check if this map has a landscape
            lscs = {k: [] for k in valid_types.keys()} # type: dict[str, list[Export]]
            try:
                lscs["Landscape"] = [from_dict(data_class=LandscapeExport, data=ls) for ls in uasset_json if ls["Type"] == "Landscape"]
            except Exception as ex:
                print(os.path.basename(file), ex)
                return (file, None, None)

            assert len(lscs["Landscape"]), f'No landscapes found in'
            landscape = lscs["Landscape"][0] # type: LandscapeExport

            # load implemented export types
            for ls in uasset_json:
                obj_type = ls["Type"]
                if obj_type not in valid_types.keys():
                # if ls["Outer"] != landscape.Name or obj_type not in valid_types.keys(): # older versions dont assign outer
                    continue
                if obj_type in lscs.keys():
                    exp = from_dict(data_class=valid_types[obj_type], data=ls)
                    lscs[ls["Type"]].append(exp)
            
            ## older versions dont register textures
            # if len(lscs["Texture2D"]) == 0:
            #     for lsc in lscs["LandscapeComponent"]:
            #         wt_names = [x.AssetName for x in lsc.Properties.WeightmapTextures]
            #         lscs["Texture2D"].extend(wt_names)
            #         lscs["Texture2D"].append(lsc.Properties.HeightmapTexture.AssetName)

            if not hasattr(landscape, 'Properties'):
                return (file, lscs, None)

            return (file, lscs, LandscapeStitcher.populate_params(file, lscs))
        return (file, None, None)

    def show_preview(hm_canvas: Image.Image, wm_canvases: dict[str,Image.Image]):
        fig, axs = plt.subplots(1, len(wm_canvases.values()), figsize=(15, 5))
        fig.suptitle(f'({hm_canvas.size})')
        cnt = 0

        if len(wm_canvases) > 1:
            for layername, image in wm_canvases.items():
                axs[cnt].imshow(image)
                axs[cnt].set_title(f'{layername}')
                cnt += 1
        elif len(wm_canvases) == 1:
            layername, image = next(iter(wm_canvases.items()))
            axs.imshow(image)
            axs.set_title(layername)
            cnt += 1
        plt.show()

        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        fig.suptitle(f'({hm_canvas.size})')
        axes[0].imshow(hm_canvas)
        axes[0].set_title("RGBE")
        axes[1].imshow(Image.fromarray(ImageHelpers.rgbe_to_depth(hm_canvas)))
        axes[1].set_title("Depth Image")
        # axes[2].imshow(Image.fromarray(np.uint8(abbs)))
        # axes[2].set_title("RGBE")

        # plt.xticks(np.arange(-0.5, canvas_sz[0], tile_sz),labels=np.arange(0, canvas_sz[0], tile_sz))
        # plt.yticks(np.arange(-0.5, canvas_sz[1], tile_sz),labels=np.arange(0, canvas_sz[1], tile_sz))
        plt.show()

    def visualize_weightmaps(weight_maps, height_map, colors, max_channels=15):
        if len(weight_maps) > max_channels:
            raise ValueError(f"Too many channels! Only up to {max_channels} channels are supported.")

        # Normalize height map for transparency
        height_map_norm = (height_map - np.min(height_map)) / (np.max(height_map) - np.min(height_map))
        height_map_norm = np.clip(height_map_norm, 0, 1)  # Clip values between 0 and 1

        # Create an empty RGB image and an alpha channel
        height, width = height_map.shape
        composite_image = np.zeros((height, width, 3), dtype=np.float32)
        alpha_channel = np.zeros((height, width), dtype=np.float32)

        # Apply each weight map with the given color
        for i, (name, weight_map) in enumerate(weight_maps.items()):
            if i >= len(colors):
                break
            weight_map_norm = (weight_map - np.min(weight_map)) / (np.max(weight_map) - np.min(weight_map))
            weight_map_norm = np.clip(weight_map_norm, 0, 1)

            color = np.array(colors[i][:3])
            composite_image += weight_map_norm[..., None] * color
            alpha_channel = np.maximum(alpha_channel, weight_map_norm)
        alpha_channel *= height_map_norm

        # print('val', np.min(alpha_channel), np.max(alpha_channel))
        composite_image = np.clip(composite_image, 0, 1) 
        out = np.dstack([composite_image, alpha_channel])
        return composite_image, alpha_channel

    def dump_output(self, file: str, lp: LandscapeParams, heightmap: Image, weightmaps: dict[str, Image.Image]):
        test = []
        base_name = os.path.basename(file).split(".")[0]
        dir_name = os.path.dirname(file)
        file_dir = os.path.join(dir_name, base_name)
        viz_dir = dir_name
        os.makedirs(file_dir, exist_ok=True)

        with open(os.path.join(file_dir, f'{base_name}_LandscapeInfo.json'), 'w') as file:
            json.dump(asdict(lp), file, cls=ExportsEncoder, indent=2)

        depth_arr = ImageHelpers.rgbe_to_depth(heightmap)
        depth_image = Image.fromarray(depth_arr)
        self.save_queue.put((os.path.join(file_dir, f'{base_name}_Heightmap.png'), depth_image))
        for label, image in weightmaps.items():
            self.save_queue.put((os.path.join(file_dir, f'{label}.png'), image))

        if self.produce_viz:
            self.tqdm_iter.set_description('Generating VIZ')
            ## exagerrated heightmap
            depth_equalized, _ = ImageHelpers.image_histogram_equalization(depth_image)
            img_arr = np.asarray(depth_equalized)
            eq = Image.fromarray((plt.cm.jet(img_arr.astype(np.uint16)) * 0xFF).astype(np.uint8))
            self.save_queue.put((os.path.join(viz_dir, f'VIZ_{base_name}_hist_eq_cmap.png'), eq))
            self.save_queue.put((os.path.join(viz_dir, f'VIZ_{base_name}_RGBE.png'), heightmap))

            self.tqdm_iter.set_description('Generating Overlay')
            # merge weightmaps with heightmap
            colors = [
                        (0, 1, 0), (1, 1, 0), (0.75, 0.5, 0.25), (0, 0.5, 0.5), (1, 0, 0),  (0, 0, 1),  (1, 0, 1), (0, 1, 1),
                        (0.5, 0.5, 0), (0.5, 0, 0.5), (0.75, 0.25, 0.5),
                        (0.25, 0.75, 0.5), (0.5, 0.25, 0.75), (0.25, 0.5, 0.75), (0.1, 0.9, 0.3)
                    ]
            img, alpha = LandscapeStitcher.visualize_weightmaps(weightmaps, depth_equalized, colors)
            img_t = img * np.clip(alpha[..., None] + 0.1, 0, 1)
            # plt.imsave(os.path.join(viz_dir, f'VIZ_{base_name}_weight_height_overlay.png'), img_t)
            self.tqdm_iter.set_description('Saving VIZ')
            self.save_queue.put((os.path.join(viz_dir, f'VIZ_{base_name}_weight_height_overlay.png'), Image.fromarray((img_t*0xFF).astype(np.uint8))))

        pass        

    def StitchMaps(self, data: dict, lp: LandscapeParams, images):
        tile_sz, min_s, max_s, comp_locs_scaled = LandscapeStitcher.get_tile_locations_scaled(lp)
        canvas_sz = (max_s - min_s) + tile_sz

        wm_canvases = {} # type: dict[str, Image.Image]
        hm_canvas = Image.new('RGBA', tuple(canvas_sz))
        if self.produce_viz:
            viz_canvas = Image.new('RGBA', tuple(canvas_sz))

        for idx, (name, vector) in enumerate(lp.Components.items()):
            comp = next(filter(lambda x: x.Name == name, data["LandscapeComponent"])) # type: LSCExport
            htexture = images[comp.Properties.HeightmapTexture.AssetName] # type: Image
            # get relative location
            pos_shifted = comp_locs_scaled[name] - min_s
            canvas_loc = np.hstack([pos_shifted, pos_shifted + tile_sz]).astype(np.uint32)

            # get crop area within texture (e.g. texture size is 256x512 @ 256x256 tile)
            tex_crop_hm = LandscapeStitcher.get_xeightmap_offset(comp.Properties.HeightmapScaleBias, tile_sz, *htexture.size)
            crop = htexture.crop(tex_crop_hm)
            hm_canvas.paste(crop, canvas_loc)

            # weightmaps - same, but 1 image per weightmap
            valid_layers = {wa.LayerInfo.AssetName: (wa.WeightmapTextureIndex, wa.WeightmapTextureChannel) for wa in comp.Properties.WeightmapLayerAllocations}
            for layer, (index, channel) in valid_layers.items():
                wtexture = images[comp.Properties.WeightmapTextures[index].AssetName] # type: Image
                tex_crop_wm = LandscapeStitcher.get_xeightmap_offset(comp.Properties.WeightmapScaleBias, tile_sz, *wtexture.size)
                wcrop = wtexture.crop(tex_crop_wm)

                if layer not in wm_canvases:
                    self.tqdm_iter.write(f'Adding Layer: {layer}')
                    wm_canvases[layer] = Image.new('L', tuple(canvas_sz))
                wm_canvases[layer].paste(wcrop.split()[channel], canvas_loc)

            if self.produce_viz:
                # block vizualization
                tv = np.ones([tile_sz, tile_sz, 4], dtype=np.uint8)
                tv2 = np.multiply(tv, np.random.rand(4,) * 255).astype(np.uint8)
                tilevas = Image.fromarray(tv2)
                ImageDraw.Draw(
                    tilevas  # Image
                ).text(
                    (0,tile_sz/2),  # Coordinates
                    f'{idx}: LSC_{name[18:]}',
                    # f'{idx}:{name[18:]}: {pos_shifted} {comp.Properties.HeightmapTexture.AssetName}',  # Text
                    (0,0,0)  # Color
                )
                viz_canvas.paste(tilevas, tuple(canvas_loc))
            pass
        if self.preview_active:
            self.show_preview(hm_canvas, wm_canvases)
            # plt.imshow(hm_canvas)
            # # matplotlib shifts by 0.5, wtf?
            # plt.xticks(np.arange(-0.5, canvas_sz[0]-0.5, tile_sz),labels=np.arange(0, canvas_sz[0], tile_sz))
            # plt.yticks(np.arange(-0.5, canvas_sz[1]-0.5, tile_sz),labels=np.arange(0, canvas_sz[1], tile_sz))
            # plt.grid(which='both')
            # plt.show()

        if self.produce_viz:
            base_name = os.path.basename(self.current_file).split(".")[0]
            dir_name = os.path.dirname(self.current_file)
            file_dir = os.path.join(dir_name, base_name)
            viz_dir = dir_name
            self.save_queue.put((os.path.join(viz_dir, f'VIZ_{base_name}_tiling.png'), viz_canvas))

        return hm_canvas, wm_canvases

    def Process(self, input_dir: str):
        filelist = glob.glob(f'{self.input_dir}/**/*.json', recursive=True)
        workers = 4
        processes = []
        for _ in range(workers):
            saver_process = multiprocessing.Process(target=LandscapeStitcher.image_saver_worker, args=(self.save_queue,))
            saver_process.start()
            processes.append(saver_process)

        loaded_data = {}
        for jsfile in filelist:
            # if 'Bulwark_Landscap' not in jsfile: continue
            if '_LandscapeInfo.json' in jsfile: continue # ignore output json
            loaded_data[jsfile] = LandscapeStitcher.load_js_data(jsfile)[1:]

        self.tqdm_iter = tqdm(loaded_data.items(), desc="Processing maps", position=0, leave=True)
        for file, (data, landscape_params) in self.tqdm_iter:
            if data is None: continue
            self.current_file = file
            self.tqdm_iter.write(f'Processing {file}: {len(landscape_params.Components)} components')
            # todo: theaded loading if needed

            LandscapeStitcher.get_tile_locations_scaled(landscape_params)
            images = []
            self.tqdm_iter.set_description("Loading tiles")
            heightmaps = [x for x in data["Texture2D"] if x.Properties.LODGroup == "TEXTUREGROUP_Terrain_Heightmap"] # type: list[Texture2DExport]
            weightmaps = [x for x in data["Texture2D"] if x.Properties.LODGroup == "TEXTUREGROUP_Terrain_Weightmap"] # type: list[Texture2DExport]
            files = {x.Name : os.path.join(os.path.dirname(file), 'Weightmaps', f'{x.Name}') for x in weightmaps}
            files.update({x.Name : os.path.join(os.path.dirname(file), 'Heightmaps', f'{x.Name}') for x in heightmaps})
            # with multiprocessing.Pool(2) as pool:
            #     images = dict(zip(list(files.keys()), pool.map(ImageHelpers.load_PIL_image, list(files.values()))))
            #     pool.close()
            #     pool.join()
            images = {hm.Name: ImageHelpers.load_PIL_image(os.path.join(os.path.dirname(file), 'Heightmaps', f'{hm.Name}')) for hm in heightmaps}
            wimages = {hm.Name: ImageHelpers.load_PIL_image(os.path.join(os.path.dirname(file), 'Weightmaps', f'{hm.Name}')) for hm in weightmaps}
            images.update(wimages)
            self.tqdm_iter.set_description("Stitching tiles")
            out_heightmap, out_weightmaps = self.StitchMaps(data, landscape_params, images)
            self.tqdm_iter.set_description("Writing")
            self.dump_output(file, landscape_params, out_heightmap, out_weightmaps)
            # LandscapeStitcher.show_preview(out_heightmap, out_weightmaps)

        print('Saving...')
        for _ in range(workers):
            self.save_queue.put(None)
        for process in processes:
            process.join()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="UE4 Asset processing script.")
    parser.add_argument('--input', '-i', type=str, required=True, help='Base directory with LandscapeExtractor processed files')
    parser.add_argument('--preview', '-p', type=str, default=False, help='Preview heightmaps during processing')
    parser.add_argument('--noviz', type=str, default=False, help='Don\'t produce visualization output (normalized, rgbe, tiling)')
    args = parser.parse_args()
    ls = LandscapeStitcher(args.input, args.preview, not args.noviz)
    ls.Process('output')
