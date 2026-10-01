import CoreGraphics
let l = CGWindowListCopyWindowInfo([.optionAll], kCGNullWindowID) as! [[String: Any]]
for w in l where (w["kCGWindowOwnerName"] as? String ?? "").contains("Unreal") {
  let b = w["kCGWindowBounds"] as! [String: Any]
  print(w["kCGWindowNumber"]!, w["kCGWindowName"] ?? "", b["Width"]!, b["Height"]!, w["kCGWindowLayer"]!)
}
