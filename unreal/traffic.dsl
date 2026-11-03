; BP_TrafficCar EventGraph. Drives the car round its Points loop (lane points from the real roads, set by
; unreal/traffic.py) at Speed cm/s, turning smoothly toward each point.
(event EventTick (DeltaSeconds)
  (bind pts (Variables|Default|GetPoints))
  (bind n (Utilities|Array|Length pts))
  (if (> n 1)
    (bind i (Variables|Default|GetIndex))
    (bind target (Utilities|Array|Get(acopy) pts i))
    (bind loc (Transformation|GetActorLocation))
    (bind next (Math|Interpolation|VInterptoConstant loc target DeltaSeconds (Variables|Default|GetSpeed)))
    (bind look (Math|Rotator|FindLookatRotation loc target))
    (bind rot (Math|Interpolation|RInterpTo (Transformation|GetActorRotation) (Math|Rotator|MakeRotator :Roll 0.0 :Pitch 0.0 :Yaw (.yaw look)) DeltaSeconds 4.0))
    (Transformation|SetActorLocationAndRotation :NewLocation next :NewRotation rot)
    (bind walker (Utilities|Casting|CastToCharacter (Game|GetPlayerPawn 0)))
    ; hit Joshua on foot: the car's pivot is on the ground at its centre, so measure flat (Distance2D) and allow half a car
    ; length plus his capsule. 280 cm in 3D never fired (the capsule centre sits 90 cm up). Not before Story Mode starts.
    (bind m (Actor|GetActorOfClass :ActorClass "/Game/VancouverVice/BP_Missions.BP_Missions_C"))
    (if (and (and (Utilities|IsValid walker) (Class|BPMissions|GetStarted m)) (< (Math|Vector|Distance2D(Vector) next (Transformation|GetActorLocation walker)) 320.0))
      (Class|BPMissions|SetHealth :self m :Health (- (Class|BPMissions|GetHealth m) (* 400.0 DeltaSeconds)))
      (bind fwd (Transformation|GetActorForwardVector))
      (Character|LaunchCharacter :self walker :LaunchVelocity (Math|Vector|MakeVector (* 1400.0 (.x fwd)) (* 1400.0 (.y fwd)) 500.0) :bXYOverride true :bZOverride true))
    (if (< (Math|Vector|Distance(Vector) next target) 120.0)
      (Variables|Default|SetIndex (select (>= (+ i 1) n) 0 (+ i 1))))))
