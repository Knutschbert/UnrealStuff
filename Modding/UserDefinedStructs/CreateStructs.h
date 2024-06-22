// Nihi 2024. All Rights Reserved perhaps.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "Kismet2/StructureEditorUtils.h"
#include "CreateStructs.generated.h"

class UFactory;
class UUserDefinedEnum;
class UUserDefinedStruct;
class UWorld;

/**
 * 
 */

USTRUCT(BlueprintType)
struct FCreateStructsDTFmt : public FTableRowBase
{
public:
	GENERATED_BODY()
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString File;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Class_Name;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Property_Class_Name;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Friendly_Name;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Name_ID;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Name_GUID;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Dir;

	DLLEXPORT FCreateStructsDTFmt() {}
};


UCLASS()
class ASSETGENERATOR_API UCreateStructs : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()

		UFUNCTION(BlueprintCallable, Category = "Nihi|Create Assets")
		static UObject* CreateAsset(FString AssetPath, UClass* AssetClass, UFactory* AssetFactory, bool& success, FString& OutInfoMessage);


	UFUNCTION(BlueprintCallable, Category = "Nihi|Create Assets")
		static UWorld* CreateWorldAsset(FString AssetPath, bool& success, FString& OutInfoMessage);

	UFUNCTION(BlueprintCallable, Category = "Nihi|Create Assets")
		static UUserDefinedEnum* CreateEnumAsset(FString AssetPath, bool& success, FString& OutInfoMessage);

	UFUNCTION(BlueprintCallable, Category = "Nihi|Create Assets")
		static UUserDefinedStruct* CreateStructAsset(FString AssetPath, bool& success, FString& OutInfoMessage);
public:
	//void * CreateAsset()
	
};
