from __future__ import annotations
import os
import sys
from pythonnet import load


try:
    load("coreclr")
except Exception as e:
    print(f"CoreCLR already loaded or failed: {e}")

import clr

dll_dir = r"P:\code\random\cue_nodes\py_cue4parse\CUE4Parse\temp_out"
dll_path = os.path.join(dll_dir, "CUE4Parse.dll")

if os.path.exists(dll_path):
    clr.AddReference(dll_path)
    print("Successfully added reference to CUE4Parse.dll")
else:
    print(f"ERROR: Could not find DLL at {dll_path}")
    sys.exit(1)

try:
    from CUE4Parse.UE4.Versions import EGame

    print(f"Success! UE5 Version: {EGame.GAME_UE5_0}")
except ImportError as e:
    print(f"Import failed: {e}")
    # Troubleshooting: print everything visible in the CLR
    import System

    print(
        "Available Assemblies:",
        [a.GetName().Name for a in System.AppDomain.CurrentDomain.GetAssemblies()],
    )

from CUE4Parse.UE4.Versions import EGame, VersionContainer
from CUE4Parse.FileProvider import DefaultFileProvider
from CUE4Parse.Encryption.Aes import FAesKey
from CUE4Parse.UE4.Objects.Core.Misc import FGuid
from CUE4Parse.Compression import ZlibHelper
from CUE4Parse.Compression import OodleHelper
from CUE4Parse.UE4.Assets import IPackage, Package
from System.IO import SearchOption  # Required for the constructor
from System import Guid  # .NET's Guid type

# 1. Initialize Provider
game_path = r"U:\Games\Chivalry2_c\TBL\Content\Paks"
paks = [f for f in os.listdir(game_path) if f.endswith(".pak")]
print(f"OS sees {len(paks)} pak files in {game_path}")

if len(paks) == 0:
    print("Warning: No .pak files found in that directory. Check your path!")

versions = VersionContainer(EGame.GAME_UE4_27)
is_case_insensitive = True
provider = DefaultFileProvider(
    game_path, SearchOption.AllDirectories, is_case_insensitive, versions
)
provider.Initialize()

guid = FGuid(0, 0, 0, 0)  # Replace with actual GUID if needed
provider.SubmitKey(
    guid,
    FAesKey("0x0000000000000000000000000000000000000000000000000000000000000000"),
)
provider.LoadVirtualPaths()

ZlibHelper.DownloadDll()
ZlibHelper.Initialize("zlib-ng2.dll")

OodleHelper.DownloadOodleDll()
OodleHelper.Initialize("oo2core_9_win64.dll")
asset_path = None
for kvp in provider.Files:
    file_path = kvp.Key
    file_obj = kvp.Value
    if "ArgonSDKModBase" in file_path:
        fp_noext = file_path.split(".")[0]
        print(f"File: {fp_noext}")
        asset_path = fp_noext

if asset_path is None:
    asset_path = "TBL/Content/GameModes/Modes/Mode_TDM.uasset"
asset_path = "TBL/Content/Mods/AgMods/FlashBlades/FlashBlades"
package = provider.LoadPackage(asset_path)  # type: Package

from CUE4Parse.UE4.Objects.Engine import UBlueprintGeneratedClass
from CUE4Parse.UE4.Objects.UObject import UClass

from Newtonsoft.Json import JsonConvert, Formatting, JsonSerializerSettings

# from CUE4Parse.Utils import JsonSerializerOptions  # CUE4Parse internal helper

from System.Collections import IEnumerable

from CUE4Parse.UE4.Assets.Exports import UObject


def package_to_json_internal(package: IPackage):
    """
    Converts a package to JSON using CUE4Parse's internal Newtonsoft.Json converters.
    """
    exports = package.GetExports()  # type: IEnumerable[UObject]
    settings = JsonSerializerSettings()
    json_string = JsonConvert.SerializeObject(package.GetExports(), Formatting.Indented)

    return json_string


def convert_to_json_obj(data):
    temp_json_str = JsonConvert.SerializeObject(data, Formatting.Indented)
    return json.loads(temp_json_str)


import json

kvp = None
# json_data = package_to_json_internal(package)
package_json = convert_to_json_obj(package)
package_json["ExportMap"] = convert_to_json_obj(package.GetExports())
package_json["Decompile"] = {}

for kvp in package.GetExports():
    if isinstance(kvp.Class, UClass):
        _class = kvp.Class
        try:
            pseudo = _class.DecompileBlueprintToPseudo()
            print("Class", kvp.Name, _class)
            # print("BP Class", kvp.Name)
            print("ClassDefaultObject", _class.ClassDefaultObject)
            print("ClassGeneratedBy", _class.ClassGeneratedBy)
            print("SuperStruct", _class.SuperStruct)
            print(pseudo)
            package_json["Decompile"][kvp.Name] = pseudo
            pak = package  # type: Package
        except Exception as ex:
            # print(ex)
            pass

with open("package_dump.json", "w") as f:
    json.dump(package_json, f, indent=2)
