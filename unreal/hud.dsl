; BP_VVHud EventGraph (write with write_graph_dsl). Minimap bottom-left: RT_Minimap (300 m across, north up) in a dark
; frame, the player as a clay dot in the middle, the current objective (BP_Missions' Marker) as a yellow square that
; sticks to the edge when it is off the map. Screen up is world +X, screen right is world +Y; 240 px / 30000 cm = 0.008.
(event EventReceiveDrawHUD (SizeX SizeY)
  (bind top (- SizeY 264.0))
  (bind pawnloc (Transformation|GetActorLocation (Game|GetPlayerPawn 0)))
  (bind goal (Transformation|GetWorldLocation (Class|BPMissions|GetMarker (Actor|GetActorOfClass :ActorClass "/Game/VancouverVice/BP_Missions.BP_Missions_C"))))
  (HUD|DrawRect :RectColor "(R=0.020000,G=0.022000,B=0.030000,A=0.700000)" :ScreenX 16.0 :ScreenY (- top 4.0) :ScreenW 256.0 :ScreenH 256.0)
  (HUD|DrawTextureSimple :Texture "/Game/VancouverVice/HUD/RT_Minimap.RT_Minimap" :ScreenX 24.0 :ScreenY (+ top 4.0) :Scale 0.46875)
  (HUD|DrawRect :RectColor "(R=1.000000,G=0.800000,B=0.050000,A=1.000000)"
    :ScreenX (Math|Float|Clamp(Float) (+ 139.0 (* 0.008 (- (.y goal) (.y pawnloc)))) 26.0 254.0)
    :ScreenY (Math|Float|Clamp(Float) (+ (+ top 119.0) (* -0.008 (- (.x goal) (.x pawnloc)))) (+ top 6.0) (+ top 234.0))
    :ScreenW 10.0 :ScreenH 10.0)
  (HUD|DrawRect :RectColor "(R=0.710000,G=0.314000,B=0.173000,A=1.000000)" :ScreenX 140.0 :ScreenY (+ top 120.0) :ScreenW 8.0 :ScreenH 8.0))
