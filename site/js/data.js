export const block = 260, road = 80;
export const vanMap = ["WWRWWWWWWWWWWWWW","WPRPWWWWWWWWWWWW","PPPPPWWWWCWWWWWW","PPPPBBBBBBHBGWWW","WPPBBBBBBBBBBBBW","WYBBBBBBABBBBBBB","WWYBBBBBBBBBBBBB","WWWWBBBBBBBSOBBB","WWWWWWBBBBBBBBBB","WWWWWRWIRWWWWWEW","BBYYBBBBBBBBBBBB","BBBBBBBBBBBBBBBB","WWWWWRWWWWWWWWWW","WWWWWRWWWWWWWWWW","WWWBBBBBWWWWWWWW","WWWBBLBBWWWWWWWW","WWWBBBBBWWWWWWWW","WWWWWWWWWWWWWWWW"];
export const cols = 16, rows = vanMap.length, W = cols * block, H = rows * block;
export const aves = ["Burrard Inlet","Coal Harbour","Canada Place Way","W Hastings","W Pender","W Georgia","Robson","Smithe","Pacific","False Creek","W 2nd","W 4th"];
export const streets = ["Chilco","Denman","Bidwell","Nicola","Bute","Thurlow","Burrard","Hornby","Granville","Seymour","Richards","Homer","Cambie","Beatty","Quebec","Main"];
export const NAMES = { C: "Canada Place", S: "BC Place", E: "Science World", L: "BC Legislature", H: "Harbour Centre", G: "Gastown Steam Clock", A: "Vancouver Art Gallery", O: "Rogers Arena", I: "Granville Island" };
export const HOODS = {
  dtes: { name: "Downtown Eastside", shirts: [0x5a5048, 0x3d3d3d, 0x6b5b4a, 0x4a4f3a], cart: .35, slow: .6, lines: ["Got a smoke?", "Shelter's full again tonight", "Stay safe out here, alright", "Housing first, that's all I'm saying", "Spare a toonie?", "I used to work the docks, you know"] },
  gastown: { name: "Gastown", shirts: [0xc0392b, 0xe0a526, 0x2a6fdb, 0xeeeeee], camera: .5, lines: ["Where's the steam clock?", "Is this where they film everything?", "Cobblestones, so charming", "Twelve dollar coffee, wow"] },
  westend: { name: "West End / Coal Harbour", shirts: [0x1f2a44, 0x111111, 0xdddddd, 0x5a1f2a], dog: .35, lines: ["My Tesla's double parked", "The condo went up again, love it", "Seawall run at six, then the yacht club", "Have you tried the new omakase?"] },
  yaletown: { name: "Yaletown", shirts: [0x222222, 0x6b7f8f, 0xeeeeee, 0x2e5e4e], lines: ["Brunch was forty bucks each, worth it", "Startup's pivoting again", "Did you see the Canucks game?"] },
  kits: { name: "Kitsilano", shirts: [0x8fb8a8, 0xe8d8c8, 0x1c1c1c, 0xd98b8b], dog: .25, lines: ["Namaste", "Just did the Grouse Grind", "Kits Beach later?", "Oat milk, obviously"] },
  victoria: { name: "Victoria", shirts: [0x7a6a8a, 0x8a9a7a, 0xc8b89a, 0x2a4a6a], lines: ["Tea at the Empress?", "Ferry was late again", "Lovely day for the harbour", "Are you from the mainland, dear?"] },
  downtown: { name: "Downtown", shirts: [0x8b5a2b, 0xc0392b, 0x2a6fdb, 0x222222, 0x2e9e4f, 0xe0a526], lines: [] },
};
export const kinds = [[40, 20, 420], [40, 20, 400], [80, 24, 260], [38, 18, 600]];
export const colors = [0xd33, 0xeec21b, 0xe67e22, 0x2e9e4f, 0xeeeeee, 0xe86aa6];
export const PERKS = {
  Joshua: { blurb: "Gastown hustler: +50% mission cash, cops lose interest twice as fast", cash: 1.5, cool: 2 },
  Ben: { blurb: "Kits athlete: runs 40% faster, jumps higher, drops people in two punches", run: 1.4, jump: 1.35, fists: 2 },
  Alexandre: { blurb: "Victoria fixer: steady aim (+50% range), faster cars, shrugs off 30% of damage", aim: 1.5, drive: 1.15, armor: .7 },
};
export const HERO_LOOK = { Joshua: 0xe8b21a, Ben: 0x2a5fb8, Alexandre: 0x1c1c1f };
export const STARS = [1, 20, 60, 140, 260];
export const WEAPONS = [{ name: "Fists" }, { name: "Pistol", dmg: 1, range: 600, rate: 250, max: 90, mag: 12, reload: 1.2 }, { name: "Shotgun", dmg: 3, range: 220, rate: 800, pellets: 3, max: 30, mag: 6, reload: 2.2 }, { name: "SMG", dmg: 1, range: 450, rate: 90, max: 240, mag: 30, reload: 1.6 }, { name: "Revolver", dmg: 2, range: 650, rate: 600, max: 36, mag: 6, reload: 2 }, { name: "Assault rifle", dmg: 1, range: 750, rate: 110, max: 300, mag: 30, reload: 1.8 }, { name: "Sniper rifle", dmg: 5, range: 1500, rate: 1300, max: 20, mag: 5, reload: 2.6 }];
export const ACH = { first: "First Blood", thief: "Grand Theft Auto", five: "Five Star Menace", copkill: "Cop Killer", island: "Island Hopper", tourist: "Tourist: every landmark", courier: "Courier: 5 deliveries", taxi: "Night Shift: first fare", ghost: "Ghost: lost a 3 star chase", champ: "Level 5" };
export const MISSIONS = ["deliver", "taxi", "evade"];
export const STATIONS = [{ name: "Off" }, { name: "Kits Beach FM", bpm: 104, root: 55, beat: [1, 0, 0, 0, 1, 0, 0, 0], hat: true }, { name: "Hastings Hardcore", bpm: 150, root: 41, beat: [1, 0, 1, 0, 1, 0, 1, 1], hat: true }, { name: "CBC Rain Radio", bpm: 70, root: 48, beat: [1, 0, 0, 0, 0, 0, 0, 0], pad: true }];
export const WX = { 0: "Clear", 1: "Mostly clear", 2: "Partly cloudy", 3: "Overcast", 45: "Fog", 48: "Fog", 51: "Drizzle", 53: "Drizzle", 55: "Drizzle", 61: "Rain", 63: "Rain", 65: "Heavy rain", 71: "Snow", 73: "Snow", 75: "Heavy snow", 80: "Showers", 81: "Showers", 82: "Downpour", 95: "Thunderstorm", 96: "Thunderstorm", 99: "Thunderstorm" };
export const LINES = ["Sorry!", "Canucks are gonna choke again, eh", "Rent's thirty-four hundred for a one bedroom, man", "You been to Granville Island? The market's sick", "It's gonna rain. It's always gonna rain", "Spare some change for the SkyTrain?", "Nice day for the seawall", "Have you seen my dog? Off leash at English Bay", "Go Whitecaps!", "Where's the nearest Tim's?", "Bro, the Expo line is down again", "You look like you could use a JapaDog", "Hey, you're Brian's kid, aren't you? Still owe him that hard drive", "Your mom's called me twice today looking for you, Joshua", "Sarah again? Smartest one in that family by a mile"];
export const BUMPS = ["Watch it, bud", "Hey! Eyes up", "Seriously?"];
export const FIGHTS = ["You got a problem?", "Wanna go?", "Say that again"];
export const STORY = [
  // Act one: forty grand by Friday (Joshua, downtown)
  { title: "Joshua: The Georgia Store", kind: "heist", text: "Dmitri wants something worth a grand by tonight. Six Mac minis on the tables at the store on Georgia, and nobody's looking yet. Grab them and run for the door. Two guys in blue shirts won't let it go and one will call the cops: jack a car and lose them", pay: 300 },
  { title: "Joshua: Pawn the Mac minis", kind: "deliver", at: "pawn", chain: true, text: "Six Mac minis, no receipts, no questions you want asked. Drive them to Granville Pawn (green on the map), then walk in and take the cash. The guy behind the counter pays half what you hoped and asks how your dad's doing", pay: 400 },
  { title: "Joshua: Dmitri", kind: "meet", at: { x: 12 * block + 40, y: 3 * block + 170 }, text: "Dmitri runs a co-working space in Gastown that has never had a single co-worker. Go see him", pay: 0,
    scene: "Dmitri is in a Patagonia vest, standing desk, kombucha on tap. He counts the pawn money twice.\n\nDMITRI  This is interest, Joshua. You owe me forty grand by Friday.\nJOSHUA  For what?\nDMITRI  For the thing you did. Here's how you start paying: Colin at the McDonald's on Granville runs my cash through his night deposit. Bring me the bag.\n\nHe goes back to his laptop. The meeting is over." },
  { title: "Joshua: Colin's Night Deposit", kind: "rob", text: "Colin manages the McDonald's on Granville and brags about the night deposit to anyone who'll listen. It isn't burger money, it's Dmitri's. Walk in with a gun out, take the bag, and lose the cops", pay: 500 },
  { title: "Joshua: Club Velvet", kind: "club", text: "Your girl's at Club Velvet on Granville tonight. So, it turns out, is Colin, wearing a watch he could not afford last week. Go find her", pay: 600 },
  { title: "Joshua: Heat on Hastings", kind: "evade", text: "Colin gave the cops your name. Dmitri says he'd rather they chase you than his money: pull three stars down Hastings, then shake them", pay: 600 },
  { title: "Joshua: Night Shift", kind: "taxi", text: "Lie low. Cover your buddy's cab for the night. First fare is a woman who won't stop talking about her son who never calls. It's Mom. Don't turn around", pay: 350 },
  // Act two: the crew (Ben in Kits, Alexandre in Victoria)
  { title: "Ben: Kits Beach", kind: "taxi", text: "Joshua needs a boat and can't face his dad, so Ben asks. Drive Brian down to Kits Beach to look at the boat. He'll say yes on one condition: Joshua brings back the hard drive he borrowed two years ago", pay: 700 },
  { title: "Ben: Springs", kind: "evade", text: "Ben fixed a garage door spring in Kerrisdale and the guy won't pay the bill. Ben got his money the hard way. Now get out in the work truck and lose the cops", pay: 600 },
  { title: "Ben: The Lululemon Sale", kind: "deliver", text: "Rich people stampeding for Lululemon on 4th Avenue. The stock is worthless. The delivery van is the prize: grab it in the chaos and bring it to the beacon", pay: 750 },
  { title: "Ben: The Boys", kind: "deliver", text: "Joshua, Alex and the boys are waiting at the Kits lot. Bring a car worth racing. Maddie said be home for dinner", pay: 700 },
  { title: "Alexandre: Island Business", kind: "hit", text: "Dmitri's courier in Victoria knows Joshua's name and is selling it on the docks. Alexandre has a desk job, a plan, and now a problem. Find the marked man", pay: 500 },
  { title: "Alexandre: The Ferry", kind: "taxi", text: "That's Dmitri's truck on the Swartz Bay ferry. Follow him off the boat and find out where he really goes", pay: 850 },
  { title: "Alexandre: Government Street", kind: "evade", text: "Dmitri launders through condo presales. Saturday the cash leaves a sales centre in Coal Harbour in an armoured truck. Get close enough to scope it, then lose whoever notices", pay: 950 },
  { title: "Joshua: Colin's Place", kind: "meet", at: { x: 10 * block + 40, y: 8 * block + 170 }, text: "You followed Colin home to Yaletown. Go get your girl back", pay: 0,
    scene: "Colin answers the door in a bathrobe. She isn't there; she left him at brunch. But on his desk is a silver hard drive with a strip of masking tape on it that says BRIAN.\n\nCOLIN  That? Bought it at Granville Pawn for twenty bucks. Four thousand photos of a boat.\nJOSHUA  You know whose that is?\nCOLIN  Some guy named Brian, I guess.\n\nYou take it. Colin calls Dmitri before you reach the elevator." },
  // Act three: the score
  { title: "All three: The Plan", kind: "meet", at: { x: 1 * block + 230, y: 11 * block + 40 }, text: "Dad's garage. All three of you in one room for the first time", pay: 0,
    scene: "Joshua, Ben and Alexandre around Brian's workbench. Mom brings sandwiches and pretends not to hear anything.\n\nALEXANDRE  Saturday the armoured truck leaves the presale centre. We take it at the light on Georgia, swap to the boat under the Burrard Bridge, and come out in North Van.\nBEN  Brian's boat.\nBRIAN  My boat. Where's my hard drive?\nJOSHUA  After.\n\nYou need one more person. The best hacker in the city is your sister, and she said no." },
  { title: "Joshua: Sarah's Interview", kind: "taxi", text: "Sarah will do the job on one condition: drive her to her job interview in Burnaby, on time, no cops. Pick her up", pay: 600 },
  { title: "All three: The Score", kind: "deliver", text: "Saturday. Sarah has the lights on Georgia. The armoured truck rolls out of the presale centre. Take it and bring it to the beacon. Mom is calling. Do not pick up", pay: 2500 },
  { title: "Joshua: The Getaway", kind: "evade", text: "Every cop in the city is on you. Dad's boat is waiting under the Burrard Bridge. Lose them and get to the water. He will ask about the hard drive", pay: 3000 },
  { title: "Joshua: Waterfront", kind: "deliver", text: "Dmitri is waiting at the Waterfront for his forty grand. Bring him the car with the money, or drive straight past him to family dinner", pay: 5000 },
];
// Granville Pawn on Granville St between W Georgia and Robson; prices per item
export const PAWN = { x: 8 * block + 40, y: 6 * block + 170, name: "Granville Pawn" };
export const LOOT = { mac: ["Mac mini", 150], book: ["MacBook", 300], phone: ["phone", 40] };
export const SKIN = [0xf1c9a5, 0xd9a680, 0xb67b53, 0x8d5a3b, 0x5c3a24];
export const HAIR = [0x1c140f, 0x3b2616, 0x6b4a2b, 0xb58a4c, 0x8f8f8f];
export const PANTS = [0x2b3440, 0x1f1f24, 0x4a3b2a, 0x3b4f6b, 0x5a5a5a];
export const HERO_BODY = { Joshua: "hero", Ben: "male_adult_05", Alexandre: "male_adult_09" };
