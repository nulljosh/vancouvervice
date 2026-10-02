; BP_ThirdPersonCharacter UserConstructionScript. Mesh (the hidden mannequin) animates; Body, Face, Polo and Pants copy its pose.
; Glasses ride the Mesh head socket. Hair rides the Face head bone: the mannequin is hidden in game and would hide it too.
(fn ConstructionScript ()
  (Components|SkinnedMesh|SetLeaderPoseComponent (Variables|Default|GetBody) (Variables|Character|GetMesh))
  (Components|SkinnedMesh|SetLeaderPoseComponent (Variables|Default|GetFace) (Variables|Character|GetMesh))
  (Components|SkinnedMesh|SetLeaderPoseComponent (Variables|Default|GetPolo) (Variables|Character|GetMesh))
  (Components|SkinnedMesh|SetLeaderPoseComponent (Variables|Default|GetPants) (Variables|Character|GetMesh))
  (Transformation|AttachComponentToComponent (Variables|Default|GetGlasses) (Variables|Character|GetMesh) "head")
  (Transformation|AttachComponentToComponent (Variables|Default|GetHair) (Variables|Default|GetFace) "head"))
