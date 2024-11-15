
from dataclasses import dataclass, field
import json
from typing import Optional
from numpy import asarray
import numpy as np

@dataclass
class Vector2D:
    X: float
    Y: float
    # ndarr: np.ndarray = np.ndarray((0,4), np.float32)
    def __post_init__(self):
        self.ndarr = asarray(list(self.__dict__.values()))

@dataclass
class Vector3D(Vector2D):
    Z: float

@dataclass
class Vector4D(Vector3D): 
    W: float

@dataclass
class Rotator:
    Pitch: float
    Yaw: float
    Roll: float
    def __post_init__(self):
        self.ndarr = asarray(list(self.__dict__.values()))

@dataclass
class PathName:
    ObjectName: str = ''
    ObjectPath: str = ''
    Outer: str = ''
    AssetType: str = field(init=False)
    AssetName: str = field(init=False)
    Context: str = field(init=False, default="N/A")
    SubObject: str = field(init=False, default="N/A")

    def __post_init__(self):
        if self.ObjectName[-1] == "'":
            self.AssetName = self.ObjectName.split("'")[-2].split('.')[-1]
        else:
            self.AssetName = self.ObjectName.split('.')[-1]

        self.AssetType = self.ObjectName.split("'")[0]

        if ':' in self.ObjectName:
            parts = self.ObjectName.split(':')
            if len(parts) > 1:
                self.Context = parts[1]

@dataclass
class Export:
    Type: str
    Name: str
    Outer: Optional[str]

## Landscape Component
@dataclass
class Allocations:
    LayerInfo: PathName
    WeightmapTextureIndex: int
    WeightmapTextureChannel: int
    
@dataclass
class LandscapeComponentProperties:
    ComponentSizeQuads: int
    SubsectionSizeQuads: int
    NumSubsections: int
    HeightmapTexture: PathName
    HeightmapScaleBias: Vector4D
    WeightmapScaleBias: Vector4D
    MaterialInstances: list[PathName]
    WeightmapTextures: Optional[list[PathName]] = field(default_factory=list)
    WeightmapLayerAllocations: Optional[list[Allocations]] = field(default_factory=list)
    SectionBaseX: int = 0
    SectionBaseY: int = 0
    RelativeLocation: Vector3D = Vector3D(0,0,0)
    def __post_init__(self):
        if self.SectionBaseX is None:
            self.SectionBaseX = 0
        if self.SectionBaseY is None:
            self.SectionBaseY = 0
        self.SectionBase = Vector2D(self.SectionBaseX, self.SectionBaseY)

@dataclass
class LSCExport(Export):
    Properties: LandscapeComponentProperties
    Class: str = None

## Texture
@dataclass
class TextureProperties:
    AddressX: str
    AddressY: str
    ImportedSize: Vector2D
    LightingGuid: str
    LODGroup: str
    SRGB: bool

@dataclass
class Texture2DExport(Export):
    Properties: TextureProperties
    Class: str = None

## Material instance
@dataclass
class ParameterInfo:
    Name: str
    Association: str
    Index: int

@dataclass
class TerrainLayerWeightParameters:
    WeightmapIndex: int 
    bWeightBasedBlend: bool
    ParameterInfo: ParameterInfo

@dataclass
class ParameterValue:
    R: float
    G: float
    B: float
    A: float
    Hex: str

@dataclass
class VectorParameterValue:
    ParameterInfo: ParameterInfo
    ParameterValue: ParameterValue

@dataclass
class StaticParameters:
    TerrainLayerWeightParameters: list[TerrainLayerWeightParameters]

@dataclass
class LandscapeMaterialInstanceConstantProperties:
    StaticParameters: Optional[dict[str,list[TerrainLayerWeightParameters]]]
    VectorParameterValues: Optional[list[VectorParameterValue]]


@dataclass
class LMICExport(Export): #LandscapeMaterialInstanceConstant
    Properties: Optional[LandscapeMaterialInstanceConstantProperties]
    Class: str = None

## Landscape
@dataclass
class LandscapeProperties:
    LandscapeGuid: str
    LandscapeMaterial: PathName
    LandscapeComponents: list[PathName]
    ComponentSizeQuads: int
    SubsectionSizeQuads: int
    NumSubsections: int

@dataclass
class LandscapeExport(Export):
    Properties: Optional[LandscapeProperties]  = field(init=False, default=None)
    Class: str = None

## Scene Component
@dataclass
class SceneComponentProperties:
    RelativeLocation: Vector3D
    RelativeRotation: Rotator = Rotator(0,0,0)
    RelativeScale3D: Vector3D = Vector3D(0,0,0)

@dataclass
class SceneComponentExport(Export):
    Properties: SceneComponentProperties
    Class: str = None

class ExportsEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(ExportsEncoder, self).default(obj)