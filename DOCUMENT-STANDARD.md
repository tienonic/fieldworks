# FieldWorks documentation standard

Use this format for every maintained document in the repository.

## Required header

Every operating document begins with:

- Status: `verified`, `working`, `blocked`, `historical`, or `candidate`
- Owner: accountable person or `unassigned`
- Updated: ISO date
- Evidence: source document, message ID, order ID, datasheet, or physical inspection

## Writing rules

1. State the current answer first.
2. Separate facts, assumptions, proposals, and decisions.
3. Use one term for each object. Use `ENTS node`, `irrigation head station`, `soil monitoring station`, and `gateway` consistently.
4. Give every station and hardware item a stable ID.
5. Name the full electrical path: connector, voltage, signal type, adapter, board input, firmware conversion, and transmitted unit.
6. Use `ordered`, `received`, and `working` only with matching evidence.
7. Put unresolved choices in an `Open decisions` section with an owner and acceptance test.
8. Link to repository-relative documents. Keep machine-local paths in the private source index only.
9. Keep raw email, receipts, tax or account data, credentials, personal addresses, and secure links out of Git.
10. Keep tables narrow. Put long explanations below the table.

## Station document order

1. Purpose and lifecycle state
2. At a glance: physical package, data product, and field question
3. Included instruments and quantities
4. Expected data fields, units, and meaning
5. Connection table
6. Mermaid signal path
7. Power and enclosure
8. Procurement evidence
9. Bench acceptance tests
10. Installation gates and open decisions

Explain the physical package and its data before showing purchasing history.

## Data representation rules

- Show engineering units beside every expected measurement.
- Preserve raw diagnostic values beside converted values.
- Use `null` and a quality flag for unavailable values. Reserve zero for measured zero.
- Call valve output `valve_command` and label it as a controller command.
- Keep station ID stable. Store site alias, coordinates, and probe depths as metadata.
- Label illustrative payloads as examples.
- For an unverified model, show `no approved stream` or null fields.

## Status vocabulary

| Status | Meaning |
|---|---|
| verified | Supported by a current primary source or physical inspection |
| working | Current design or operating state with named open checks |
| blocked | Cannot proceed until a stated dependency is resolved |
| candidate | Concept awaiting approval and assignment |
| historical | Preserved context from an earlier state |
