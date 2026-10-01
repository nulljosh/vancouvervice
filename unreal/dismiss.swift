// Clicks OK / Overwrite on any Unreal modal. swift unreal/dismiss.swift
import Cocoa
let apps = NSRunningApplication.runningApplications(withBundleIdentifier: "com.epicgames.UnrealEditor")
guard let app = apps.first else { print("no editor"); exit(0) }
let ax = AXUIElementCreateApplication(app.processIdentifier)
var wins: CFTypeRef?
AXUIElementCopyAttributeValue(ax, kAXWindowsAttribute as CFString, &wins)
var clicked = 0
for w in (wins as? [AXUIElement]) ?? [] {
  var title: CFTypeRef?; AXUIElementCopyAttributeValue(w, kAXTitleAttribute as CFString, &title)
  let t = (title as? String) ?? ""
  guard t == "Message" || t.hasPrefix("Overwrite") || t.hasPrefix("Memory") else { continue }
  var kids: CFTypeRef?; AXUIElementCopyAttributeValue(w, kAXChildrenAttribute as CFString, &kids)
  func walk(_ e: AXUIElement) {
    var role: CFTypeRef?; AXUIElementCopyAttributeValue(e, kAXRoleAttribute as CFString, &role)
    var name: CFTypeRef?; AXUIElementCopyAttributeValue(e, kAXTitleAttribute as CFString, &name)
    if (role as? String) == "AXButton", let n = name as? String, ["OK","Overwrite","Dismiss","Yes"].contains(n) {
      AXUIElementPerformAction(e, kAXPressAction as CFString); clicked += 1; return }
    var c: CFTypeRef?; AXUIElementCopyAttributeValue(e, kAXChildrenAttribute as CFString, &c)
    for k in (c as? [AXUIElement]) ?? [] { walk(k) }
  }
  for k in (kids as? [AXUIElement]) ?? [] { walk(k) }
}
print("dismissed \(clicked)")
