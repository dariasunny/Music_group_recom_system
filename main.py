class Profile:
  def __init__(self, preferences):
      self._preferences = preferences
  def agents_num(self):
        return len(self._preferences)
    def candidates_num(self):
        return len(self._preferences[0])
    def candidates_names(self):
        return sorted(self._preferences[0])    
    def first_pref(self):
        return [x[0] for x in self.k_first_pref(1)]
    def k_first_pref(self, k):
        return [item[0:k] for item in self._preferences]
    def pref(self):
        return [item[:] for item in self._preferences]
    def candidate_positions(self, candidate):
        list_positions = []
        for preference in self._preferences:
            list_positions.append(preference.index(candidate))
        return list_positions
    def candidate_Borda_positions(self, candidate):
        m = self.candidates_num()
        return [m-1-pos for pos in self.candidate_positions(candidate)]

      
def k_approval_scores(k, m):
    return [1 for i in range(k)]+[0 for i in range(m-k)]

def trunc_Borda_scores(k, m):
    return [*range(k, 0, -1)]+[0 for i in range(m-k)]
  
def garmonic_scores(m):
    return [1/i for i in range(1, m+1)]

def geometric_scores(p, m):
    if p > 1:
        return [p**(m-i) for i in range(1, m+1)]
    if p == 1:
        return [m-i for i in range(1, m+1)]
    if p < 1:
        return [(1 - p**(m-i)) for i in range(1, m+1)]
  
def dict_positions(profile):
    candidates_names = profile.candidates_names()
    candidates_num = profile.candidates_num()
    list_of_lists_positions = [profile.candidate_positions(candidate) for candidate in candidates_names]
    list_dict = []
    for each_list in list_of_lists_positions:
        dict_count_positions = {}
        for j in range(candidates_num):
            dict_count_positions[j] = 0
        for value in each_list:
            dict_count_positions[value] = dict_count_positions.get(value, 0) + 1
        list_dict.append(dict_count_positions)
    return dict(zip(candidates_names, list_dict))

def dict_scores(profile, scoring_vector):
    candidates_names = profile.candidates_names()
    dict_positions1 = dict_positions(profile)
    matrix_positions = []
    for candidate in candidates_names:
        matrix_positions.append(list(dict_positions1.get(candidate).values()))
    return dict(zip(candidates_names, np.dot(np.array(matrix_positions), np.array(scoring_vector))))

def max_key_in_dict(dictionary):
    max_list = []
    m = max(dictionary.keys(), key=(lambda k: dictionary[k]))
    for key in dictionary:
        if dictionary[key] == dictionary[m]:
            max_list.append(key)
    return max_list

def scoring_rule(profile, scoring_vector):
    return max_key_in_dict(dict_scores(profile, scoring_vector))

def plurality(profile):
    scores = k_approval_scores(1, profile.candidates_num())
    return scoring_rule(profile, scores)

def k_approval(profile, k):
    scores = k_approval_scores(k, profile.candidates_num())
    return scoring_rule(profile, scores)

def borda(profile):
    m = profile.candidates_num()
    scores = trunc_Borda_scores(m-1, m)
    return scoring_rule(profile, scores)

def borda_truncated(profile, v):
    scores = trunc_Borda_scores(v, profile.candidates_num())
    return scoring_rule(profile, scores)

def generate_IC_preferences(voters, candidates):
    i = 1
    preferences = []
    while i <= voters:
        rng = default_rng()
        num = list(rng.choice(candidates, size= candidates, replace=False))
        preferences.append(num)
        i += 1
    return preferences
    return Profile(preferences)

def naming_function(names_num, nested_list):
    names = [*range(0, names_num)]
    return [dict(zip(names, each_list)) for each_list in nested_list]

def euclidean_preferences(n, m, k):
    voters = [[random.uniform(-1, 1) for i in range(k)] for a in range(n)]
    candidates = [[random.uniform(-1, 1) for i in range(k)] for a in range(m)]
    distances_list = [[euclidean_distance(voter, candidate) for candidate in candidates] for voter in voters]
    unordered_named_nested_list = naming_function(len(candidates), distances_list)
    
    profile = []
    for i in unordered_named_nested_list:
        sorted_distance = sorted(i.items(), key = lambda item: item[1])
        preferences = []
        for j in sorted_distance:
            candidate_name = j[0]
            preferences.append(candidate_name)
        profile.append(preferences)
    return Profile(profile)

def borda_utility(profile, winner):
    return sum(profile.candidate_Borda_positions(winner))

def rawls_utility(profile, winner):
    return min(profile.candidate_Borda_positions(winner))

def nash_utility(profile, winner):
    return np.prod(profile.candidate_Borda_positions(winner))

def euclidean_distance(point_1, point_2):
    return sum((np.array(point_1) - np.array(point_2))**2)  
      
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
