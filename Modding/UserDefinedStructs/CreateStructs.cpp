// Nihi 2024

#include "CreateStructs.h"
#include "ScopedTransaction.h"
#include "EdGraphSchema_K2.h"
#include "UserDefinedStructure/UserDefinedStructEditorData.h"

//#include "Internationalization.h"
#include "Engine/World.h"
#include "Engine/UserDefinedEnum.h"
#include "Engine/UserDefinedStruct.h"

#include "Factories/WorldFactory.h"
#include "Factories/StructureFactory.h"
#include "AssetToolsModule.h"
#include <map>


UObject* UCreateStructs::CreateAsset(FString AssetPath, UClass* AssetClass, UFactory* AssetFactory, bool& success, FString& OutInfoMessage)
{
    IAssetTools& AssetTools = FModuleManager::GetModuleChecked < FAssetToolsModule>("AssetTools").Get();

    UFactory* Factory = AssetFactory;
    if (Factory == nullptr)
    {
        for (UFactory* Fac : AssetTools.GetNewAssetFactories())
        {
            if (Fac->SupportedClass == AssetClass)
            {
                Factory = Fac;
                break;
            }

        }
    }

    if (Factory == nullptr)
    {
        success = false;
        OutInfoMessage = FString::Printf(TEXT("Create failed, no factory: '%s'"), *AssetPath);
        return nullptr;
    }

    if (Factory->SupportedClass != AssetClass)
    {
        success = false;
        OutInfoMessage = FString::Printf(TEXT("Create failed, cant produce class: '%s'"), *AssetPath);
        return nullptr;

    }

    UObject* Asset = AssetTools.CreateAsset(FPaths::GetBaseFilename(AssetPath), FPaths::GetPath(AssetPath), AssetClass, Factory);

    if (Asset == nullptr)
    {
        success = false;
        OutInfoMessage = FString::Printf(TEXT("asset creation failed: '%s'"), *AssetPath);
        return nullptr;

    }

    success = true;
    OutInfoMessage = FString::Printf(TEXT("Created Asset: '%s'"), *AssetPath);
    return Asset;
}

UWorld* UCreateStructs::CreateWorldAsset(FString AssetPath, bool& success, FString& OutInfoMessage)
{

    UWorldFactory* Factory = NewObject<UWorldFactory>();
    Factory->bInformEngineOfWorld = false;
    Factory->FeatureLevel = ERHIFeatureLevel::ES3_1; // no idea

    UObject* Asset = CreateAsset(AssetPath, UWorld::StaticClass(), Factory, success, OutInfoMessage);
    return Cast<UWorld>(Asset);
}

UUserDefinedEnum* UCreateStructs::CreateEnumAsset(FString AssetPath, bool& success, FString& OutInfoMessage)
{
    UObject* Asset = CreateAsset(AssetPath, UUserDefinedEnum::StaticClass(), nullptr, success, OutInfoMessage);
    return Cast<UUserDefinedEnum>(Asset);
}

struct FMemberVariableNameHelper
{
    static FName Generate(UUserDefinedStruct* Struct, const FString& NameBase, const FGuid Guid, FString* OutFriendlyName = NULL)
    {
        check(Struct);

        FString Result;
        if (!NameBase.IsEmpty())
        {
            if (!FName::IsValidXName(NameBase, INVALID_OBJECTNAME_CHARACTERS))
            {
                Result = MakeObjectNameFromDisplayLabel(NameBase, NAME_None).GetPlainNameString();
            }
            else
            {
                Result = NameBase;
            }
        }

        if (Result.IsEmpty())
        {
            Result = TEXT("MemberVar");
        }

        const uint32 UniqueNameId = CastChecked<UUserDefinedStructEditorData>(Struct->EditorData)->GenerateUniqueNameIdForMemberVariable();
        const FString FriendlyName = FString::Printf(TEXT("%s_%u"), *Result, UniqueNameId);
        if (OutFriendlyName)
        {
            *OutFriendlyName = FriendlyName;
        }
        const FName NameResult = *FString::Printf(TEXT("%s_%s"), *FriendlyName, *Guid.ToString(EGuidFormats::Digits));
        check(NameResult.IsValidXName(INVALID_OBJECTNAME_CHARACTERS));
        return NameResult;
    }

    static FGuid GetGuidFromName(const FName Name)
    {
        const FString NameStr = Name.ToString();
        const int32 GuidStrLen = 32;
        if (NameStr.Len() > (GuidStrLen + 1))
        {
            const int32 UnderscoreIndex = NameStr.Len() - GuidStrLen - 1;
            if (TCHAR('_') == NameStr[UnderscoreIndex])
            {
                const FString GuidStr = NameStr.Right(GuidStrLen);
                FGuid Guid;
                if (FGuid::ParseExact(GuidStr, EGuidFormats::Digits, Guid))
                {
                    return Guid;
                }
            }
        }
        return FGuid();
    }
};
bool AddVariable(UUserDefinedStruct* Struct, const FString & FriendlyName, const FString & VarName, const FString & GUID,  const FEdGraphPinType& VarType)
{
    if (Struct)
    {
        //const FScopedTransaction Transaction(LOCTEXT("AddVariable", "Add Variable"));
        FStructureEditorUtils::ModifyStructData(Struct);

        FString ErrorMessage;
        if (!FStructureEditorUtils::CanHaveAMemberVariableOfType(Struct, VarType, &ErrorMessage))
        {
            UE_LOG(LogBlueprint, Warning, TEXT("%s"), *ErrorMessage);
            return false;
        }

        FGuid Guid;
        FGuid::Parse(GUID, Guid);
        //const FGuid Guid = FGuid::NewGuid();
        FString DisplayName(*FriendlyName);
        //const FName VarName = FMemberVariableNameHelper::Generate(Struct, FString(), Guid, &DisplayName);
        check(NULL == FStructureEditorUtils::GetVarDesc(Struct).FindByPredicate(FStructureEditorUtils::FFindByNameHelper<FStructVariableDescription>(FName(*VarName))));
        check(FStructureEditorUtils::IsUniqueVariableFriendlyName(Struct, DisplayName));
        
        const FName NameResult = *FString::Printf(TEXT("%s_%s"), *VarName, *Guid.ToString(EGuidFormats::Digits));
        //check(NameResult.IsValidXName(INVALID_OBJECTNAME_CHARACTERS));
        FStructVariableDescription NewVar;

        NewVar.VarName = NameResult;
        NewVar.FriendlyName = DisplayName;
        NewVar.SetPinType(VarType);
        NewVar.VarGuid = Guid;
        FStructureEditorUtils::GetVarDesc(Struct).Add(NewVar);

        FStructureEditorUtils::OnStructureChanged(Struct, FStructureEditorUtils::EStructureEditorChangeInfo::AddedVariable);
        return true;
    }
    return false;
}

const FName PC_Exec(TEXT("exec"));
const FName PC_Boolean(TEXT("bool"));
const FName PC_Byte(TEXT("byte"));
const FName PC_Class(TEXT("class"));
const FName PC_Int(TEXT("int"));
const FName PC_Int64(TEXT("int64"));
const FName PC_Float(TEXT("float"));
const FName PC_Name(TEXT("name"));
const FName PC_Delegate(TEXT("delegate"));
const FName PC_MCDelegate(TEXT("mcdelegate"));
const FName PC_Object(TEXT("object"));
const FName PC_Interface(TEXT("interface"));
const FName PC_String(TEXT("string"));
const FName PC_Text(TEXT("text"));
const FName PC_Struct(TEXT("struct"));
const FName PC_Wildcard(TEXT("wildcard"));
const FName PC_Enum(TEXT("enum"));
const FName PC_SoftObject(TEXT("softobject"));
const FName PC_SoftClass(TEXT("softclass"));
const FName PSC_Self(TEXT("self"));
const FName PSC_Index(TEXT("index"));
const FName PSC_Bitmask(TEXT("bitmask"));
const FName PN_Execute(TEXT("execute"));

static const std::map<FString, const FName> PropertyTypePCMap = {
    {L"InterfaceProperty", PC_Interface},
    {L"ClassProperty", PC_Class},
    {L"SoftClassProperty", PC_SoftClass},
    {L"SoftObjectProperty", PC_SoftObject},
    {L"ObjectProperty", PC_Object},
    {L"StructProperty", PC_Struct},
    {L"FloatProperty", PC_Float},
    {L"Int64Property", PC_Int64},
    {L"IntProperty", PC_Int},
    {L"ByteProperty", PC_Byte},
    {L"EnumProperty", PC_Byte},
    {L"NameProperty", PC_Name},
    {L"BoolProperty", PC_Boolean},
    {L"StrProperty", PC_String},
    {L"TextProperty", PC_Text}
};


// Valid types
/*
FInterfaceProperty
FClassProperty
FSoftClassProperty
FSoftObjectProperty
FObjectPropertyBase
FStructProperty
FFloatProperty
FInt64Property
FIntProperty
ByteProperty
EnumProperty
FNameProperty
FBoolProperty
FStrProperty
FTextProperty

PC_Interface
PC_Class
PC_SoftClass
PC_SoftObject
PC_Object
PC_Struct
PC_Float
PC_Int64
PC_Int
PC_Byte
PC_Byte
PC_Name
PC_Boolean
PC_String
PC_Text
*/

UUserDefinedStruct* UCreateStructs::CreateStructAsset(FString AssetPath, bool& success, FString& OutInfoMessage)
{

    UStructureFactory* Factory = NewObject<UStructureFactory>();
    UDataTable * dt = Cast<UDataTable>(StaticLoadObject(UDataTable::StaticClass(), NULL, L"/Game/GameModes/Stages/ScoredStage/UE4SS_ObjectDump.UE4SS_ObjectDump"));

    if (dt)
    {
        FString cur_file;
        UUserDefinedStruct* Struct = nullptr;

        for (auto it : dt->GetRowMap())
        {
            FCreateStructsDTFmt* data = (FCreateStructsDTFmt*)(it.Value);
            UObject* cls = nullptr;
            if (cur_file != data->File)
            {
                cur_file = data->File;

                Struct = Cast<UUserDefinedStruct>(CreateAsset(TEXT("/Game/GameModes/Stages/ScoredStage/Output/") + data->File, UUserDefinedStruct::StaticClass(), Factory, success, OutInfoMessage));
                FStructureEditorUtils::GetVarDesc(Struct).Pop(); // remove default

                UE_LOG(LogBlueprint, Warning, TEXT("creating asset %s"), *data->File);
            }

            auto type_name = PropertyTypePCMap.find(data->Class_Name);
            auto container_type = EPinContainerType::None;
            auto terminal_type = FEdGraphTerminalType();
            auto lookup_class = data->Property_Class_Name;

            FString p_subtype, p_subpath;
            FString t_subtype, t_subpath;
            bool t_split = data->Class_Name.Split(L" ", &t_subtype, &t_subpath);
            bool p_split = data->Property_Class_Name.Split(L" ", &p_subtype, &p_subpath);

            if (p_split)
            {
                if (t_split)
                {
                    // map
                    // TODO: this is not quite right
                    cls = StaticLoadObject(UObject::StaticClass(), nullptr, *t_subpath);
                    type_name = PropertyTypePCMap.find(t_subtype);
                    auto type_name2 = PropertyTypePCMap.find(p_subtype);
                    auto cls2 = StaticLoadObject(UObject::StaticClass(), nullptr, *p_subpath);
                    
                    terminal_type.TerminalCategory = type_name2->second;
                    terminal_type.TerminalSubCategoryObject = cls2;
                }
                else
                {
                    if (data->Class_Name == "ArrayProperty")
                        container_type = EPinContainerType::Array;
                    else if (data->Class_Name == "SetProperty")
                        container_type = EPinContainerType::Set;
;
                    type_name = PropertyTypePCMap.find(p_subtype);
                    lookup_class = p_subpath;
                }
            }

            //if (data->Class_Name == "ArrayProperty")
            //{
            //    container_type = EPinContainerType::Array;
            //    data->Property_Class_Name.Split(L" ", &p_subtype, &p_subpath);
            //    type_name = PropertyTypePCMap.find(p_subtype);
            //    lookup_class = p_subpath;
            //    //UE_LOG(LogBlueprint, Warning, TEXT("%s : %s"), *subtype, *subpath);
            //}
            //else if (data->Class_Name == "MapProperty")
            //{

            //}
            //else if (data->Class_Name == "SetProperty")
            //{

            //}

            if (!cls && !lookup_class.IsEmpty())
                cls = StaticLoadObject(UObject::StaticClass(), nullptr, *lookup_class);


            if (type_name != PropertyTypePCMap.end())
            {
                    bool status = AddVariable(Struct, data->Friendly_Name, data->Friendly_Name+"_" + data->Name_ID, data->Name_GUID,
                        FEdGraphPinType(type_name->second, NAME_None, cls, container_type, false, terminal_type));
            }
            else
                UE_LOG(LogBlueprint, Warning, TEXT("%s: failed to handle type %s"), *data->File, *data->Class_Name);
            
        }
        UE_LOG(LogBlueprint, Warning, TEXT("%s"), *AssetPath);
    }

    return nullptr;


    UObject* Asset = CreateAsset(AssetPath, UUserDefinedStruct::StaticClass(), Factory, success, OutInfoMessage);
    UE_LOG(LogBlueprint, Warning, TEXT("%s"), *OutInfoMessage);
    UE_LOG(LogBlueprint, Warning, TEXT("%s"), *AssetPath);
    UUserDefinedStruct* Struct = Cast<UUserDefinedStruct>(Asset);
    FStructureEditorUtils::GetVarDesc(Struct).Pop();

        auto cls = StaticLoadObject(UObject::StaticClass(), nullptr, TEXT("/Script/Engine.SceneComponent"));
        if (!cls)
        {
            UE_LOG(LogBlueprint, Warning, TEXT("%s failed to load /Script/Engine.SceneComponent"), *AssetPath);
        }
        else
        {
            /*AddVariable(Struct, FString("MaxTimeToShares2"), FString("MaxTimeToShares2_11"), FString("69F9CE124D3C72ACC2C9F48743DB95DC"),
                FEdGraphPinType(UEdGraphSchema_K2::PC_Object, NAME_None, cls, EPinContainerType::None, false, FEdGraphTerminalType()));*/
            FStructureEditorUtils::AddVariable(Struct, FEdGraphPinType(UEdGraphSchema_K2::PC_Object, L"LevelSequenceActor", nullptr, EPinContainerType::None, false, FEdGraphTerminalType()));
        }

    AddVariable(Struct, FString("MaxTimeToShares"), FString("MaxTimeToShares_11"), FString("69F9CE124D3C72ACC2C9F48743DB95DC"),
        FEdGraphPinType(UEdGraphSchema_K2::PC_Object, L"LevelSequenceActor", nullptr, EPinContainerType::None, false, FEdGraphTerminalType()));
    AddVariable(Struct, FString("InitialScore"), FString("InitialScore_12"), FString("4AEBA1704DAF75ADE2924DA3D12558DE"),
        FEdGraphPinType("int", NAME_None, nullptr, EPinContainerType::None, false, FEdGraphTerminalType()));
    AddVariable(Struct, FString("MaxScore"), FString("MaxScore_13"), FString("D70C38EE4707623CFCA61EA5717BDEAB"),
        FEdGraphPinType(UEdGraphSchema_K2::PC_Int, NAME_None, nullptr, EPinContainerType::None, false, FEdGraphTerminalType()));
    AddVariable(Struct, FString("DurationSeconds"), FString("DurationSeconds_7"), FString("ADCEBB60497B67D582A629BA8EE1ECE4"),
        FEdGraphPinType(UEdGraphSchema_K2::PC_Float, NAME_None, nullptr, EPinContainerType::None, false, FEdGraphTerminalType()));
    AddVariable(Struct, FString("PercentTimeToShareWithNextStage"), FString("PercentTimeToShareWithNextStage_9"), FString("124A116F449FD592EA5A5FB82AAA4F6D"),
        FEdGraphPinType(UEdGraphSchema_K2::PC_Float, NAME_None, nullptr, EPinContainerType::None, false, FEdGraphTerminalType()));
    AddVariable(Struct, FString("MaxTimeToShare"), FString("MaxTimeToShare_11"), FString("69F9CE124D3C72ACC2C9F48743DB95DC"),
        FEdGraphPinType(UEdGraphSchema_K2::PC_Float, NAME_None, nullptr, EPinContainerType::None, false, FEdGraphTerminalType()));

    //bool addbool1 = AddVariable(Struct, FEdGraphPinType(UEdGraphSchema_K2::PC_Int, NAME_None, nullptr, EPinContainerType::Array, false, FEdGraphTerminalType()));
    //bool addbool2 = AddVariable(Struct, FEdGraphPinType(UEdGraphSchema_K2::PC_Float, NAME_None, nullptr, EPinContainerType::None, false, FEdGraphTerminalType()));
    //bool addbool3 = AddVariable(Struct, FEdGraphPinType(UEdGraphSchema_K2::PC_Int, NAME_None, nullptr, EPinContainerType::None, false, FEdGraphTerminalType()));
    //bool addbool4 = AddVariable(Struct, FEdGraphPinType(UEdGraphSchema_K2::PC_Boolean, NAME_None, nullptr, EPinContainerType::None, false, FEdGraphTerminalType()));
    //UE_LOG(LogBlueprint, Warning, TEXT("%d %d %d %d"), addbool1, addbool2, addbool3, addbool4);
    
    return Struct;

    //UUserDefinedStruct* Struct = NULL;

    ////if (UserDefinedStructEnabled())
    //
    //    
    //    UObject* Asset = CreateAsset(AssetPath, UUserDefinedStruct::StaticClass(), nullptr, success, OutInfoMessage);
    //    Struct = Cast<UUserDefinedStruct>(Asset);
    //    UE_LOG(LogBlueprint, Warning, TEXT("%s"), *OutInfoMessage);
    //    //check(Struct);
    //    Struct->EditorData = NewObject<UUserDefinedStructEditorData>(Struct, NAME_None, RF_Transactional);
    //    //check(Struct->EditorData);

    //    Struct->Guid = FGuid::NewGuid();
    //    Struct->SetMetaData(TEXT("BlueprintType"), TEXT("true"));
    //    Struct->Bind();
    //    Struct->StaticLink(true);
    //    Struct->Status = UDSS_Error;

    //    {
    //        FStructureEditorUtils::AddVariable(Struct, FEdGraphPinType(UEdGraphSchema_K2::PC_Int, NAME_None, nullptr, EPinContainerType::None, false, FEdGraphTerminalType()));
    //    }
    //

    //return Struct;

    //UObject* Asset = CreateAsset(AssetPath, UUserDefinedStruct::StaticClass(), nullptr, success, OutInfoMessage);
    //UUserDefinedStruct * Struct = Cast<UUserDefinedStruct>(Asset);
    //
    //FEdGraphPinType VarType =
    //    FEdGraphPinType(UEdGraphSchema_K2::PC_Int, NAME_None, nullptr, EPinContainerType::None, false, FEdGraphTerminalType());


    //FStructureEditorUtils::AddVariable(Struct, FEdGraphPinType(UEdGraphSchema_K2::PC_Boolean, NAME_None, nullptr, EPinContainerType::None, false, FEdGraphTerminalType()));
    //return Struct;

    ///*if (Struct)*/
    //{ 
    //    const FScopedTransaction Transaction();
    //    
    //    FStructureEditorUtils::ModifyStructData(Struct);

    //    FString ErrorMessage;
    //    if (!FStructureEditorUtils::CanHaveAMemberVariableOfType(Struct, VarType, &ErrorMessage))
    //    {
    //        UE_LOG(LogBlueprint, Warning, TEXT("%s"), *ErrorMessage);
    //        return nullptr;
    //    }

    //    const FGuid Guid = FGuid::NewGuid();
    //    FString DisplayName;
    //    const FName VarName = FMemberVariableNameHelper::Generate(Struct, FString("ASDF"), Guid, &DisplayName);
    //    bool hasDesc = (NULL != FStructureEditorUtils::GetVarDesc(Struct).FindByPredicate(FStructureEditorUtils::FFindByNameHelper<FStructVariableDescription>(VarName)));
    //    bool isUniqueName = (FStructureEditorUtils::IsUniqueVariableFriendlyName(Struct, DisplayName));

    //    FStructVariableDescription NewVar;
    //    NewVar.VarName = VarName;
    //    NewVar.FriendlyName = DisplayName;
    //    NewVar.SetPinType(VarType);
    //    NewVar.VarGuid = Guid;
    //    FStructureEditorUtils::GetVarDesc(Struct).Add(NewVar);

    //    FStructureEditorUtils::OnStructureChanged(Struct, FStructureEditorUtils::EStructureEditorChangeInfo::AddedVariable);
    //}


    //return Struct;
}
