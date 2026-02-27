import json

with open("sample-data.json") as f:
    data = json.load(f)

print("Interface Status")
print("="*80)
print(f"{'DN':<50} {'Description':<20} {'Speed':<6} {'MTU':<6}")
print("-"*50, "-"*20, "-"*6, "-"*6)

for item in data["imdata"]:
    intf = item["l1PhysIf"]["attributes"]
    dn = intf.get("dn", "")
    descr = intf.get("descr", "")
    speed = intf.get("speed", "")
    mtu = intf.get("mtu", "")
    print(f"{dn:<50} {descr:<20} {speed:<6} {mtu:<6}")