# TrinketMenu

A trinket management, flyout drawer, and auto-swapping add-on for World of Warcraft 1.12.1.

## Features

- **Equipped Trinket HUD**: Clean on-screen buttons displaying your currently equipped trinkets, their cooldown spirals, and readiness states.
- **Flyout Trinket Drawer**: Hover or right-click to open a configurable grid drawer displaying all trinkets carried in your bags for fast one-click swapping.
- **Intelligent Auto-Queue**: Automatically swaps trinkets according to a customizable priority list when an active trinket is on cooldown.
- **Combat Delay & Queueing**: Swaps triggered during combat or death are queued and execute automatically as soon as combat ends.
- **Flexible Docking & Scaling**: Dock the drawer to any side of the main bar or position it independently, with granular scale controls.
- **Suite Synergy**: Cooperates seamlessly with ItemRack to prevent simultaneous inventory moves, and reflects queued trinkets on Bagnon item tooltips.

## Requirements

- **World of Warcraft 1.12.1** (Build 5875)
- [ClassicAPI v1.15.15+](https://github.com/brues-code/ClassicAPI) (`ClassicAPI.dll`)
- [SuperWoW v2.2+](https://github.com/balakethelock/SuperWoW) (`SuperWoWhook.dll` / `SuperWoWlauncher.exe`)

> Note: Completely restart the game client after installing or updating DLLs. `/reload` cannot reload DLLs.

## Installation

1. Copy or clone this repository into your WoW add-on directory:
   ```text
   World of Warcraft/Interface/AddOns/TrinketMenu/
   ```
2. Verify that `TrinketMenu.toc` is located directly at `Interface/AddOns/TrinketMenu/TrinketMenu.toc`.
3. Launch WoW using the SuperWoW launcher.
4. Ensure TrinketMenu is checked on the character selection AddOn screen.

## Useful Commands & Shortcuts

| Command | Description |
| :--- | :--- |
| `/trinket` or `/trinketmenu` | Toggle visibility of the main trinket buttons |
| `/trinket opt` | Open options and auto-queue priority window |
| `/trinket lock` / `/trinket unlock` | Lock or unlock frame dragging |
| `/trinket reset` | Reset frame positions, scaling, and settings |
| `/trinket scale main <0.5 - 2.0>` | Set scale of the equipped trinket buttons |
| `/trinket scale menu <0.5 - 2.0>` | Set scale of the flyout drawer |

| Shortcut | Action |
| :--- | :--- |
| `Left-Click` Worn Trinket | Use / activate equipped trinket |
| `Right-Click` Worn Trinket | Toggle flyout trinket drawer |
| `Left-Click` Drawer Trinket | Equip trinket (or queue if in combat) |
| `Alt-Click` Worn Trinket | Toggle Auto-Queue for that slot |

## Limitations & Notes

- **Combat Restrictions**: Trinkets cannot be swapped while in combat. Requested swaps are placed into a pending queue and completed automatically upon dropping combat.
- **Identical Items**: Multiple copies of the same trinket are treated as interchangeable instances of that item ID.
- **ItemRack Coordination**: When ItemRack is performing a set swap, TrinketMenu delays its own equip moves until ItemRack finishes to prevent inventory lockups.

---

For detailed priority list setup, bar docking, and advanced settings, see the [User Guide](docs/USER_GUIDE.md). Technical architecture notes are documented in [INTEGRATION_REVIEW_2026-09-29.md](INTEGRATION_REVIEW_2026-09-29.md).

## License & Credits

Original author: Gello. Maintained by [Fostercare5988](https://github.com/Fostercare5988). Licensed under the MIT License.
