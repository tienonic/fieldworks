# Equipment readiness

This public view separates what is physically on hand from what still needs verification or may be added later. Purchase dates, request IDs, order numbers, receipts, vendors, and costs stay out of the repository.

| Station | Current equipment state |
|---|---|
| `IH-01` | reference irrigation package needs physical inventory and a full bench test |
| `IH-02` | replication package is planned later, after `IH-01` passes |
| `SM-01` | reference soil package needs physical inventory and a four-channel bench test |
| `SM-02`–`SM-04` | replication packages are planned later, after `SM-01` passes |
| `MET-01` | ENTS board is on hand; loaned instrument models and interfaces still need verification |
| `GW-01` | gateway is planned later after the network location, backhaul, and owner are settled |

## Status meanings

- `on hand`: physically present and directly checked;
- `inventory unverified`: the design expects the part, but the physical item still needs confirmation;
- `planned later`: may be needed after the reference build passes; not treated as ordered or purchased;
- `on hold`: no hardware action until a compatibility or ownership question is resolved.

Private purchasing evidence remains outside Git. This repository records only the station effect and the next technical check.
