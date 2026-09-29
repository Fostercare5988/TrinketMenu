# TrinketMenu User Guide

Detailed configuration, auto-queue management, and bar controls for **TrinketMenu**.

---

## 1. Interface Controls & Sizing

### The Main Bar
- **Visibility**: Toggle the equipped trinket buttons with `/trinket` or `/trinketmenu`.
- **Repositioning**: Type `/trinket unlock` to show drag handles. Drag the bar to your preferred position, then type `/trinket lock` to fix it in place.
- **Scaling**: Adjust the size of the buttons at any time:
  - `/trinket scale main <0.5 - 2.0>` adjusts the main equipped trinket buttons.
  - `/trinket scale menu <0.5 - 2.0>` adjusts the flyout menu drawer.
- **Docking**: In the options menu (`/trinket opt`), configure whether the flyout drawer docks to the top, bottom, left, or right of the main bar, or floats independently.

### Mouse Interactions
- **Left-Click Worn Trinket**: Use / activate the equipped trinket.
- **Right-Click Worn Trinket**: Open or close the flyout trinket drawer.
- **Left-Click Flyout Trinket**: Equip that trinket into the corresponding slot (or queue the swap if currently in combat).
- **Alt-Click Worn Trinket**: Toggle the Auto-Queue feature on or off for that slot.

---

## 2. Intelligent Auto-Queue

TrinketMenu can automatically cycle trinkets so you always have ready on-use effects or strong passive bonuses active:

### Setting Up Auto-Queue
1. Type `/trinket opt` and navigate to the **Trinket Priority** tab.
2. Arrange your trinkets in priority order for each slot (Top and Bottom trinket slots can have separate lists).
3. Activate auto-queue by checking the box in options or `Alt-Clicking` the worn trinket button.
4. When an equipped on-use trinket is activated and goes on cooldown, TrinketMenu automatically queues and equips the next highest-priority ready trinket once combat ends.

---

## 3. Combat Delays & Swap Safety

- **In-Combat Restrictions**: World of Warcraft prevents swapping trinkets while engaged in combat or while dead.
- **Automatic Queueing**: Swaps triggered manually or by Auto-Queue during combat enter a staging queue. A small overlay indicates a pending swap. Once combat ends or you revive, TrinketMenu executes the swap automatically.
- **ItemRack Coordination**: When ItemRack is performing a multi-piece equipment set swap, TrinketMenu yields briefly to ensure equipment moves do not collide or lock inventory bags.
- **Duplicate Items**: If you carry multiple copies of the exact same trinket, TrinketMenu treats them as interchangeable copies of the same item ID.
