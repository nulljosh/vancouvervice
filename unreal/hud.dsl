; BP_VVHud EventGraph (write with write_graph_dsl). Minimap bottom-left: RT_Minimap (300 m across, north up) in a dark
; frame, the player as a clay dot in the middle, the current objective (BP_Missions' Marker) as a yellow square that
; sticks to the edge when it is off the map. Screen up is world +X, screen right is world +Y; 240 px / 30000 cm = 0.008.
; Top right: five wanted stars (squares, white when lit). BUSTED across the middle while BP_Missions.Busted counts down.
(event EventReceiveDrawHUD (SizeX SizeY)
  (bind top (- SizeY 264.0))
  (bind pawnloc (Transformation|GetActorLocation (Game|GetPlayerPawn 0)))
  (bind m (Actor|GetActorOfClass :ActorClass "/Game/VancouverVice/BP_Missions.BP_Missions_C"))
  (bind goal (Transformation|GetWorldLocation (Class|BPMissions|GetMarker m)))
  (bind stars (Class|BPMissions|GetStars m))
  ; Title screen while BP_Missions.Menu: the key art full screen (2048 x 1152, same 16:9), and the menu inside its
  ; bottom-left comic panel (x 0.9 to 31.6%, y 65.6 to 98.4% of the art), darkened, in Anton. Red bar = selection.
  (if (Class|BPMissions|GetMenu m)
    (HUD|DrawTextureSimple :Texture "/Game/VancouverVice/HUD/T_KeyArt.T_KeyArt" :ScreenX 0.0 :ScreenY 0.0 :Scale (/ SizeX 2048.0))
    (HUD|DrawRect :RectColor "(R=0.010000,G=0.010000,B=0.015000,A=0.820000)" :ScreenX (* SizeX 0.009) :ScreenY (* SizeY 0.656) :ScreenW (* SizeX 0.307) :ScreenH (* SizeY 0.328))
    (HUD|DrawRect :RectColor "(R=0.750000,G=0.170000,B=0.120000,A=1.000000)" :ScreenX (* SizeX 0.009) :ScreenY (+ (* SizeY 0.69) (* 64.0 (Class|BPMissions|GetMenuSel m))) :ScreenW (* SizeX 0.307) :ScreenH 52.0)
    (HUD|DrawText :Text "STORY MODE" :TextColor "(R=1.000000,G=1.000000,B=1.000000,A=1.000000)" :ScreenX (+ (* SizeX 0.009) 28.0) :ScreenY (+ (* SizeY 0.69) 4.0) :Font "/Game/VancouverVice/HUD/F_Anton.F_Anton" :Scale 0.75)
    (HUD|DrawText :Text "QUIT GAME" :TextColor "(R=1.000000,G=1.000000,B=1.000000,A=1.000000)" :ScreenX (+ (* SizeX 0.009) 28.0) :ScreenY (+ (* SizeY 0.69) 68.0) :Font "/Game/VancouverVice/HUD/F_Anton.F_Anton" :Scale 0.75)
    (HUD|DrawText :Text "ENTER  Select      W / S  Move" :TextColor "(R=0.700000,G=0.700000,B=0.720000,A=1.000000)" :ScreenX (+ (* SizeX 0.009) 28.0) :ScreenY (- (* SizeY 0.984) 40.0) :Scale 1.2)
    (else
    (HUD|DrawRect :RectColor "(R=0.020000,G=0.022000,B=0.030000,A=0.700000)" :ScreenX 16.0 :ScreenY (- top 4.0) :ScreenW 256.0 :ScreenH 256.0)
    (HUD|DrawTextureSimple :Texture "/Game/VancouverVice/HUD/RT_Minimap.RT_Minimap" :ScreenX 24.0 :ScreenY (+ top 4.0) :Scale 0.46875)
    (HUD|DrawRect :RectColor "(R=1.000000,G=0.800000,B=0.050000,A=1.000000)"
      :ScreenX (Math|Float|Clamp(Float) (+ 139.0 (* 0.008 (- (.y goal) (.y pawnloc)))) 26.0 254.0)
      :ScreenY (Math|Float|Clamp(Float) (+ (+ top 119.0) (* -0.008 (- (.x goal) (.x pawnloc)))) (+ top 6.0) (+ top 234.0))
      :ScreenW 10.0 :ScreenH 10.0)
    (HUD|DrawRect :RectColor "(R=0.710000,G=0.314000,B=0.173000,A=1.000000)" :ScreenX 140.0 :ScreenY (+ top 120.0) :ScreenW 8.0 :ScreenH 8.0)
    (HUD|DrawRect :RectColor "(R=0.020000,G=0.022000,B=0.030000,A=0.550000)" :ScreenX (- SizeX 160.0) :ScreenY 28.0 :ScreenW 22.0 :ScreenH 22.0)
    (HUD|DrawRect :RectColor "(R=1.000000,G=1.000000,B=1.000000,A=1.000000)" :ScreenX (- SizeX 160.0) :ScreenY 28.0 :ScreenW (select (>= stars 1) 22.0 0.0) :ScreenH 22.0)
    (HUD|DrawRect :RectColor "(R=0.020000,G=0.022000,B=0.030000,A=0.550000)" :ScreenX (- SizeX 130.0) :ScreenY 28.0 :ScreenW 22.0 :ScreenH 22.0)
    (HUD|DrawRect :RectColor "(R=1.000000,G=1.000000,B=1.000000,A=1.000000)" :ScreenX (- SizeX 130.0) :ScreenY 28.0 :ScreenW (select (>= stars 2) 22.0 0.0) :ScreenH 22.0)
    (HUD|DrawRect :RectColor "(R=0.020000,G=0.022000,B=0.030000,A=0.550000)" :ScreenX (- SizeX 100.0) :ScreenY 28.0 :ScreenW 22.0 :ScreenH 22.0)
    (HUD|DrawRect :RectColor "(R=1.000000,G=1.000000,B=1.000000,A=1.000000)" :ScreenX (- SizeX 100.0) :ScreenY 28.0 :ScreenW (select (>= stars 3) 22.0 0.0) :ScreenH 22.0)
    (HUD|DrawRect :RectColor "(R=0.020000,G=0.022000,B=0.030000,A=0.550000)" :ScreenX (- SizeX 70.0) :ScreenY 28.0 :ScreenW 22.0 :ScreenH 22.0)
    (HUD|DrawRect :RectColor "(R=1.000000,G=1.000000,B=1.000000,A=1.000000)" :ScreenX (- SizeX 70.0) :ScreenY 28.0 :ScreenW (select (>= stars 4) 22.0 0.0) :ScreenH 22.0)
    (HUD|DrawRect :RectColor "(R=0.020000,G=0.022000,B=0.030000,A=0.550000)" :ScreenX (- SizeX 40.0) :ScreenY 28.0 :ScreenW 22.0 :ScreenH 22.0)
    (HUD|DrawRect :RectColor "(R=1.000000,G=1.000000,B=1.000000,A=1.000000)" :ScreenX (- SizeX 40.0) :ScreenY 28.0 :ScreenW (select (>= stars 5) 22.0 0.0) :ScreenH 22.0)
    ; GTA V bar under the map: health (green) on the left half, armour (blue, empty for now) on the right.
    (HUD|DrawRect :RectColor "(R=0.020000,G=0.022000,B=0.030000,A=0.800000)" :ScreenX 16.0 :ScreenY (+ top 253.0) :ScreenW 256.0 :ScreenH 9.0)
    (HUD|DrawRect :RectColor "(R=0.090000,G=0.200000,B=0.110000,A=1.000000)" :ScreenX 18.0 :ScreenY (+ top 255.0) :ScreenW 125.0 :ScreenH 5.0)
    (HUD|DrawRect :RectColor "(R=0.300000,G=0.700000,B=0.330000,A=1.000000)" :ScreenX 18.0 :ScreenY (+ top 255.0)
      :ScreenW (* 1.25 (Math|Float|Clamp(Float) (Class|BPMissions|GetHealth m) 0.0 100.0)) :ScreenH 5.0)
    (HUD|DrawRect :RectColor "(R=0.080000,G=0.140000,B=0.240000,A=1.000000)" :ScreenX 145.0 :ScreenY (+ top 255.0) :ScreenW 125.0 :ScreenH 5.0)
    ; WASTED / BUSTED: a dark band across the middle of the screen behind the word, like GTA V.
    (if (or (> (Class|BPMissions|GetWasted m) 0.0) (> (Class|BPMissions|GetBusted m) 0.0))
      (HUD|DrawRect :RectColor "(R=0.000000,G=0.000000,B=0.000000,A=0.550000)" :ScreenX 0.0 :ScreenY (- (* SizeY 0.4) 20.0) :ScreenW SizeX :ScreenH 150.0))
    (if (> (Class|BPMissions|GetWasted m) 0.0)
      (HUD|DrawText :Text "WASTED" :TextColor "(R=0.780000,G=0.090000,B=0.070000,A=1.000000)" :ScreenX (- (* SizeX 0.5) 170.0) :ScreenY (* SizeY 0.4) :Font "/Game/VancouverVice/HUD/F_Anton.F_Anton" :Scale 2.2))
    (if (> (Class|BPMissions|GetBusted m) 0.0)
      (HUD|DrawText :Text "BUSTED" :TextColor "(R=0.780000,G=0.090000,B=0.070000,A=1.000000)" :ScreenX (- (* SizeX 0.5) 170.0) :ScreenY (* SizeY 0.4) :Font "/Game/VancouverVice/HUD/F_Anton.F_Anton" :Scale 2.2)))))
