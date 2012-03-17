import os
import re
from datetime import datetime
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
      self.effect = ''
      return
    self.type = x.split(':')[0]
    self.detail = x.split(':')[1]

class Value:
  def __init__(self, x):
    if not x:
      self.value = 0
      self.type = ''
      return
    foo = x.split(' ')
    self.value = int(x[0])
    if len(x) > 1:
      self.type = x[1]
    else:
      self.type=''

class Roll:
  def __init__(self, x):
    if not x:
      self.value = 0
      self.type = ''
      return
    foo = x.split(' ')
    self.value = int(x[0])
    if len(x) > 1:
      self.type = x[1]
    else:
      self.type=''

#date, source, target, ability, effect.type/detail, value.value/type, roll
def main():
  if len(sys.argv) == 1:
    print 'File not specified, defaulting to data.txt'
    filename = 'data.txt'
  else:
    filename = sys.argv[1]
  file = open(filename, 'r')
  events = []
  for line in file.readlines():
    events.append(Event(line))

  players = set([event.source.name for event in events])
  print players
  for player in players:
    combat = False
    dmg = 0
    for event in events:
      if 'EnterCombat' in event.effect.detail:
        combat = event.date
      if 'ExitCombat' in event.effect.detail:
        if combat:
          print 'Player %s did %d in %s' % (player, dmg, str(event.date-combat))
        combat = False
        
      if not combat:
        continue

      if event.source.name == player and 'Damage ' in event.effect.detail:
        dmg += event.value.value
        
  #print "\n".join([event.to_string for event in events])
if __name__ == "__main__":
  main()
