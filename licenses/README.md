# SPD licence list

Edit `spd.json` on GitHub (pencil icon -> Commit changes). SPD checks it at start-up and every 30 minutes.

| field | meaning |
|---|---|
| `default` | `"allow"` = PCs not in the list can use SPD, `"block"` = only PCs in the list with `"allow"` |
| `id` | Machine ID shown in SPD (log line at start-up, or the lock screen) e.g. `SPD-1A2B-3C4D-5E6F` |
| `name` | any name for you (visible to anyone - use a nickname, not personal data) |
| `status` | `"allow"` or `"block"` |
| `expires` | optional `"2026-12-31"` - after this date the PC is locked; `""` = never |

Offline PCs keep working for 7 days after their last successful check, then lock until they are online again.

Example:
```json
{
  "app": "SPD",
  "message": "Contact Praveen Kumar B to get access.",
  "default": "block",
  "machines": [
    { "id": "SPD-1A2B-3C4D-5E6F", "name": "Praveen laptop", "status": "allow", "expires": "" },
    { "id": "SPD-9F8E-7D6C-5B4A", "name": "Office PC 2",    "status": "allow", "expires": "2026-12-31" },
    { "id": "SPD-1111-2222-3333", "name": "Old trainee PC", "status": "block", "expires": "" }
  ]
}
```
