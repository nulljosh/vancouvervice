; BP_ThirdPersonCharacter UserConstructionScript. Mesh is forced to Manny here: it is inherited from Character, so a component edit
; reverts on restart, and Quinn (the default) gave Joshua a female build through leader pose.
; Mesh (the hidden mannequin) animates; Body, Face, Polo and Pants copy its pose.
; Glasses ride the Mesh head socket. Hair rides the Face head bone: the mannequin is hidden in game and would hide it too.
(fn ConstructionScript ()
  (Components|SkeletalMesh|SetSkeletalMeshAsset (Variables|Character|GetMesh) "/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple.SKM_Manny_Simple")
  (Components|SkinnedMesh|SetLeaderPoseComponent (Variables|Default|GetBody) (Variables|Character|GetMesh))
  (Components|SkinnedMesh|SetLeaderPoseComponent (Variables|Default|GetFace) (Variables|Character|GetMesh))
  (Components|SkinnedMesh|SetLeaderPoseComponent (Variables|Default|GetPolo) (Variables|Character|GetMesh))
  (Components|SkinnedMesh|SetLeaderPoseComponent (Variables|Default|GetPants) (Variables|Character|GetMesh))
  (Components|SkinnedMesh|SetLeaderPoseComponent (Variables|Default|GetHairShell) (Variables|Character|GetMesh))
  (Transformation|AttachComponentToComponent (Variables|Default|GetGlasses) (Variables|Character|GetMesh) "head")
  (Transformation|AttachComponentToComponent (Variables|Default|GetHair) (Variables|Default|GetFace) "head")
  (Transformation|AttachComponentToComponent (Variables|Default|GetHairCards) (Variables|Default|GetFace) "head"))
