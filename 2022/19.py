from copy import copy
from collections import defaultdict, deque
import math
import re
import sys

input_file = sys.argv[1] if len(sys.argv) > 1 else '/Users/markeccles/adventcode/2022/19.txt'
X = [line.strip() for line in open(input_file)]

ORE, CLAY, OBSIDIAN, GEODE = 1, 2, 3, 4 # Aliases
RES_TYPES = [ORE, CLAY, OBSIDIAN, GEODE]

blueprints = []
for line in X:
  numbers = [int(n) for n in re.findall(R'\d+', line)]
  blueprints.append(
    {
      'ID': numbers[0],
      'RES_REQS': {
        ORE: {
          ORE: numbers[1]
        },
        CLAY: {
          ORE: numbers[2]
        },
        OBSIDIAN: {
          ORE: numbers[3],
          CLAY: numbers[4],
        },
        GEODE: {
          ORE: numbers[5],
          OBSIDIAN: numbers[6],
        }
      }
    }
  )

def get_max_robots(blueprint):
  """Returns max effective number of each robot."""
  max_robots = {r: 0 for r in RES_TYPES}
  for _, reqs in blueprint['RES_REQS'].items():
    for robot, amount in reqs.items():
      max_robots[robot] = max(max_robots[robot], amount)
  max_robots[GEODE] = 1_000_000
  return max_robots

def get_build_options(blueprint, res):
  """Returns set of robots that can be built"""
  opts = set()
  for robot, reqs in blueprint['RES_REQS'].items():
    if all(amount <= res[req] for req, amount in reqs.items()):
      opts.add(robot)
  if GEODE in opts:
    return {GEODE} # Always prioritize Geode.
  opts.add(False)
  return opts

def build_robot(bp, robots, resources, to_build):
  """Builds a robot and subtracts resources."""
  robots[to_build] += 1
  for resource, amount in bp['RES_REQS'][to_build].items():
    resources[resource] -= amount
  return (robots, resources)

def harvest(robots, resources):
  """Harvests res."""
  for res, amount in robots.items():
    resources[res] += amount
  return resources

def initial_state():
  """Generates state in form (turn,(robots),(resources),(skipped_builds))."""
  robots = {r: 0 for r in RES_TYPES}
  robots[ORE] = 1
  res = {r: 0 for r in RES_TYPES}
  yield (0, robots, res, set())

def best_score(blueprint, max_time):
  queue = deque(initial_state())
  best_at_time = defaultdict(int)
  max_robots = get_max_robots(blueprint)
  while queue:
    t, robots, resources, skipped_builds = queue.popleft()
    best_at_time[t] = max(best_at_time[t], resources[GEODE])
    if t <= max_time and best_at_time[t] == resources[GEODE]:
      options = get_build_options(blueprint, resources)
      for buildable in options:
        if not buildable:
          res1 = harvest(robots, copy(resources))
          queue.append((t + 1, robots, res1, options))
        elif buildable in skipped_builds:
          continue
        elif robots[buildable] >= max_robots[buildable]:
          continue
        else:
          robots1, res1 = build_robot(
              blueprint, copy(robots), copy(resources), buildable)
          res1 = harvest(robots, res1)
          queue.appendleft((t + 1, robots1, res1, set()))
  return best_at_time[max_time]

print(sum(b['ID'] * best_score(b, 24) for b in blueprints))
print(math.prod([best_score(b, 32) for b in blueprints[:3]]))
