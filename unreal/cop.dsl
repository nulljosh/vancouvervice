; BP_CopCar EventGraph. Parked until BP_Missions has Stars; then it drives BP_Missions' Trail (where the player has
; driven, so it keeps to real roads) at 27 m/s, and once it has caught up with the end of the trail it goes straight
; for the player. The light bar flashes red and blue while it chases.
(event EventTick (DeltaSeconds)
  (bind m (Actor|GetActorOfClass :ActorClass "/Game/VancouverVice/BP_Missions.BP_Missions_C"))
  (bind chasing (> (Class|BPMissions|GetStars m) 0))
  (Rendering|SetVisibility :self (Variables|Default|GetLightRed) :bNewVisibility (and chasing (> (Math|Trig|Sin(Radians) (* (Utilities|Time|GetGameTimeinSeconds) 12.0)) 0.0)))
  (Rendering|SetVisibility :self (Variables|Default|GetLightBlue) :bNewVisibility (and chasing (<= (Math|Trig|Sin(Radians) (* (Utilities|Time|GetGameTimeinSeconds) 12.0)) 0.0)))
  (if chasing
    (bind pts (Class|BPMissions|GetTrail m))
    (bind n (Utilities|Array|Length pts))
    (bind i (Variables|Default|GetIndex))
    (bind pawnloc (Transformation|GetActorLocation (Game|GetPlayerPawn 0)))
    (bind target (select (< i n) (Utilities|Array|Get(acopy) pts i) (Math|Vector|MakeVector (.x pawnloc) (.y pawnloc) -6840.0)))
    (bind loc (Transformation|GetActorLocation))
    (bind next (Math|Interpolation|VInterptoConstant loc target DeltaSeconds 2700.0))
    (bind look (Math|Rotator|FindLookatRotation loc target))
    (bind rot (Math|Interpolation|RInterpTo (Transformation|GetActorRotation) (Math|Rotator|MakeRotator :Roll 0.0 :Pitch 0.0 :Yaw (.yaw look)) DeltaSeconds 5.0))
    (Transformation|SetActorLocationAndRotation :NewLocation next :NewRotation rot)
    (if (and (< i n) (< (Math|Vector|Distance(Vector) next target) 300.0))
      (Variables|Default|SetIndex (+ i 1)))))
