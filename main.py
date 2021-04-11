class Profile:
  def __init__(self, preferences):
      self._preferences = preferences
        
class Room:
  def __init__(self, generate_new_agent, play_track, update_happiness, happiness_threshold, number_of_genres):
    self.generate_new_agent = generate_new_agent
    self.play_track = play_track
    self.update_happiness = update_happiness
    self.happiness_threshold = happiness_threshold
    self.number_of_genres = number_of_genres
    self.agents = []
    self.history = []
    
  def get_profile(self):
    preferences = [agent[0] for agent in self.agents]
    return Profile(preferences)
    
  def update_agents(self):
    for agent in self.agents:
      self.update_happiness(agent, self.history)
    self.agents = [agent for agent in self.agents if agent[1]>= self.happiness_threshold]
    
  def next_period(self):
    new_agent = self.generate_new_agent(self.number_of_genres)
    self.agents.append(new_agent)
    new_track = self.play_track(self.get_profile())
    self.history.append(new_track)
    self.update_agents()
    
  def print_state(self):
    print("Tracks played: " + str(self.history))
    print("Currently in room:")
    for agent in self.agents:
      print(str(agent[0]) + ", happiness: " + str(agent[1]))
  
def everyone_is_unique(m):
  initial_happiness = 0
  preferences = list(range(0,m))
  return [preferences, initial_happiness]
  
def play_michael_jackson(profile):
  the_king_of_pop = 0
  return the_king_of_pop
  
def i_dont_like_the_drugs_but_the_drugs_like_me(agent, history):
  agent[1] += 1
  
if __name__ == "__main__":
  room = Room(everyone_is_unique, play_michael_jackson, i_dont_like_the_drugs_but_the_drugs_like_me, 0, 3)
  for i in range(0,5):
    room.next_period()
    room.print_state()
    print("")
