; Additions to BP_Missions for mission one.
; Add these nodes to the existing EventBeginPlay (after tile setup, before the rest).
; Spawns two blue-shirt employees who chase the player from the Apple Store start.

; ATTACH TO: EventBeginPlay (after line 6, before the rest)
(bind spawnClass (Utilities|Class|LoadClassFromPath "/Game/VancouverVice/Blueprints/BP_AppleEmployee.BP_AppleEmployee_C"))
(bind pawn (Game|GetPlayerPawn 0))
(bind playerStart (Transformation|GetActorLocation :self pawn))
; UNCERTAIN: Using GetActorForwardVector; may need GetActorRightVector for left/right offsets.
; Spawn location is 300cm behind player, Y offset left/right by 120cm each.
(bind playerForward (Transformation|GetActorForwardVector :self pawn))
(bind playerRight (Transformation|GetActorRightVector :self pawn))
; Left employee: back 300, left 120
(bind offset1 (Math|Vector|Add
  (Math|Vector|Multiply playerForward -300.0)
  (Math|Vector|Multiply playerRight -120.0)))
(bind loc1 (Math|Vector|Add playerStart offset1))
(bind transform1 (Transformation|MakeTransform :Location loc1 :Rotation (Transformation|GetActorRotation pawn) :Scale (Math|Vector|MakeVector 1.0 1.0 1.0)))
(bind emp1 (Actor|SpawnActor :Class spawnClass :SpawnTransform transform1))
; Right employee: back 300, right 120
(bind offset2 (Math|Vector|Add
  (Math|Vector|Multiply playerForward -300.0)
  (Math|Vector|Multiply playerRight 120.0)))
(bind loc2 (Math|Vector|Add playerStart offset2))
(bind transform2 (Transformation|MakeTransform :Location loc2 :Rotation (Transformation|GetActorRotation pawn) :Scale (Math|Vector|MakeVector 1.0 1.0 1.0)))
(bind emp2 (Actor|SpawnActor :Class spawnClass :SpawnTransform transform2))
; Print tutorial message with 8 second duration
(Development|PrintString "Mouse: aim. Click: fire. Keep them off the bag. E at the car." :Duration 8.0 :Key "tutorial")
