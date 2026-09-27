"""Native timer cancellation/ownership regressions (mock Lua, not in-game).
Run: python -B tests/test_timers.py [directory-containing-lupa]
"""
from pathlib import Path
import sys
import unittest
if len(sys.argv)>1: sys.path.insert(0,sys.argv.pop(1))
from lupa.lua51 import LuaRuntime
ROOT=Path(__file__).resolve().parents[1]
SOURCE=(ROOT/'TrinketMenu.lua').read_text(encoding='utf-8')
CODE=SOURCE[SOURCE.index('function TrinketMenu.InitTimers()'):SOURCE.index('function TrinketMenu.TimersFrame_OnUpdate()')]
def runtime():
 lua=LuaRuntime(unpack_returned_tuples=True)
 lua.execute('''TrinketMenu={}; C_Timer={}; handles={}; fired=0
 function C_Timer.NewTimer(delay,cb)
  local h={callback=cb,cancelled=false,delay=delay}
  function h:Cancel() self.cancelled=true end
  table.insert(handles,h); return h
 end
 C_Timer.NewTicker=C_Timer.NewTimer
 function C_Timer.After() error("Non-cancellable After is not valid here") end
 ''')
 lua.execute(CODE); lua.execute('TrinketMenu.InitTimers()')
 return lua
class TimerTests(unittest.TestCase):
 def test_one_shot_can_be_cancelled(self):
  runtime().execute('''TrinketMenu.CreateTimer("t",function() fired=fired+1 end,.2)
  TrinketMenu.StartTimer("t");assert(TrinketMenu.IsTimerActive("t"))
  TrinketMenu.StopTimer("t");assert(handles[1].cancelled)
  handles[1].callback();assert(fired==0 and not TrinketMenu.IsTimerActive("t"))''')
 def test_replaced_timer_cannot_clear_or_fire_new_request(self):
  runtime().execute('''TrinketMenu.CreateTimer("t",function() fired=fired+1 end,.2)
  TrinketMenu.StartTimer("t");TrinketMenu.StartTimer("t")
  assert(handles[1].cancelled);handles[1].callback()
  assert(fired==0 and TrinketMenu.ActiveTimers.t==handles[2])
  handles[2].callback();assert(fired==1 and not TrinketMenu.IsTimerActive("t"))''')
 def test_callback_can_reschedule_itself(self):
  runtime().execute('''TrinketMenu.CreateTimer("t",function() fired=fired+1;TrinketMenu.StartTimer("t") end,.2)
  TrinketMenu.StartTimer("t");handles[1].callback()
  assert(fired==1 and TrinketMenu.ActiveTimers.t==handles[2])''')
 def test_repeating_timer_keeps_cancellable_handle(self):
  runtime().execute('''TrinketMenu.CreateTimer("t",function() fired=fired+1 end,.2,1)
  TrinketMenu.StartTimer("t");handles[1].callback();handles[1].callback()
  assert(fired==2 and TrinketMenu.IsTimerActive("t"))
  TrinketMenu.StopTimer("t");assert(handles[1].cancelled)''')
if __name__=='__main__': unittest.main(verbosity=2)
