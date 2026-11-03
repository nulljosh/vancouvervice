; BP_VVHud EventGraph (write with write_graph_dsl). Three screens, all drawn on the canvas in GTA V's layout:
; 1. Startup (BP_Missions.Started false): one key-art panel (site/img/key-art.png) full bleed at a time, slowly zooming,
;    next panel every 6 s, the title card bottom-left, key hints bottom-right.
; 2. Pause (Menu after Started, Esc): game dimmed, title top-left, name and mission count top-right, a full-width tab bar
;    (MAP BRIEF STATS SETTINGS GAME, selected tab white with black text and a red strip on top), the tab's content
;    under it, key hints bottom-right. Black-on-white labels are drawn over the white labels (canvas has no per-item colour).
; 3. Game HUD: minimap bottom-left (RT_Minimap, 300 m across, north up; 240 px / 30000 cm = 0.008), health bar under it,
;    wanted stars top-right, the objective as a subtitle bottom-centre, MISSION PASSED / WASTED / BUSTED bands.
; Panel UVs: the art is 2048 x 1152, so a 16:9 crop is as wide in U as it is tall in V (s by s).
(event EventReceiveDrawHUD (SizeX SizeY)
  (bind top (- SizeY 264.0))
  (bind pawnloc (Transformation|GetActorLocation (Game|GetPlayerPawn 0)))
  (bind m (Actor|GetActorOfClass :ActorClass "/Game/VancouverVice/BP_Missions.BP_Missions_C"))
  (bind goal (Transformation|GetWorldLocation (Class|BPMissions|GetMarker m)))
  (bind stars (Class|BPMissions|GetStars m))
  (bind mt (Class|BPMissions|GetMenuT m))
  (bind tab (Class|BPMissions|GetMenuTab m))
  (bind sel (Class|BPMissions|GetMenuSel m))
  (bind idx (Class|BPMissions|GetIndex m))
  (bind names (Class|BPMissions|GetMissionNames m))
  (bind nmiss (Utilities|Array|Length names))
  (if (not (Class|BPMissions|GetStarted m))
    (bind p (Class|BPMissions|GetMenuPanel m))
    ; T_MenuArt is a 2 x 2 atlas of 16:9 Higgsfield panels (brand/menu/panel0-3: downtown towers, English Bay, Joshua
    ; leaving the store, the car chase); each panel is a 0.5 x 0.5 UV square, slowly zooming toward its centre.
    (bind s (* 0.5 (- 1.0 (* 0.012 mt))))
    (bind u0 (+ (select (or (== p 1) (== p 3)) 0.5 0.0) (* 0.5 (- 0.5 s))))
    (bind v0 (+ (select (>= p 2) 0.5 0.0) (* 0.5 (- 0.5 s))))
    (HUD|DrawRect :RectColor "(R=0.000000,G=0.000000,B=0.000000,A=1.000000)" :ScreenX 0.0 :ScreenY 0.0 :ScreenW SizeX :ScreenH SizeY)
    (HUD|DrawTexture :Texture "/Game/VancouverVice/HUD/T_MenuArt.T_MenuArt" :ScreenX 0.0 :ScreenY 0.0 :ScreenW SizeX :ScreenH SizeY
      :TextureU u0 :TextureV v0 :TextureUWidth s :TextureVHeight s)
    ; brand: on art, a 48 percent black scrim behind the wordmark (never a gradient); it also carries the key hints
    (HUD|DrawRect :RectColor "(R=0.000000,G=0.000000,B=0.000000,A=0.480000)" :ScreenX 0.0 :ScreenY (* SizeY 0.66) :ScreenW SizeX :ScreenH (* SizeY 0.34))
    ; logo (brand/app-icon lettering, T_Logo 1024 x 512, transparent), bottom-left
    (HUD|DrawTexture :Texture "/Game/VancouverVice/HUD/T_Logo.T_Logo" :ScreenX (* SizeX 0.035) :ScreenY (- SizeY (+ (* SizeX 0.15) (* SizeY 0.05))) :ScreenW (* SizeX 0.3) :ScreenH (* SizeX 0.15)
      :TextureU 0.0 :TextureV 0.0 :TextureUWidth 1.0 :TextureVHeight 1.0 :BlendMode "BLEND_Translucent")
    ; save slots (Enter from the startup art): GTA V list, selected row white with black text
    (if (== (Class|BPMissions|GetTitleStep m) 1)
        (HUD|DrawRect :RectColor "(R=0.000000,G=0.000000,B=0.000000,A=0.450000)" :ScreenX 0.0 :ScreenY 0.0 :ScreenW SizeX :ScreenH SizeY)
        (HUD|DrawText :Text "STORY MODE" :TextColor "(R=0.896000,G=0.879000,B=0.839000,A=1.000000)" :ScreenX (* SizeX 0.1) :ScreenY (* SizeY 0.17) :Font "/Game/VancouverVice/HUD/F_Anton.F_Anton" :Scale 1.05)
        (HUD|DrawRect :RectColor "(R=0.007500,G=0.008500,B=0.012300,A=0.820000)" :ScreenX (* SizeX 0.1) :ScreenY (+ (* SizeY 0.3) 0.0) :ScreenW (* SizeX 0.36) :ScreenH 54.0)
        (HUD|DrawText :Text (Utilities|String|Append "Slot 1      " (select (< (Class|BPMissions|GetSlot0 m) 0) "New game" (Utilities|String|Append "Mission " (Utilities|String|Append (Utilities|String|ToString(Integer) (Math|Integer|Min(Integer) (+ (Class|BPMissions|GetSlot0 m) 1) nmiss)) (Utilities|String|Append " of " (Utilities|String|ToString(Integer) nmiss))))))
          :TextColor "(R=0.896000,G=0.879000,B=0.839000,A=1.000000)" :ScreenX (+ (* SizeX 0.1) 20.0) :ScreenY (+ (* SizeY 0.3) 16.0) :Scale 1.4)
        (HUD|DrawRect :RectColor "(R=0.007500,G=0.008500,B=0.012300,A=0.820000)" :ScreenX (* SizeX 0.1) :ScreenY (+ (* SizeY 0.3) 58.0) :ScreenW (* SizeX 0.36) :ScreenH 54.0)
        (HUD|DrawText :Text (Utilities|String|Append "Slot 2      " (select (< (Class|BPMissions|GetSlot1 m) 0) "New game" (Utilities|String|Append "Mission " (Utilities|String|Append (Utilities|String|ToString(Integer) (Math|Integer|Min(Integer) (+ (Class|BPMissions|GetSlot1 m) 1) nmiss)) (Utilities|String|Append " of " (Utilities|String|ToString(Integer) nmiss))))))
          :TextColor "(R=0.896000,G=0.879000,B=0.839000,A=1.000000)" :ScreenX (+ (* SizeX 0.1) 20.0) :ScreenY (+ (* SizeY 0.3) 74.0) :Scale 1.4)
        (HUD|DrawRect :RectColor "(R=0.007500,G=0.008500,B=0.012300,A=0.820000)" :ScreenX (* SizeX 0.1) :ScreenY (+ (* SizeY 0.3) 116.0) :ScreenW (* SizeX 0.36) :ScreenH 54.0)
        (HUD|DrawText :Text (Utilities|String|Append "Slot 3      " (select (< (Class|BPMissions|GetSlot2 m) 0) "New game" (Utilities|String|Append "Mission " (Utilities|String|Append (Utilities|String|ToString(Integer) (Math|Integer|Min(Integer) (+ (Class|BPMissions|GetSlot2 m) 1) nmiss)) (Utilities|String|Append " of " (Utilities|String|ToString(Integer) nmiss))))))
          :TextColor "(R=0.896000,G=0.879000,B=0.839000,A=1.000000)" :ScreenX (+ (* SizeX 0.1) 20.0) :ScreenY (+ (* SizeY 0.3) 132.0) :Scale 1.4)
        (bind slotinfo (select (== sel 0) (Class|BPMissions|GetSlot0 m) (select (== sel 1) (Class|BPMissions|GetSlot1 m) (Class|BPMissions|GetSlot2 m))))
        (HUD|DrawRect :RectColor "(R=0.896000,G=0.879000,B=0.839000,A=1.000000)" :ScreenX (* SizeX 0.1) :ScreenY (+ (* SizeY 0.3) (* 58.0 sel)) :ScreenW (* SizeX 0.36) :ScreenH 54.0)
        (HUD|DrawText :Text (Utilities|String|Append (Utilities|String|Append "Slot " (Utilities|String|ToString(Integer) (+ sel 1))) (Utilities|String|Append "      " (select (< slotinfo 0) "New game" (Utilities|String|Append "Mission " (Utilities|String|Append (Utilities|String|ToString(Integer) (Math|Integer|Min(Integer) (+ slotinfo 1) nmiss)) (Utilities|String|Append " of " (Utilities|String|ToString(Integer) nmiss)))))))
          :TextColor "(R=0.000000,G=0.000000,B=0.000000,A=1.000000)" :ScreenX (+ (* SizeX 0.1) 20.0) :ScreenY (+ (+ (* SizeY 0.3) (* 58.0 sel)) 16.0) :Scale 1.4))
    ; key hints, bottom-right: white key cap, black key name, white label
    (HUD|DrawRect :RectColor "(R=0.896000,G=0.879000,B=0.839000,A=1.000000)" :ScreenX (- SizeX 330.0) :ScreenY (- SizeY 64.0) :ScreenW 62.0 :ScreenH 26.0)
    (HUD|DrawText :Text "ENTER" :TextColor "(R=0.000000,G=0.000000,B=0.000000,A=1.000000)" :ScreenX (- SizeX 322.0) :ScreenY (- SizeY 60.0) :Scale 1.2)
    (HUD|DrawText :Text (select (== (Class|BPMissions|GetTitleStep m) 0) "Story Mode" "Play") :TextColor "(R=0.896000,G=0.879000,B=0.839000,A=1.000000)" :ScreenX (- SizeX 260.0) :ScreenY (- SizeY 60.0) :Scale 1.2)
    (HUD|DrawRect :RectColor "(R=0.896000,G=0.879000,B=0.839000,A=1.000000)" :ScreenX (- SizeX 150.0) :ScreenY (- SizeY 64.0) :ScreenW 44.0 :ScreenH 26.0)
    (HUD|DrawText :Text "ESC" :TextColor "(R=0.000000,G=0.000000,B=0.000000,A=1.000000)" :ScreenX (- SizeX 142.0) :ScreenY (- SizeY 60.0) :Scale 1.2)
    (HUD|DrawText :Text (select (== (Class|BPMissions|GetTitleStep m) 0) "Quit" "Back") :TextColor "(R=0.896000,G=0.879000,B=0.839000,A=1.000000)" :ScreenX (- SizeX 98.0) :ScreenY (- SizeY 60.0) :Scale 1.2)
    (else
      (if (Class|BPMissions|GetMenu m)
        ; @include hud_pause.dsl
        (else
          (HUD|DrawRect :RectColor "(R=0.020000,G=0.022000,B=0.030000,A=0.700000)" :ScreenX 16.0 :ScreenY (- top 4.0) :ScreenW 256.0 :ScreenH 256.0)
          (HUD|DrawTextureSimple :Texture "/Game/VancouverVice/HUD/RT_Minimap.RT_Minimap" :ScreenX 24.0 :ScreenY (+ top 4.0) :Scale 0.46875)
          (HUD|DrawRect :RectColor "(R=1.000000,G=0.800000,B=0.050000,A=1.000000)"
            :ScreenX (Math|Float|Clamp(Float) (+ 139.0 (* 0.008 (- (.y goal) (.y pawnloc)))) 26.0 254.0)
            :ScreenY (Math|Float|Clamp(Float) (+ (+ top 119.0) (* -0.008 (- (.x goal) (.x pawnloc)))) (+ top 6.0) (+ top 234.0))
            :ScreenW 10.0 :ScreenH 10.0)
          (HUD|DrawRect :RectColor "(R=0.710000,G=0.314000,B=0.173000,A=1.000000)" :ScreenX 140.0 :ScreenY (+ top 120.0) :ScreenW 8.0 :ScreenH 8.0)
          (HUD|DrawRect :RectColor "(R=0.020000,G=0.022000,B=0.030000,A=0.550000)" :ScreenX (- SizeX 160.0) :ScreenY 28.0 :ScreenW 22.0 :ScreenH 22.0)
          (HUD|DrawRect :RectColor "(R=0.896000,G=0.879000,B=0.839000,A=1.000000)" :ScreenX (- SizeX 160.0) :ScreenY 28.0 :ScreenW (select (>= stars 1) 22.0 0.0) :ScreenH 22.0)
          (HUD|DrawRect :RectColor "(R=0.020000,G=0.022000,B=0.030000,A=0.550000)" :ScreenX (- SizeX 130.0) :ScreenY 28.0 :ScreenW 22.0 :ScreenH 22.0)
          (HUD|DrawRect :RectColor "(R=0.896000,G=0.879000,B=0.839000,A=1.000000)" :ScreenX (- SizeX 130.0) :ScreenY 28.0 :ScreenW (select (>= stars 2) 22.0 0.0) :ScreenH 22.0)
          (HUD|DrawRect :RectColor "(R=0.020000,G=0.022000,B=0.030000,A=0.550000)" :ScreenX (- SizeX 100.0) :ScreenY 28.0 :ScreenW 22.0 :ScreenH 22.0)
          (HUD|DrawRect :RectColor "(R=0.896000,G=0.879000,B=0.839000,A=1.000000)" :ScreenX (- SizeX 100.0) :ScreenY 28.0 :ScreenW (select (>= stars 3) 22.0 0.0) :ScreenH 22.0)
          (HUD|DrawRect :RectColor "(R=0.020000,G=0.022000,B=0.030000,A=0.550000)" :ScreenX (- SizeX 70.0) :ScreenY 28.0 :ScreenW 22.0 :ScreenH 22.0)
          (HUD|DrawRect :RectColor "(R=0.896000,G=0.879000,B=0.839000,A=1.000000)" :ScreenX (- SizeX 70.0) :ScreenY 28.0 :ScreenW (select (>= stars 4) 22.0 0.0) :ScreenH 22.0)
          (HUD|DrawRect :RectColor "(R=0.020000,G=0.022000,B=0.030000,A=0.550000)" :ScreenX (- SizeX 40.0) :ScreenY 28.0 :ScreenW 22.0 :ScreenH 22.0)
          (HUD|DrawRect :RectColor "(R=0.896000,G=0.879000,B=0.839000,A=1.000000)" :ScreenX (- SizeX 40.0) :ScreenY 28.0 :ScreenW (select (>= stars 5) 22.0 0.0) :ScreenH 22.0)
          ; GTA V bar under the map: health (green) on the left half, armour (blue, empty for now) on the right.
          (HUD|DrawRect :RectColor "(R=0.020000,G=0.022000,B=0.030000,A=0.800000)" :ScreenX 16.0 :ScreenY (+ top 253.0) :ScreenW 256.0 :ScreenH 9.0)
          (HUD|DrawRect :RectColor "(R=0.090000,G=0.200000,B=0.110000,A=1.000000)" :ScreenX 18.0 :ScreenY (+ top 255.0) :ScreenW 125.0 :ScreenH 5.0)
          (HUD|DrawRect :RectColor "(R=0.300000,G=0.700000,B=0.330000,A=1.000000)" :ScreenX 18.0 :ScreenY (+ top 255.0)
            :ScreenW (* 1.25 (Math|Float|Clamp(Float) (Class|BPMissions|GetHealth m) 0.0 100.0)) :ScreenH 5.0)
          (HUD|DrawRect :RectColor "(R=0.080000,G=0.140000,B=0.240000,A=1.000000)" :ScreenX 145.0 :ScreenY (+ top 255.0) :ScreenW 125.0 :ScreenH 5.0)
          ; GTA V help box, top-left: the tutorial step (BP_Missions.Help), black box, white text
          (bind help (Class|BPMissions|GetHelp m))
          (if (> (Utilities|String|Len help) 0)
            (HUD|DrawRect :RectColor "(R=0.000000,G=0.000000,B=0.000000,A=0.800000)" :ScreenX 40.0 :ScreenY 40.0 :ScreenW (+ 40.0 (* 8.6 (Utilities|String|Len help))) :ScreenH 52.0)
            (HUD|DrawText :Text help :TextColor "(R=0.896000,G=0.879000,B=0.839000,A=1.000000)" :ScreenX 60.0 :ScreenY 55.0 :Scale 1.3))
          ; subtitle bottom-centre: a message (Msg, for MsgT seconds) or else the current objective. Shadow then white.
          (bind sub (select (> (Class|BPMissions|GetMsgT m) 0.0) (Class|BPMissions|GetMsg m) (select (< idx nmiss) (Utilities|Array|Get(acopy) names idx) "")))
          (bind subx (- (* SizeX 0.5) (* 6.3 (Utilities|String|Len sub))))
          (HUD|DrawText :Text sub :TextColor "(R=0.000000,G=0.000000,B=0.000000,A=0.850000)" :ScreenX (+ subx 2.0) :ScreenY (- SizeY 88.0) :Scale 1.5)
          (HUD|DrawText :Text sub :TextColor "(R=0.896000,G=0.879000,B=0.839000,A=1.000000)" :ScreenX subx :ScreenY (- SizeY 90.0) :Scale 1.5)
          ; MISSION PASSED / WASTED / BUSTED: a dark band across the middle of the screen behind the word, like GTA V.
          (if (or (or (> (Class|BPMissions|GetWasted m) 0.0) (> (Class|BPMissions|GetBusted m) 0.0)) (> (Class|BPMissions|GetPassed m) 0.0))
            (HUD|DrawRect :RectColor "(R=0.000000,G=0.000000,B=0.000000,A=0.550000)" :ScreenX 0.0 :ScreenY (- (* SizeY 0.4) 20.0) :ScreenW SizeX :ScreenH 150.0))
          (if (> (Class|BPMissions|GetPassed m) 0.0)
            (HUD|DrawText :Text "MISSION PASSED" :TextColor "(R=0.807000,G=0.445000,B=0.010000,A=1.000000)" :ScreenX (- (* SizeX 0.5) 250.0) :ScreenY (* SizeY 0.4) :Font "/Game/VancouverVice/HUD/F_Anton.F_Anton" :Scale 1.6)
            (HUD|DrawText :Text (Class|BPMissions|GetPassedName m) :TextColor "(R=0.896000,G=0.879000,B=0.839000,A=1.000000)"
              :ScreenX (- (* SizeX 0.5) (* 6.3 (Utilities|String|Len (Class|BPMissions|GetPassedName m)))) :ScreenY (+ (* SizeY 0.4) 92.0) :Scale 1.5))
          (if (> (Class|BPMissions|GetWasted m) 0.0)
            (HUD|DrawText :Text "WASTED" :TextColor "(R=0.745000,G=0.036000,B=0.025000,A=1.000000)" :ScreenX (- (* SizeX 0.5) 170.0) :ScreenY (* SizeY 0.4) :Font "/Game/VancouverVice/HUD/F_Anton.F_Anton" :Scale 2.2))
          (if (> (Class|BPMissions|GetBusted m) 0.0)
            (HUD|DrawText :Text "BUSTED" :TextColor "(R=0.745000,G=0.036000,B=0.025000,A=1.000000)" :ScreenX (- (* SizeX 0.5) 170.0) :ScreenY (* SizeY 0.4) :Font "/Game/VancouverVice/HUD/F_Anton.F_Anton" :Scale 2.2)))))))
