; BP_Missions EventGraph (read back with read_graph_dsl, edited, written with write_graph_dsl). The objective is a
; glowing beam (Marker component, M_Marker) instead of a debug sphere.
(event Collision|EventActorBeginOverlap (OtherActor))

(event EventTick (DeltaSeconds)
  (bind _returnvalue (Game|GetPlayerPawn 0))
  (bind _returnvalue_1 (Transformation|GetActorLocation _returnvalue))
  (bind _index (Variables|Default|GetIndex))
  (bind _targets (Variables|Default|GetTargets))
  (bind _output (Utilities|Array|Get(acopy) _targets _index))
  (bind _missionnames (Variables|Default|GetMissionNames))
  (bind _output_1 (Utilities|Array|Get(acopy) _missionnames _index))
  (bind _returnvalue_3 (== _index 1))
  (if (< _index (Utilities|Array|Length _targets))
    (bind _returnvalue_5 (Actor|GetActorOfClass "/Game/VehicleTemplate/Blueprints/SportsCar/BP_VehicleAdvSportsCar.BP_VehicleAdvSportsCar_C"))
    (Transformation|SetWorldLocation :self (Variables|Default|GetMarker) :NewLocation (Math|Vector|MakeVector (.x (select _returnvalue_3 (Transformation|GetActorLocation _returnvalue_5) _output)) (.y (select _returnvalue_3 (Transformation|GetActorLocation _returnvalue_5) _output)) (+ (.z _returnvalue_1) 1160.0)))
    (Development|PrintString (Utilities|String|Append "Mission: " _output_1) true true "(R=0.000000,G=0.660000,B=1.000000,A=1.000000)" 0.0 "mission")
    (if (or (and _returnvalue_3 (== _returnvalue _returnvalue_5)) (and (not _returnvalue_3) (< (Math|Vector|Distance2D(Vector) _returnvalue_1 _output) 400.0)))
      (Development|PrintString (Utilities|String|Append "Mission complete: " _output_1) true true "(R=0.000000,G=0.660000,B=1.000000,A=1.000000)" 4.0)
      (Variables|Default|SetIndex (+ _index 1)))
    (else
      (Transformation|SetWorldLocation :self (Variables|Default|GetMarker) :NewLocation (Math|Vector|MakeVector 0.0 0.0 -100000.0))
      (Development|PrintString "All missions done. Vancouver is yours." true true "(R=0.000000,G=0.660000,B=1.000000,A=1.000000)" 0.0 "mission"))))

