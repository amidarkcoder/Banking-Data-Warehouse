from generate_all import generate_all

d = generate_all()
cust = {c["customer_id"] for c in d["customers"]}
prod = {p["product_id"]  for p in d["products"]}
br   = {b["branch_id"]   for b in d["branches"]}
acc  = {a["account_id"]  for a in d["accounts"]}
A, T = d["accounts"], d["transactions"]

checks = {
    "unique branch ids":          (len(br), len(d["branches"])),
    "accounts w/ valid customer": (sum(a["customer_id"] in cust for a in A), len(A)),
    "accounts w/ valid product":  (sum(a["product_id"]  in prod for a in A), len(A)),
    "accounts w/ valid branch":   (sum(a["branch_id"]   in br   for a in A), len(A)),
    "txns w/ valid account":      (sum(t["account_id"]  in acc  for t in T), len(T)),
}

ok = True
for name, (good, total) in checks.items():
    status = "OK  " if good == total else "FAIL"
    ok &= good == total
    print(f"[{status}] {name:28} {good} / {total}")

print("\nALL LINKS VALID" if ok else "\nSOME LINKS BROKEN")