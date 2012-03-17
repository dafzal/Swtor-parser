# Danial Afzal
# iotasquared@gmail.com
import os
import re
from datetime import datetime
import sys
#[03/16/2012 22:53:45] [@Asdffljklasdfj] [@Asdffljklasdfj] [Unnatural Might {1781509484707840}] [RemoveEffect {836045448945478}: Unnatural Might {1781509484707840}] ()
#[date] [src] [target] [ability] [effect] (value) <roll>
#src = [foo {id}] or [@player]
# ability = abil {id}
# effect = type:effect
# value = # or # type
# roll? int
class Event:
  regex = r'[\[<\(]([^\[<\(\]>\)]*)[\]>\)]'
  def __init__(self, x):
    #print x
    data = re.findall(Event.regex, x)
    data.append('')
    self.to_string = '  '.join(data)
    
    date = datetime.strptime(data[0], '%m/%d/%Y %H:%M:%S')
    self.date = date
    self.source = Entity(data[1])
    self.target = Entity(data[2])
    self.ability = Ability(data[3])
    self.effect = Effect(data[4])
    self.value = Value(data[5])
    print data[5]
    print self.value.value
    self.roll = Roll(data[6])

class Entity:
  def __init__(self, x):
    if not x:
      self.name = x
      self.player = False
    elif x[0] == '@':
      self.name = x[1:]
      self.player = True
    else:
      self.name = x
      self.player = False

class Ability:
  def __init__(self, x):
    self.name = x

class Effect:
  def __init__(self, x):
    if not x:
      self.type = ''
      self.detail = ''
      return
    foo = x.split(':')
    if len(foo) > 1:
      self.type = foo[0]
      self.detail = foo[1]
    else:
      self.type = x
      self.detail = ''
      
class Value:
  def __init__(self, x):
    if not x:
      self.value = 0
      self.type = ''
      return
    foo = x.replace('*','').split(' ')
    self.value = int(foo[0])
    if len(foo) > 1:
      self.type = foo[1]
    else:
      self.type=''

class Roll:
  def __init__(self, x):
    if not x:
      self.value = 0
      self.type = ''
      return
    foo = x.replace('*','').split(' ')
    self.value = int(foo[0])
    if len(foo) > 1:
      self.type = foo[1]
    else:
      self.type=''

#date, source, target, ability, effect.type/detail, value.value/type, roll
# TODO:
#  multiple sources
#  more interesting output, graphs? What about that metric site? Google charts?
#  App engine seems fun
#  Details for abilities:
     # dmg per ability
# Combine multiple entries per ability
def main():
  if len(sys.argv) == 1:
    filename = 'argorash.txt'
    print 'File not specified, defaulting to ' + filename
  else:
    filename = sys.argv[1]
  file = open(filename, 'r')
  events = []
  for line in file.readlines():
    events.append(Event(line))

  players = set([event.source.name for event in events])
  for player in players:
    combat = False
    dmg = 0
    for event in events:
      if 'EnterCombat' in event.effect.detail:
        combat = event.date
        dmg = 0
      if 'ExitCombat' in event.effect.detail:
        if combat and dmg:
          print '%s did %d in %s' % (player, dmg, str(event.date-combat))
        combat = False
        
      if not combat:
        continue

      if event.source.name == player and 'Damage ' in event.effect.detail:
        dmg += event.value.value
        
  #print "\n".join([event.to_string for event in events])
if __name__ == "__main__":
  main()
