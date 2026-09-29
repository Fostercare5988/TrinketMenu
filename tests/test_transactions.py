"""Lua 5.1 behavioral regressions; mocks are not client/server or rendering tests.

Run: python -B tests/test_transactions.py [directory-containing-lupa]
Set TRINKETMENU_TEST_REVISION to test the same cases against a Git revision.
"""
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

if len(sys.argv)>1 and Path(sys.argv[1]).is_dir():
    sys.path.insert(0,sys.argv.pop(1))
from lupa.lua51 import LuaRuntime

ROOT=Path(__file__).resolve().parents[1]

def source(name):
    revision=os.environ.get('TRINKETMENU_TEST_REVISION')
    if revision:
        return subprocess.check_output(['git','show',revision+':'+name],cwd=ROOT,encoding='utf8')
    return (ROOT/name).read_text(encoding='utf8')

def runtime():
    lua=LuaRuntime(unpack_returned_tuples=True)
    lua.execute(r'''
      CLASSIC_API_VERSION=11515; SUPERWOW_VERSION='2.2'; getglobal=function(n) return _G[n] end
      hooks={}; calls={}; handles={}; inventory={[13]=100,[14]=200}; bags={[0]={[1]=300,[2]=400}}
      names={[100]='First',[200]='Second',[300]='Choice',[400]='Other'}; now=10
      function link(id) return id and ('|Hitem:'..id..':0:0:0|h['..names[id]..']|h') end
      function frame(name)
        local f={name=name,scale=1,x=400,y=400,visible=false,width=92,height=52,events={}}
        function f:GetName() return self.name end
        function f:SetScale(v) assert(type(v)=='number' and v>0 and v<math.huge);self.scale=v end
        function f:GetScale() return self.scale end
        f.GetEffectiveScale=f.GetScale
        function f:SetPoint(_,_,_,x,y) x=x or 0;y=y or 0;assert(type(x)=='number' and type(y)=='number');self.x=x;self.y=y end
        function f:GetLeft() return self.x end
        function f:GetTop() return self.y end
        function f:GetBottom() return self.y-self.height end
        function f:ClearAllPoints() end
        function f:Show() self.visible=true end
        function f:Hide() self.visible=false end
        function f:IsVisible() return self.visible end
        function f:SetWidth(v) self.width=v end
        function f:GetWidth() return self.width end
        function f:SetHeight(v) self.height=v end
        function f:GetHeight() return self.height end
        function f:SetTexture(v) self.texture=v end
        function f:SetText(v) self.text=v end
        function f:GetText() return self.text end
        function f:SetChecked(v) self.checked=v end
        function f:SetOwner() end
        function f:ClearLines() self.itemID=nil end
        function f:SetAction(slot) self.itemID=tooltipID end
        function f:GetItem() return names[self.itemID],link(self.itemID),self.itemID end
        function f:SetScript() end
        function f:RegisterEvent(e) self.events[e]=true end
        function f:UnregisterEvent(e) self.events[e]=nil end
        function f:EnableMouse() end
        function f:Enable() end
        function f:Disable() end
        function f:SetAlpha() end
        function f:SetTextColor() end
        function f:SetDesaturated(v) self.desaturated=v end
        function f:SetVertexColor() end
        function f:SetBackdrop() end
        function f:SetBackdropColor() end
        function f:SetBackdropBorderColor() end
        function f:GetFrameLevel() return 1 end
        function f:SetFrameLevel() end
        function f:SetNormalTexture() end
        function f:SetPushedTexture() end
        function f:GetNormalTexture() return self end
        function f:GetPushedTexture() return self end
        function f:SetTexCoord() end
        function f:SetFont() end
        function f:GetFont() return 'font',12,'' end
        function f:LockHighlight() end
        function f:UnlockHighlight() end
        function f:SetValue(v) self.value=v end
        function f:AddMessage() end
        return f
      end
      function CreateFrame(kind,name) return frame(name) end
      UIParent=frame('UIParent'); Minimap=frame('Minimap'); DEFAULT_CHAT_FRAME=frame('chat')
      GameTooltip=frame('GameTooltip'); UISpecialFrames={}; SlashCmdList={}; StaticPopupDialogs={}
      function hooksecurefunc(name,fn) hooks[name]=fn end
      C_Timer={}
      function C_Timer.NewTimer(delay,cb)
        local h={callback=cb}; function h:Cancel() self.cancelled=true end
        table.insert(handles,h);return h
      end
      C_Timer.NewTicker=C_Timer.NewTimer
      function GetTime() return now end
      function GetInventoryItemID(_,slot) return inventory[slot] end
      function GetInventoryItemLink(_,slot) return link(inventory[slot]) end
      function GetContainerItemLink(b,s) return link(bags[b] and bags[b][s]) end
      function GetItemInfo(id)
        id=tonumber(id) or tonumber(string.match(id or '', 'item:(%d+)'))
        return names[id],link(id),3,1,'type','subtype',1,'INVTYPE_TRINKET','same-icon'
      end
      function GetContainerNumSlots(b) return b==0 and 4 or 0 end
      function GetContainerItemInfo(b,s) return 'same-icon',1,bagLocked end
      C_Container={GetContainerItemID=function(b,s) return bags[b] and bags[b][s] end}
      C_Item={EquipItemByName=function(location,slot)
        assert(not cursorType);table.insert(calls,{bag=location.bagID,slot=location.slotIndex,dest=slot})
      end}
      function PickupContainerItem() table.insert(calls,{legacy=true}) end
      function PickupInventoryItem() table.insert(calls,{legacy=true}) end
      function ClearCursor() error('Unexpected cursor mutation') end
      function GetCursorInfo() return cursorType end
      function CursorHasItem() return cursorType=='item' end
      function SpellIsTargeting() return targeting end
      function IsInventoryItemLocked() return inventoryLocked end
      function UnitAffectingCombat() return combat end
      function UnitIsDeadOrGhost() return dead end
      function UnitBuff() return nil end
      function GetInventoryItemCooldown() return wornStart or 0,wornDuration or 0,1 end
      function GetContainerItemCooldown() return 0,0,1 end
      function GetInventoryItemQuality() return 3 end
      function GetInventoryItemTexture() return 'same-icon' end
      function GetActionInfo() return actionType,actionID end
      function GetActionTexture() return 'same-icon' end
      function IsEquippedAction() return true end
      function CooldownFrame_SetTimer(f,start,duration) f.start=start;f.duration=duration end
      function IsShiftKeyDown() return false end
      function IsAltKeyDown() return false end
      function GetBindingKey() end
      function GetBindingText() return '' end
      function GetItemQualityColor() return 0,0,1 end
      function PlaySound() end
      function StaticPopup_Show() end
      function ReloadUI() reloaded=true end
      cos=function(v) return math.cos(math.rad(v)) end; sin=function(v) return math.sin(math.rad(v)) end
      strlen=string.len
      ITEM_SPELL_CHARGES='%d Charges'; ITEM_SPELL_CHARGES_P1='%d Charge'
      ITEM_COOLDOWN_TIME_SEC='Cooldown: %d sec'
      ITEM_COOLDOWN_TIME_MIN='Cooldown: %d min'; ITEM_COOLDOWN_TIME_HOURS='Cooldown: %d hr'
      table.wipe=function(t) for k in pairs(t) do t[k]=nil end end
    ''')
    codes=[source(n) for n in ('TrinketMenu.lua','TrinketMenuOpt.lua','TrinketMenuQueue.lua')]
    # Explicit fixture names and methods; no permissive global/method metatable.
    names=set(re.findall(r'\bTrinketMenu_[A-Za-z0-9_]+', '\n'.join(codes)))
    for path in ROOT.glob('*.xml'):
        names.update(re.findall(r'name="(TrinketMenu_[^"]+)"',path.read_text(encoding='utf8')))
    names.update('TrinketMenu_Menu'+str(i)+suffix for i in range(1,31)
                 for suffix in ('','Icon','Cooldown','Time'))
    names.update('TrinketMenu_Trinket'+str(i)+suffix for i in (0,1)
                 for suffix in ('','Icon','Queue','Cooldown','Time','Check','HotKey'))
    names.update('TrinketMenu_Opt'+n+suffix for n in re.findall(r'\{"(\w+)","(?:ON|OFF)"',codes[1])
                 for suffix in ('','Text'))
    names.update('TrinketMenu_'+w+'Dock_'+c for w in ('Main','Menu')
                 for c in ('TOPLEFT','TOPRIGHT','BOTTOMLEFT','BOTTOMRIGHT'))
    for n in names:
        lua.globals()[n]=lua.globals().frame(n)
    for code in codes:
        # ClassicAPI accepts the original vanilla table-iteration syntax.
        code=re.sub(r'for (\w+) in ([\w.]+) do',r'for \1 in pairs(\2) do',code)
        lua.execute(code)
    lua.execute('TrinketMenu.LoadDefaults(); TrinketMenu.Initialize()')
    return lua

class TransactionTests(unittest.TestCase):
    def test_macro_shared_icon_requires_structured_item_identity(self):
        runtime().execute("actionType='macro';actionID=1;tooltipID=200;hooks.UseAction(1);assert(TrinketMenuPerOptions.ItemsUsed.Second==0 and not TrinketMenuPerOptions.ItemsUsed.First)")

    def test_unresolved_macro_does_not_inherit_prior_tooltip_item(self):
        runtime().execute("actionType='macro';tooltipID=200;hooks.UseAction(1);TrinketMenuPerOptions.ItemsUsed={};tooltipID=nil;hooks.UseAction(1);assert(next(TrinketMenuPerOptions.ItemsUsed)==nil)")

    def test_bag_action_without_id_resolves_structured_tooltip(self):
        runtime().execute("actionType='item';tooltipID=200;hooks.UseAction(1);assert(TrinketMenuPerOptions.ItemsUsed.Second==0 and not TrinketMenuPerOptions.ItemsUsed.First)")

    def test_spell_and_equipment_set_actions_do_not_count_as_item_use(self):
        runtime().execute("actionType='spell';hooks.UseAction(1);actionType='equipmentset';hooks.UseAction(1);assert(next(TrinketMenuPerOptions.ItemsUsed)==nil)")

    def test_direct_item_action_and_native_inventory_hook_still_work(self):
        runtime().execute("actionType='item';actionID=200;hooks.UseAction(1);hooks.UseInventoryItem(13);assert(TrinketMenuPerOptions.ItemsUsed.First==0 and TrinketMenuPerOptions.ItemsUsed.Second==0)")

    def test_same_name_different_id_is_not_equipment_completion(self):
        runtime().execute("names[100]='Choice';TrinketMenu.EquipTrinketByName('Choice',13,300);assert(#calls==1 and calls[1].slot==1 and calls[1].dest==13 and TrinketMenu.CombatQueue[0])")

    def test_native_exact_move_waits_for_observed_slot(self):
        runtime().execute("TrinketMenu.EquipTrinketByName('Choice',13);assert(#calls==1 and not calls[1].legacy);TrinketMenu.ProcessCombatQueue();assert(#calls==1 and TrinketMenu.CombatQueue[0]);inventory[13]=300;TrinketMenu.ProcessCombatQueue();assert(not TrinketMenu.CombatQueue[0] and not TrinketMenu.PendingSwap[0])")

    def test_combat_queue_retains_id_after_bag_changes(self):
        runtime().execute("combat=true;TrinketMenu.EquipTrinketByName('Choice',13);bags[0][1]=400;names[400]='Choice';combat=false;TrinketMenu.ProcessCombatQueue();assert(#calls==0 and not TrinketMenu.CombatQueue[0])")

    def test_equipment_set_cursor_is_preserved(self):
        runtime().execute("cursorType='equipmentset';TrinketMenu.EquipTrinketByName('Choice',13);assert(#calls==0 and TrinketMenu.CombatQueue[0])")

    def test_locks_death_and_itemrack_defer_moves(self):
        runtime().execute("dead=true;TrinketMenu.EquipTrinketByName('Choice',13);assert(#calls==0);dead=false;bagLocked=true;TrinketMenu.ProcessCombatQueue();assert(#calls==0);bagLocked=false;Rack={IsEquipmentSwapActive=function() return true end};TrinketMenu.ProcessCombatQueue();assert(#calls==0);Rack=nil;TrinketMenu.ProcessCombatQueue();assert(#calls>0)")

    def test_superseded_pending_move_does_not_complete_new_intent(self):
        runtime().execute("TrinketMenu.EquipTrinketByName('Choice',13);TrinketMenu.EquipTrinketByName('Other',13);local before=#calls;TrinketMenu.ProcessCombatQueue();assert(#calls==before);inventory[13]=300;TrinketMenu.ProcessCombatQueue();assert(TrinketMenu.CombatQueue[0]=='Other');inventory[13]=400;TrinketMenu.ProcessCombatQueue();assert(not TrinketMenu.CombatQueue[0])")

    def test_rejected_moves_have_bounded_retries(self):
        runtime().execute("TrinketMenu.EquipTrinketByName('Choice',13);for i=1,4 do now=now+3;TrinketMenu.ProcessCombatQueue() end;assert(#calls==3 and not TrinketMenu.CombatQueue[0])")

    def test_readonly_queue_query_compares_item_id(self):
        runtime().execute("combat=true;names[400]='Choice';TrinketMenu.EquipTrinketByName('Choice',13,300);assert(TrinketMenu.GetQueuedSlotForItem(link(300))==13 and not TrinketMenu.GetQueuedSlotForItem(link(400)))")

    def test_name_macro_lookup_does_not_match_name_prefix(self):
        runtime().execute("names[100]='Choice Plus';local inv,bag,slot=TrinketMenu.FindItem('Choice',1);assert(not inv and bag==0 and slot==1)")

    def test_auto_queue_revalidates_cached_bag_identity(self):
        runtime().execute("names[400]='Choice';TrinketMenu.WatchItem.Choice={bag=0,slot=2};TrinketMenuQueue.Sort[0]={'300',0};wornStart=1;wornDuration=120;combat=true;TrinketMenu.ProcessAutoQueue(0);assert(TrinketMenu.GetQueuedSlotForItem(link(300))==13);combat=false;TrinketMenu.ProcessCombatQueue();assert(#calls==1 and calls[1].slot==1)")

    def test_invalid_saved_ui_values_are_normalized_before_open(self):
        runtime().execute("TrinketMenuOptions={Columns='bad',IconPos=false,Locked='ON'};TrinketMenuPerOptions={MainScale=0,MenuScale=-2,XPos={},YPos='bad',ItemsUsed={Choice=false},MainDock={}};TrinketMenu.LoadDefaults();TrinketMenu.Initialize();TrinketMenu.OptFrame_OnShow();assert(TrinketMenu_MainFrame:GetScale()==1 and TrinketMenuOptions.Columns==4 and TrinketMenuOptions.Locked=='ON');assert(not TrinketMenuPerOptions.ItemsUsed.Choice)")

    def test_invalid_queue_roots_and_delay_do_not_break_initialization(self):
        runtime().execute("TrinketMenuQueue={Sort=false,Enabled=7,Profiles='bad',Stats={['300']={delay='bad',priority=1}}};TrinketMenu.QueueInit();assert(type(TrinketMenuQueue.Sort[0])=='table' and not TrinketMenuQueue.Stats['300'].delay and TrinketMenuQueue.Stats['300'].priority==1)")

    def test_valid_settings_survive_and_scale_rejects_zero(self):
        runtime().execute("TrinketMenuPerOptions.MainScale=.75;TrinketMenuOptions.Columns=5;TrinketMenu.LoadDefaults();assert(TrinketMenuPerOptions.MainScale==.75 and TrinketMenuOptions.Columns==5);TrinketMenu.FrameToScale=TrinketMenu_MainFrame;TrinketMenu.ScaleFrame(0);assert(TrinketMenu_MainFrame:GetScale()==1);TrinketMenu.ScaleFrame('1.5');assert(TrinketMenu_MainFrame:GetScale()==1.5)")

    def test_reset_and_cooldown_redraw(self):
        runtime().execute("TrinketMenu.OnShow();wornStart=5;wornDuration=120;TrinketMenu.UpdateWornCooldowns(1);assert(TrinketMenu_Trinket0Cooldown.start==5 and TrinketMenuPerOptions.Visible=='ON');TrinketMenu.OnHide();assert(TrinketMenuPerOptions.Visible=='OFF');TrinketMenu.ResetSettings();StaticPopupDialogs.TRINKETMENURESET.OnAccept();assert(reloaded and TrinketMenuOptions==nil and TrinketMenuPerOptions==nil and TrinketMenuQueue==nil)")

    def test_two_slot_queue_serializes_and_completes_on_inventory_events(self):
        runtime().execute("combat=true;TrinketMenu.EquipTrinketByName('Choice',13);TrinketMenu.EquipTrinketByName('Other',14);combat=false;event='PLAYER_REGEN_ENABLED';TrinketMenu.OnEvent();assert(#calls==1 and calls[1].dest==13);inventory[13]=300;event='UNIT_INVENTORY_CHANGED';arg1='player';TrinketMenu.OnEvent();assert(#calls==2 and calls[2].dest==14);inventory[14]=400;TrinketMenu.OnEvent();assert(not TrinketMenu.CombatQueue[0] and not TrinketMenu.CombatQueue[1])")

    def test_normal_flyout_and_options_open(self):
        runtime().execute("TrinketMenu.BuildMenu();TrinketMenu.OptFrame_OnShow();assert(TrinketMenu.NumberOfTrinkets==2 and TrinketMenu.BaggedTrinkets[1].id==300 and TrinketMenu_MenuFrame:IsVisible())")

    def test_malformed_saved_roots_recover_on_login(self):
        runtime().execute("TrinketMenuOptions=true;TrinketMenuPerOptions='bad';TrinketMenuQueue=1;this=TrinketMenu_MainFrame;event='PLAYER_LOGIN';TrinketMenu.OnEvent();assert(TrinketMenuOptions.Columns==4 and TrinketMenuPerOptions.MainScale==1 and type(TrinketMenuQueue.Sort[0])=='table')")

if __name__=='__main__': unittest.main(verbosity=2)
