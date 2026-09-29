# TrinketMenu source and integration review

## Task and starting evidence

Task: architecture discovery, correctness audit, bounded bug fixes, integration
review and publication. Starting local/origin/remote head:
`b45388377ef0ff52f046c4b86ab524acad65b09b`; working tree clean. Reuse its timer
ownership fix and four existing regressions. User authorizes commit and push,
without tags/releases. Scope: item-use identity, trinket transactions and invalid
saved UI/queue values. Preserve auto-queue order, keep/delay/priority behavior,
manual cancellation, combat/death deferral and independent addon installation.

## Architecture

- TOC: Interface 11200; main Lua/XML, options Lua/XML, queue Lua/XML (six entries).
  Root `Bindings.xml` is client-managed. No load-order changes.
- Main module owns equipped slots 13/14, 30 flyout buttons, rarity borders,
  cooldown/tooltip display, drag/docking/scale, runtime intent and swap attempts.
  Options owns minimap/settings UI. Queue owns sort lists, profiles and selection.
- Account SavedVariables: `TrinketMenuOptions`. Per-character:
  `TrinketMenuPerOptions` and `TrinketMenuQueue`. Queue IDs, pending requests,
  handles and retry counters are runtime-only. Existing sort lists use base IDs;
  this change does not introduce per-instance/GUID selection or migrate profiles.
- Login initializes UI and timers. Inventory/lock/combat/resurrection events
  drive equipment reconciliation. BAG_UPDATE coalesces bag-watch updates;
  cooldown and binding events redraw their owned widgets. One-second cooldown
  sampling also evaluates auto-queue. Hover, docking and scaling have scoped
  tickers; minimap drag uses a zero-delay ticker only while dragging.
- Native cooldown widgets render sweeps; Lua submits cooldown values on existing
  events. Smooth drag/render behavior is not rewritten. No benchmark or blanket
  allocation claim is made.
- Published requirements remain ClassicAPI 1.15.15+ and SuperWoW 2.2+.
  New consumption: structured tooltip `GetItem`, `GetInventoryItemID`,
  `GetCursorInfo` and exact-location `C_Item.EquipItemByName`. Existing
  `C_Container.GetContainerItemID`, cancellable timers and secure hooks remain.
  No NamPower, UnitXP or DXVK dependency is introduced.
- Optional integration: read-only `Rack.IsEquipmentSwapActive()` and
  `TrinketMenu.GetQueuedSlotForItem(link)` for Bagnon. No foreign mutable queue.

## Ranked findings and bounded changes

Locations below refer to the reviewed result; starting defects are in the same
named functions at the starting commit. No P0 was found.

1. **P1 [SOURCE-VERIFIED] Name-based equipment identity.**
   `TrinketMenu.lua:430,1072,1081,1107` and
   `TrinketMenuQueue.lua:342`: different IDs with the same displayed name could
   be treated as the requested item, including false completion when the other
   ID was already worn. Reproduction: select bag ID 300 named Choice while ID
   100 named Choice is equipped, or replace the source with same-name ID 400
   during combat. The old queue completed early or selected the replacement.
   Retain the selected ID at request time; use it for search, pending completion,
   supersession and the read-only tooltip query. Auto-queue revalidates its
   name-indexed watch location against the actual candidate ID. Exact-name
   lookup replaces equipped-link substring matching for name-only macro inputs.

2. **P2 [SOURCE-VERIFIED] Ambiguous action icons.**
   `TrinketMenu.lua:902`: a macro/bag action sharing slot 13's icon could mark
   slot 13 used even when the structured item was slot 14, or no item at all.
   Direct IDs and private-tooltip `GetItem()` now select the actual equipped ID.
   The tooltip is cleared for each use; unknown item, spell and equipment-set
   actions do not infer item use. Direct inventory-use hooks remain unchanged.
   A hook observes a use attempt, not proof that the server accepted it.

3. **P2 [SOURCE-VERIFIED] Non-item cursor and pickup ownership.**
   `TrinketMenu.lua:1107`: the old guard covered only held items and targeting;
   an equipment-set/macro/spell cursor could reach two unconditional pickup
   calls. A refused first pickup could still be followed by the inventory
   pickup. Use the verified explicit-slot native swap, guarded by structured
   cursor state, the existing native item-cursor check, locks, combat/death and
   ItemRack. Keep the existing pending deadline, bounded retry and observed-ID
   completion. A native call returning is not success evidence.

4. **P2 [SOURCE-VERIFIED] Invalid persisted values reach UI/arithmetic.**
   `TrinketMenu.lua:16,849` and `TrinketMenuQueue.lua:13`: a zero/negative scale,
   nonnumeric coordinate/column/icon angle, malformed ItemsUsed counter, queue
   root or delay could break startup or later sampling. Normalize these at load
   and reject nonpositive/nonfinite scale requests. Preserve valid values and
   unknown fields. This is scoped validation, not arbitrary SavedVariables
   repair; malformed individual profile/list entries are not silently rebuilt.

## Authoritative API evidence

ClassicAPI 1.15.15, commit `71805db62f1e8a154477033dc1f50960c535af8b`:

- [Action descriptor source](https://github.com/brues-code/ClassicAPI/blob/71805db62f1e8a154477033dc1f50960c535af8b/src/action/Info.cpp):
  `item,id`, unresolved `item,nil`, `macro,index`, `spell` and `equipmentset`.
  No `itemInventorySlot` descriptor exists at this pinned version.
- [Tooltip source](https://github.com/brues-code/ClassicAPI/blob/71805db62f1e8a154477033dc1f50960c535af8b/src/item/Tooltip.cpp)
  and [item context](https://github.com/brues-code/ClassicAPI/blob/71805db62f1e8a154477033dc1f50960c535af8b/src/item/TooltipItem.cpp):
  `GetItem()` returns name, link, item ID; item context is distinguished from
  spell/unit context. No rendered text or icon comparison is needed here.
- [Equipment source](https://github.com/brues-code/ClassicAPI/blob/71805db62f1e8a154477033dc1f50960c535af8b/src/item/Equipment.cpp):
  exact bag location plus explicit destination uses the native swap primitive;
  it clears the cursor first, so the caller must guard foreign cursor state.
  It returns nothing and may refuse a move.
- [Timer source](https://github.com/brues-code/ClassicAPI/blob/71805db62f1e8a154477033dc1f50960c535af8b/src/time/Timer.cpp)
  and [API reference](https://github.com/brues-code/ClassicAPI/blob/71805db62f1e8a154477033dc1f50960c535af8b/docs/API.md):
  cancellable timer handles, container/inventory IDs and structured cursor data.
  These are available at the current published floor; no floor increase.

The five cached source files above were matched to the pinned Git tree by blob
SHA-1: action `e856b780`, equipment `1599cd73`, tooltip `fa8a05d5`, tooltip item
`acc70ace`, timer `f7a4ccbd`. API return semantics were read from source, not
inferred from Retail names. Correct native frame, cooldown and event primitives
remain in place.

## Validation and integration disposition

- 22 new full-module Lua 5.1 mock cases plus four existing timer cases: **26 pass**.
  The harness executes initialization/options paths with explicit frame methods;
  it adapts vanilla table-iteration syntax for the Lua 5.1 test VM.
  Against the starting revision, 17 new cases fail behavior assertions or the
  original malformed-value errors; five unchanged-behavior controls pass.
- Cases cover exact ID/name collisions, cached bag changes, cursor/lock/death/
  ItemRack guards, retries, supersession, two-slot inventory-event sequencing,
  action descriptors, malformed old values, normal flyout/options opening,
  reset, positive scaling and cooldown redraw arguments.
- Lua syntax: three files. TOC/XML graph: six loaded files, no orphan runtime
  Lua. Bindings remain outside TOC by native client convention.
- Strict VanillaForge linter: zero errors/advisories. Full runtime/test/docs diff
  reviewed; `git diff --check` passes. Scratch content excluded.
- Integration review: correctness, ownership, API/dependency consistency,
  persistence scope, UI/load graph and repository scope pass source/mocked
  checks. Ready for publication with the runtime acceptance boundary below.
  No in-game results are claimed as `[EMPIRICALLY VERIFIED]`.

## In-game acceptance still required

1. Start normally, open options and both flyouts; drag, dock, rotate, lock and
   scale both windows. Test native cooldown redraws, borders and click-through.
   Back up SavedVariables before testing malformed scales/coordinates and reset.
2. Use direct item actions, bag-instance actions, slot-use macros and macros
   with shared icons. A spell/equipment-set action must not mark another trinket
   used. `[UNVERIFIED - TEST FIRST]`: macro tooltip identity can depend on native
   macro behavior; unresolved actions intentionally do not guess from icons.
3. Queue both slots during combat/death, leave combat/resurrect, verify sequential
   exact-ID completion. Move/remove the source during combat. If available, test
   distinct custom IDs with the same name; no substitution is acceptable.
4. Select a newer request while an old swap is pending, cancel by selecting the
   same item again, and exercise locked items, server refusal and slow updates.
   **P2 [UNVERIFIED - TEST FIRST]**: the existing two-second watchdog may interact
   with responses delayed beyond its deadline; mocks do not establish latency.
5. Repeat with active ItemRack swaps and held item/spell/macro/equipment-set
   cursors. Validate Bagnon queue indicators against the chosen item ID.
6. Verify existing priority, delay, keep-equipped, stop-on-swap, profile order,
   Feign Death and ready notification behavior. Same-ID copies intentionally
   remain interchangeable; name-indexed cooldown watches are retained. No
   supported custom-content aura identity claim is made from the Feign Death
   icon scan (**P3 [UNVERIFIED - TEST FIRST]**); investigate in client if it
   misclassifies death on a deployment.

## Retrospective

The earlier timer audit remained valid. Checking actual descriptor and native
equipment source prevented relying on an unimplemented slot descriptor or
mistaking native dispatch for completion. Full initialization tests exposed
fixture gaps before acceptance; no production fix was inferred from those mock
errors. The main reusable principles (exact identity, deferred ownership,
source-pinned APIs and runtime evidence boundaries) are already in VanillaForge.
No framework change is proposed from this addon review.
