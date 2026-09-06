# TrinketMenu

[![Interface](https://img.shields.io/badge/Interface-1.12.1%20%28Build%205875%29-blue.svg)](https://github.com/Fostercare5988/TrinketMenu)
[![Version](https://img.shields.io/badge/Version-3.9.0-brightgreen.svg)](https://github.com/Fostercare5988/TrinketMenu)
[![Engine](https://img.shields.io/badge/Engine-ClassicAPI%20%7C%20SuperWoW%20%7C%20NamPower%20%7C%20UnitXP%20SP3%20%7C%20DXVK-orange.svg)](https://github.com/Fostercare5988/TrinketMenu)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An ultra-responsive, zero-latency trinket management and auto-swapping suite engineered natively for the **Enhanced World of Warcraft 1.12.1 Client Engine Stack**.

---

## 1. Description

**TrinketMenu** provides an intuitive, docked or floating on-screen bar displaying your currently equipped trinkets along with a flyout drawer of all trinkets carried in your bags.

This modernized edition has been completely re-architected from the ground up for modern high-performance engines. All legacy 2006 Lua `OnUpdate` timer frames, hidden tooltip scraping hacks, and global API overwrites have been eradicated and replaced with native C++ **`C_Timer`** hardware dispatchers and non-intrusive **`hooksecurefunc`** pipelines.

---

## 2. Quick Start & Slash Commands

Toggle, dock, lock, or scale your trinket bars using the `/trinket` or `/trinketmenu` slash commands:

| Command | Description |
| :--- | :--- |
| `/trinket` or `/trinketmenu` | Toggle visibility of the main equipped trinket frame. |
| `/trinket opt` or `/trinket config` | Open the comprehensive options and auto-queue configuration window. |
| `/trinket lock` | Lock trinket frames into position, preventing accidental drag or repositioning. |
| `/trinket unlock` | Unlock trinket frames to freely drag, dock, or re-orient them. |
| `/trinket reset` | Reset all positions, scaling, and settings to defaults. |
| `/trinket scale main <0.5 - 2.0>` | Set the exact scale multiplier of the main worn trinket buttons. |
| `/trinket scale menu <0.5 - 2.0>` | Set the exact scale multiplier of the flyout trinket drawer. |

**In-Game Shortcuts:**
- **Left-Click Trinket**: Activate equipped trinket.
- **Right-Click Worn Trinket**: Toggle the flyout menu drawer.
- **Left-Click Menu Trinket**: Equip trinket into the respective slot (or queues swap if in combat).
- **Alt-Click Worn Trinket**: Toggle auto-queue for that specific slot.

---

## 3. Core Features

- **Flyout Trinket Drawer**: Automatically scans bags for all trinket items and presents them in an organized, configurable grid.
- **Intelligent Auto-Queue**: Automatically swaps trinkets when your active trinket goes on cooldown and equips passive or ready on-use trinkets.
- **Combat Delay Protection**: Trinket swaps initiated during combat or death are safely queued and executed the split second combat ends.
- **Docking Flexibility**: Attach the flyout drawer to any corner of the main frame (or keep it independently placed).
- **Audio & Visual Readiness Notifications**: Configurable alerts when trinket cooldowns expire.

---

## 4. Technical Architecture & Zero-Bloat Optimizations

- **Native Hardware Timers (`C_Timer`)**: Eradicated the legacy 2006 Lua `TrinketMenu_TimersFrame` `OnUpdate` polling loop. All delayed updates and tickers now run directly in C++ via `C_Timer.After` and `C_Timer.NewTicker`.
- **Zero Tooltip Scraping**: Eliminated `TrinketMenu_TooltipScan` and GameTooltip parsing. Action bar trinket activations are resolved via `GetActionInfo` and direct Item ID comparisons.
- **Non-Destructive Secure Hooking**: Replaced destructive global function overrides (`UseAction = ...`, `UseInventoryItem = ...`) with native `hooksecurefunc`.
- **Rule C8 Mouse Passthrough**: Applied `:EnableMouse(false)` across all 32 child cooldown frames (`TrinketMenu_TrinketXCooldown` and `TrinketMenu_MenuXCooldown`), completely preventing cooldown sweeps from intercepting player clicks.
- **Pure English Standard (Rule H2)**: 100% clean English constants, eliminating legacy multi-locale string bloat.

---

## 5. Installation & Engine Requirements

### Mandatory Prerequisites:
This addon strictly requires the Enhanced 1.12.1 Client Extension Stack:

1. [**ClassicAPI v1.14.0+**](https://github.com/brues-code/ClassicAPI) — Mandatory engine DLL.
2. [**SuperWoW v2.2+**](https://github.com/balakethelock/SuperWoW) — Mandatory engine DLL.
3. [**NamPower v4.6.3+**](https://github.com/Emyrk/nampower) — Mandatory engine DLL.
4. [**UnitXP SP3 v89+**](https://codeberg.org/konaka/UnitXP_SP3) — Mandatory engine DLL.
5. [**DXVK**](https://github.com/doitsujin/dxvk) — Vulkan frame pacing translation layer.
6. [**VanillaFixes**](https://github.com/hannesmann/vanillafixes) — Modern OS framerate uncap.

### Installation Path:
Extract or clone into your World of Warcraft directory:
```text
World of Warcraft 1.12.1/
└── Interface/
    └── AddOns/
        └── TrinketMenu/
            ├── TrinketMenu.toc
            ├── TrinketMenu.lua
            ├── TrinketMenu.xml
            ├── TrinketMenuOpt.lua
            ├── TrinketMenuOpt.xml
            ├── TrinketMenuQueue.lua
            ├── TrinketMenuQueue.xml
            └── README.md
```

---

## 6. Credits & Attribution

- **Original Author**: Gello
- **Classic Modernization & Maintenance**: [Fostercare5988](https://github.com/Fostercare5988)

---

## 7. Changelog

### Version 3.9.0
- **Engine Startup Guard Enforcement**: Upgraded engine dependency guards across all module files (`TrinketMenu.lua`, `TrinketMenuOpt.lua`, `TrinketMenuQueue.lua`) to strictly enforce `MIN_CLASSIC_API = 11400` (`v1.14.0+`) and `SUPERWOW_VERSION` (`v2.2+`).
- **Modern Lua 5.1 Syntax**: Eradicated all 25 instances of legacy `table.getn(t)` in favor of the native `#` bytecode operator.
- **Global Table Indexing**: Modernized `getglobal(...)` calls across options and queue modules to direct `_G[...]` table indexing.
- **Table Recycling**: Replaced `table.setn(list, 0)` with native C++ `table.wipe` for instant garbage-free memory clearing during profile loading and queue sorting.

### Version 3.8.0 (Modern Engine Release)
- **Engine Guard**: Added strict startup dependency check requiring ClassicAPI v1.14.0+ and SuperWoW v2.2+.
- **Hardware Timers**: Replaced Lua `OnUpdate` polling frame with native C++ `C_Timer.After` and `C_Timer.NewTicker`.
- **Secure Hooking**: Replaced global API function overrides with `hooksecurefunc("UseInventoryItem")` and `hooksecurefunc("UseAction")`.
- **Tooltip Scanning Eradication**: Removed `TrinketMenu_TooltipScan` and replaced with direct item ID resolution.
- **Rule C8 Mouse Passthrough**: Enforced `:EnableMouse(false)` on all child cooldown frames to eliminate click dead zones.
- **Rule H5 Compliance**: Added full standard Markdown documentation and cleaned `.toc` metadata.
