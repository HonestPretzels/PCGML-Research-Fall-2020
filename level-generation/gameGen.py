import random
from vgdl.parser import Node
from gameComprehension import *

# SPRITES

SPRITE_CLASSES = [
    'Bomber',
    'Chaser',
    'Fleeing',
    'Flicker',
    'Immovable',
    'Missile',
    'OrientedFlicker',
    'Passive',
    'Portal',
    'RandomNPC',
    'SpawnPoint',
    'Spreader',
    'Resource'
]

SPRITE_IMAGES = [
  'oryx/alien1',
  'oryx/alien2',
  'oryx/bat1',
  'newset/bandit1',
  'newset/block1',
  'newset/barrier1',
]

SPRITE_MODIFIERS = {
  'color': [
    'GREEN',
    'BLUE',
    'RED',
    'GRAY',
    'WHITE',
    'BROWN',
    'BLACK',
    'ORANGE',
    'YELLOW',
    'PINK',
    'GOLD',
    'LIGHTRED',
    'LIGHTORANGE',
    'LIGHTBLUE',
    'LIGHTGREEN',
    'LIGHTGRAY',
    'DARKGRAY',
    'DARKBLUE',
  ],
  'orientation': [
    'LEFT',
    'RIGHT',
    'UP',
    'DOWN',
  ],
  'hidden': ['True', 'False'],
  'invisible': ['True', 'False'],
  'singleton': ['True', 'False'],
  'autoTiling': ['True', 'False'],
  'cooldown': [0, 20],
  'speed': [0, 1],
  'prob': [0, 1],
  'limit': [1, 10],
  'shrinkFactor': [0, 1],
}

AVATAR_CLASSES = [
  'FlakAvatar',
  'MovingAvatar',
  'ShootAvatar',
]

def addSprite(parent: Node, sprite: Node):
  sprite.indent = parent.indent + 4
  parent.insert(sprite)

def removeSprite(parent: Node, sprite: Node):
  idx = 0
  for child in parent.children:
    if child.content == sprite.content:
      parent.children.pop(idx)
    idx += 1
  
def newSprite(name, content):
  return Node(name + ' > ' + content, 8)

def randomSprite(otherSprites):
  sClass = random.choice(SPRITE_CLASSES)
  image = random.choice(SPRITE_IMAGES)
  sprite = sClass + ' img=' + image 
  sprite = sprite + ' orientation=' + random.choice(SPRITE_MODIFIERS['orientation'])

  if sClass in ['Bomber', 'SpawnPoint', 'Chaser', 'Fleeing', 'Portal']:
    sprite = sprite + ' stype=' + random.choice(otherSprites)

  optionCount = random.randint(0,3)
  for _ in range(optionCount):
    sprite = addOption(sprite)
  return sprite

def addOption(sprite):
  option = random.choice(list(SPRITE_MODIFIERS.keys()))
  strOption = str(option)
  if strOption in ['cooldown', 'limit']: # int
    value = random.randint(SPRITE_MODIFIERS[option][0], SPRITE_MODIFIERS[option][1])
  elif strOption in ['speed', 'prob', 'shrinkFactor']: # float
    value = random.uniform(SPRITE_MODIFIERS[option][0], SPRITE_MODIFIERS[option][1])
  else:
    value = random.choice(SPRITE_MODIFIERS[option])
  return sprite + ' ' + strOption + '=' + str(value)

def randomAvatar():
  aClass = random.choice(AVATAR_CLASSES)
  image = random.choice(SPRITE_IMAGES)
  return aClass + ' img=' + image

# INTERACTIONS

INTERACTION_TYPES = [
    'killSprite',
    'killBoth',
    'cloneSprite',
    'transformTo',
    'stepBack',
    'undoAll',
    'bounceForward',
    'attractGaze',
    'flipDirection',
    'turnAround',
    'reverseDirection',
    'killIfFromAbove',
    'collectResource', # This is probably broken for now
    'changeResource',
    'spawnIfHasMore',
    'killIfHasMore',
    'killIfOtherHasMore',
    'killIfHasLess',
    'killIfOtherHasLess',
    'wrapAround',
    'pullWithIt',
    'teleportToExit',
]

def addInteraction(parent: Node, interaction: Node):
  interaction.indent = parent.indent + 4
  parent.insert(interaction)

def newInteraction(spriteName, partnerName, interaction, options):
  return Node(spriteName + ' ' + partnerName + ' > ' + interaction + ' ' + ' '.join(options), 8)

def randomInteraction(spriteName, partnerName, resources, sTypes):
  interaction = random.choice(INTERACTION_TYPES)
  options = []

  if interaction in ['changeResource', 'spawnIfHasMore', 'killIfHasMore', 'killIfOtherHasMore', 'killIfHasLess', 'killIfOtherHasLess']:
    options.append('resource=' + random.choice(resources))
    if interaction == 'changeResource':
      options.append('value=' + str(random.randint(-5, 5)))
  
  if interaction in ['transformTo', 'spawnIfHasMore']:
    options.append('stype=' + random.choice(sTypes))

  if interaction in ['spawnIfHasMore', 'killIfHasMore', 'killIfOtherHasMore', 'killIfHasLess', 'killIfOtherHasLess']:
    options.append('limit=' + str(random.randint(1, 5)))
  
  if interaction == 'wrapAround':
    options.append('offset=' + str(random.randint(0, 3)))
  
  if interaction == 'killIfSlow':
    options.append('limitSpeed=' + str(random.randint(0, 3)))
  
  if interaction in ['bounceDirection', 'wallBounce', 'wallStop']:
    options.append('friction=' + str(random.uniform(0, 2)))

  if interaction in ['slipForward', 'attractGaze']:
    options.append('prob=' + str(random.uniform(0, 1)))
  
  if random.uniform(0, 1) > 0.5:
    options.append('scoreChange=' + str(random.randint(-5, 5)))

  return newInteraction(spriteName, partnerName, interaction, options)

# TERMINATIONS

TERMINATION_TYPES = [
    'SpriteCounter',
    # 'MultiSpriteCounter', Removed for now
    'ResourceCounter',
    'Timeout',
  ]

def addTermination(parent: Node, termination: Node):
  termination.indent = parent.indent + 4
  parent.insert(termination)

def newTermination(terminationType, options):
  return Node(terminationType + ' ' + ' '.join(options), 8)

def randomTermination(sTypes, resources, win):
  terminationType = random.choice(TERMINATION_TYPES)
  options = []

  if terminationType == 'SpriteCounter':
    options.append('stype=' + random.choice(sTypes))
    options.append('limit=' + str(random.randint(0, 10)))

  if terminationType == 'ResourceCounter':
    options.append('stype=' + random.choice(resources))
    options.append('limit=' + str(random.randint(0, 100)))
  
  if terminationType == 'Timeout':
    options.append('limit=' + str(random.randint(10, 1000)))

  options.append('win=' + str(win))
  if random.uniform(0, 1) > 0.8:
    options.append('scoreChange=' + str(random.randint(0, 500)))

  return newTermination(terminationType, options)

# MAPPING

CHARS = 'qwertyuiopasdfghjklzxcvbnm1234567890,./;[]?:"!@#$%^&*()'

def generateLevelMapping(spriteNames, avatarName):
  chars = random.sample(CHARS, len(spriteNames))
  mapping = {chars.pop(): name  for name in spriteNames}
  mapping['A'] = avatarName
  return mapping

# OUTPUT

# Recurse through a tree and write to the stream
def writeNodes(stream, spriteNode: Node):
  stream.write(' ' * spriteNode.indent + spriteNode.content + '\n')
  for child in spriteNode.children:
    writeNodes(stream, child)

# Write a dictionary level mapping to the stream
def writeLevelMapping(stream, mapping: dict):
  stream.write('    LevelMapping\n')
  for key in mapping.keys():
    stream.write('        ' + key + ' > ' + mapping[key] + '\n')

# Take a stream and write all game parts to it
def writeToFile(stream, gameDescription, spriteNode, levelMapping, terminations, interactions):
    stream.write(gameDescription + '\n')
    stream.write('\n')
    writeNodes(stream, spriteNode)
    stream.write('\n')
    writeLevelMapping(stream, levelMapping)
    stream.write('\n')
    writeNodes(stream, interactions)
    stream.write('\n')
    writeNodes(stream, terminations)

def randomGen(outPath):
  spriteRoot = Node('SpriteSet', 4)
  interactionRoot = Node('InteractionSet', 4)
  terminationRoot = Node('TerminationSet', 4)
  gameDesc = 'BasicGame block_size=10'

  spriteNames = []
  resources = []

  addSprite(spriteRoot, newSprite('avatar', randomAvatar()))
  for idx in range(8):
    rSprite = newSprite('test' + str(idx), randomSprite(['test' + str(i) for i in range(8) if i != idx]))
    if rSprite.content.split('>')[1].split()[0].strip() == 'Resource':
      resources.append('test' + str(idx))
    spriteNames.append('test' + str(idx))
    addSprite(spriteRoot, rSprite)

  if len(resources) == 0:
    addSprite(spriteRoot, Node('testResource > Resource color=' + random.choice(SPRITE_MODIFIERS['color']), 8))
    resources.append('testResource')
    spriteNames.append('testResource')

  levelMapping = generateLevelMapping(spriteNames, 'avatar')

  for _ in range (5):
    spriteChoices = random.sample(spriteNames, 2)
    rInteraction = randomInteraction(spriteChoices[0], spriteChoices[1], resources, spriteNames)
    addInteraction(interactionRoot, rInteraction)

  winCondition = randomTermination(spriteNames, resources, True)
  loseCondition = randomTermination(spriteNames, resources, False)
  addTermination(terminationRoot, winCondition)
  addTermination(terminationRoot, loseCondition)

  with open(outPath, 'w') as out:
    writeToFile(out, gameDesc, spriteRoot, levelMapping, terminationRoot, interactionRoot)

# Substitution generation

def nameSub(pre, post, root):
  if len(root.children) != 0:
    for child in root.children:
      child.content.replace(pre, post)
      nameSub(pre, post, child)

def getLeaves(node, leaves):
  if len(node.children) == 0:
    return node
  else:
    for child in node.children:
      leaves += [getLeaves(child, leaves)]
    return leaves

def subRandomSprite(spriteRoot):
  nodes = getLeaves(spriteRoot, [])
  nodes = [n for n in nodes if 'Resource' not in n.content]
  nodes = [n for n in nodes if 'avatar' not in n.content]
  
  spriteToSwap = random.randint(0, len(nodes) - 1)

  pre = nodes[spriteToSwap].content.split('>')[0]
  
  otherSprites = [nodes[i].content.split('>')[0] for i in range(len(nodes)) if i != spriteToSwap]

  rSprite = randomSprite(otherSprites)

  getNode(spriteRoot, nodes[spriteToSwap].content).content = pre + ' > ' + rSprite

def subRandomInteraction(interactionRoot, resources, sprites):
  nodes = getLeaves(interactionRoot, [])
  
  interactionToSwap = random.randint(0, len(nodes) - 1)
  
  pre = nodes[interactionToSwap].content.split('>')[0].split(' ')

  rInteraction = randomInteraction(pre[0], pre[1], resources, sprites)

  old = getNode(interactionRoot, nodes[interactionToSwap].content)
  old.parent.children.remove(old)

  addInteraction(interactionRoot, rInteraction)

def subRandomTermination(terminationRoot, resources, sprites):
  nodes = getLeaves(terminationRoot, [])
  
  terminationToSwap = random.randint(0, len(nodes) - 1)
  if 'win=True' in nodes[terminationToSwap].content:
    rTermination = randomTermination(sprites, resources, True)
  else:
    rTermination = randomTermination(sprites, resources, False)
  
  old = getNode(terminationRoot, nodes[terminationToSwap].content)
  old.parent.children.remove(old)

  addTermination(terminationRoot, rTermination)

def getResources(root):
  leaves = []
  def __getResources(node):
    if node is not None:
      if 'Resource' in node.content:
        leaves.append(node.content.split('>')[0].strip())
      for n in node.children:
        __getResources(n)
  __getResources(root)
  return leaves

def getSpriteNames(root):
  leaves = []
  def __getSpriteNames(node):
    if node is not None:
      if len(node.children) == 0:
        leaves.append(node.content.split('>')[0].strip())
      for n in node.children:
        __getSpriteNames(n)
  __getSpriteNames(root)
  return leaves

def subGen(initialGamePath, spriteSubs, interactionSubs, terminationSubs):
  with open(initialGamePath, 'r') as preGame:
    gameDesc = preGame.readline().strip()

  spriteRoot = getSpriteSetNode(initialGamePath)
  interactionRoot = getInteractionSetNode(initialGamePath)
  terminationRoot = getTerminationSetNode(initialGamePath)

  # Sub sprites (Only works on sprites with no children for now and keeps resources)
  for i in range(spriteSubs):
    subRandomSprite(spriteRoot)

  for i in range(interactionSubs):
    subRandomInteraction(interactionRoot, getResources(spriteRoot), getSpriteNames(spriteRoot))

  for i in range(terminationSubs):
    subRandomTermination(terminationRoot, getResources(spriteRoot), getSpriteNames(spriteRoot))

  levelMapping = generateLevelMapping([name for name in getSpriteNames(spriteRoot) if name != 'avatar'], 'avatar')

  with open(initialGamePath.split('.')[0] + '_sub.txt', 'w') as out:
    writeToFile(out, gameDesc, spriteRoot, levelMapping, terminationRoot, interactionRoot)

if __name__ == "__main__":
  #randomGen('level-generation/outputs/testGame.txt')
  subGen('games/frogs.txt', 0, 1, 1)

      
