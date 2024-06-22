## (WIP) Import UserDefinedStructs
## NYI
- doesn't support Map properties
- Doesn't support struct hierarchy

## UE4SS.diff
- apply to UE4SS (7b5ff7deb6ae3c578ff620c3ca8560adee2ff9c5)

## CreateStructs.cpp/h
- Add this to your game project
    - rn it will just generate stuff to "Output" directory.
    -  if you want proper output directory, swap the target from fixed string in CreateStructs to data->Dir (/Game/GameModes/Stages/ScoredStage/Output) default
    - swap the datatable location
- create an editor bp and call "Create Struct Asset" with any path

## How to generate
1. Run "Dump Objects" from within UE4SS
2. Drag and drop the ObjectDump.tt file onto `object_dump_to_json_properties.py`
    - this will create `UE4SS_ObjectDump.csv` file
3. Import the csv file to your project, use CreateStructsDTFmt
4. run the editor BP. It will generate the output
