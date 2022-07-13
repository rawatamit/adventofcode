import re
from aocd import get_data

class Deer:
  def __init__(self, name, speed, time, rest):
    self.name = name
    self.speed = speed
    self.time = time
    self.rest = rest
    self.points = 0
    self.tick = 0
    self.dist = 0
    self._run_start = 0
    self._run_end = self.time

  def __str__(self):
    return f'Deer({self.name}, speed={self.speed}, time={self.time}, rest={self.rest}, dist={self.dist}, points={self.points})'

  def __repr__(self):
    return str(self)

  def update_tick(self):
    # is not resting
    if self._run_start <= self.tick < self._run_end:
      self.dist += self.speed

    if self.tick == self._run_end:
      self._run_start = self._run_end + self.rest
      self._run_end += self.rest + self.time

    self.tick += 1
    return self.dist


def simulate_race(deer, ticks):
  max_dist = -1
  for tick in range(ticks):
    for adeer in deer:
      dist = adeer.update_tick()
      max_dist = max(max_dist, dist)

    #print(deer)
    for adeer in deer:
      if adeer.dist == max_dist:
        adeer.points += 1


def compute_distance(speed, time, rest, ticks):
  curticks = 0
  dist = 0
  while curticks < ticks:
    time_left = time if curticks + time <= ticks else ticks - curticks
    dist += speed * time_left
    curticks += time + rest
  return dist

def main():
  data = '''
    Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
    Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
'''.strip()
  data = get_data(year=2015, day=14)
  pattern = '(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.'
  max_dist = -1
  ticks = 2503
  deer = []
  for line in data.split('\n'):
    deername, speed, time, rest = re.findall(pattern, line)[0]
    deer.append(Deer(deername, int(speed), int(time), int(rest)))
    # part 1
    max_dist = max(max_dist, compute_distance(int(speed), int(time), int(rest), ticks))

  # part 1
  print(max_dist)

  # part 2
  simulate_race(deer, 2503)
  deer.sort(key=lambda adeer: adeer.points, reverse=True)
  print(deer[0])

main()