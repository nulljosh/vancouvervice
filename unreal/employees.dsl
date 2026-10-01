; BP_AppleEmployee. Chases the player when nearby, grabs at close range, ragdolls on damage.
; Parent: Character. Mesh: M_Mannequin, tinted blue via dynamic material instance.

(event EventBeginPlay
  ; Set walk speed to 450
  (Pawn|CharacterMovement|SetMaxWalkSpeed :self self :MaxWalkSpeed 450.0)
  ; UNCERTAIN: Create a dynamic material instance for the blue shirt tint.
  ; May need to use SetVectorParameterValue for a color instead of SetScalarParameterValue.
  ; Test in editor to confirm tint applies correctly.
  (bind mesh (Rendering|GetSkeletalMeshComponent :self self))
  (bind matInst (Rendering|CreateDynamicMaterialInstance :self self :SourceMaterial 0))
  (Rendering|SetScalarParameterValue :self self :ParameterName "Tint" :ParameterValue 0.3)
  (Rendering|SetMaterial :self mesh :MaterialIndex 0 :NewMaterial matInst)
  ; Initialize grab cooldown
  (Variables|Default|SetGrabCooldown 0.0))

(event EventTick (DeltaSeconds)
  (bind pawn (Game|GetPlayerPawn 0))
  (bind myLoc (Transformation|GetActorLocation :self self))
  (bind playerLoc (Transformation|GetActorLocation :self pawn))
  (bind dist (Math|Vector|Distance myLoc playerLoc))
  ; Move toward player if within 4000 cm
  (if (<= dist 4000.0)
    (bind delta (Math|Vector|Subtract playerLoc myLoc))
    (bind dir (Math|Vector|Normal delta))
    (Pawn|AddMovementInput :self self :WorldDirection dir :ScaleValue 1.0))
  ; Grab message if within 150 cm and cooldown expired
  (if (<= dist 150.0)
    (bind cooldown (Variables|Default|GetGrabCooldown))
    (if (<= cooldown 0.0)
      (Development|PrintString "The employee grabs the bag!" :Duration 0.0)
      (Variables|Default|SetGrabCooldown 2.0))
    (else
      (Variables|Default|SetGrabCooldown (- cooldown DeltaSeconds)))))

(event EventAnyDamage (DamageAmount DamageType InstigatedBy DamageCauser)
  ; Ragdoll on damage
  (bind mesh (Rendering|GetSkeletalMeshComponent :self self))
  (Rendering|SetSimulatePhysics :self mesh :NewSimulate true)
  ; Destroy after 3 seconds
  (Utilities|FlowControl|Delay :Duration 3.0)
  (Actor|Destroy :self self))
