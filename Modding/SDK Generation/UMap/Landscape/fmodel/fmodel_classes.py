
from dataclasses import dataclass

@dataclass
class Vector3D:
    X: float
    Y: float
    Z: float

@dataclass
class Vector4D: 
    X: float
    Y: float
    Z: float
    W: float

@dataclass
class PathName:
    ObjectName: str
    ObjectPath: str

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
    WeightmapTextures: list[PathName]
    WeightmapLayerAllocations: list[Allocations]
    SectionBaseX: int = 0
    SectionBaseY: int = 0
    def __post_init__(self):
        if self.SectionBaseX is None:
            self.SectionBaseX = 0
        if self.SectionBaseY is None:
            self.SectionBaseY = 0
    # def __init__(self, **kwargs): # https://stackoverflow.com/a/54678706
    #     names = set([f.name for f in fields(self)])
    #     for k, v in kwargs.items():
    #         if k in names:
    #             setattr(self, k, v)
    #     self.WeightmapTextures = [PathName(**x) for x in self.WeightmapTextures]

@dataclass
class Export:
    Type: str
    Name: str
    Outer: str
    Class: str
    Properties: LandscapeComponentProperties
    # def __post_init__(self):
    #     self.Properties = LandscapeComponentProperties(**self.Properties)