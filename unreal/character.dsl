; BP_ThirdPersonCharacter UserConstructionScript. Mesh (the hidden mannequin) animates; Body, Face, Polo and Pants copy its pose.
; Glasses and Hair ride the Mesh head socket.
(fn ConstructionScript ()
  (Components|SkinnedMesh|SetLeaderPoseComponent (Variables|Default|GetBody) (Variables|Character|GetMesh))
  (Components|SkinnedMesh|SetLeaderPoseComponent (Variables|Default|GetFace) (Variables|Character|GetMesh))
  (Components|SkinnedMesh|SetLeaderPoseComponent (Variables|Default|GetPolo) (Variables|Character|GetMesh))
  (Components|SkinnedMesh|SetLeaderPoseComponent (Variables|Default|GetPants) (Variables|Character|GetMesh))
  (Transformation|AttachComponentToComponent (Variables|Default|GetGlasses) (Variables|Character|GetMesh) "head")
  (Transformation|AttachComponentToComponent (Variables|Default|GetHair) (Variables|Character|GetMesh) "head"))
