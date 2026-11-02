; BP_ThirdPersonCharacter UserConstructionScript. Mesh is inherited from Character, so a component edit reverts on restart:
; the construction script sets it. Mesh is Joshua (Higgsfield rig, metre scale) running ABP_Unarmed retargeted from Manny
; (unreal/import_hero.py). The old MetaHuman pieces (Body, Face, Polo, Pants, HairShell, Hair, Glasses) are hidden in game.
(fn ConstructionScript ()
  (Components|SkeletalMesh|SetSkeletalMeshAsset (Variables|Character|GetMesh) "/Game/Characters/Joshua2/JoshuaHero_m/SkeletalMeshes/JoshuaHero_m.JoshuaHero_m")
  (Components|SkeletalMesh|SetAnimInstanceClass (Variables|Character|GetMesh) "/Game/Characters/Joshua2/Anims/ABP_Unarmed_J2.ABP_Unarmed_J2_C"))
