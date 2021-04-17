from main import Profile
from main import plurality
from main import k_approval
from main import borda_truncated
from main import borda
from main import k_approval_scores
from main import trunc_Borda_scores
from main import dict_positions
from main import dict_scores
from main import max_key_in_dict
from main import scoring_rule
from main import generate_IC_preferences
from main import borda_utility
from main import rawls_utility
from main import nash_utility
from main import euclidean_distance
from main import euclidean_preferences
from main import naming_function
import unittest
import numpy


class Profile_Tests(unittest.TestCase):
    def test_number_of_agents(self):
        p = Profile([[], [], [], []])
        result = p.agents_num()
        self.assertEqual(result, 4)
    
    def test_number_of_candidates(self):
        p = Profile([[1, 2, 3], [1, 2, 3], [2, 3, 1]])
        self.assertEqual(p.candidates_num(), 3)
    
    def test_number_of_candidates2(self):
        p = Profile([[1, 2, 3, 4], [1, 2, 3, 4], [2, 3, 1, 4]])
        self.assertEqual(p.candidates_num(), 4)

    def test_first_pref(self):
        p = Profile([[1, 2, 3], [1, 2, 3], [2, 3, 1]])
        self.assertEqual(p.first_pref(), [1, 1, 2])

    def test_first_pref_big_profile(self):
        p = Profile([[1, 2, 3, 4, 5, 6], [2, 3, 5, 7, 9, 6], [3, 2, 1, 0, 4, 5], [4, 3, 5, 7, 9, 6], [5, 3, 5, 7, 9, 6],
                     [6, 3, 5, 7, 9, 10], [7, 3, 5, 2, 9, 6], [8, 3, 5, 7, 9, 6]])
        self.assertEqual(p.first_pref(), [1, 2, 3, 4, 5, 6, 7, 8])

    def test_profile_init(self):
        p = Profile([[1, 2, 3], [1, 2, 3], [2, 3, 1]])
        self.assertEqual(p._preferences, [[1, 2, 3], [1, 2, 3], [2, 3, 1]])
        
    def test_candidates_names(self):
        p = Profile([[1, 2, 3], [1, 2, 3], [2, 3, 1]])
        self.assertEqual(p.candidates_names(), [1, 2, 3])
    
    def test_candidates_names2(self):
        p = Profile([[3, 2, 1], [1, 2, 3], [2, 3, 1]])
        self.assertEqual(p.candidates_names(), [1, 2, 3])
    
    def test_candidates_num(self):
        p = Profile([[1, 2, 3], [1, 2, 3], [2, 3, 1]])
        self.assertEqual(p.candidates_num(), 3)
    
    def test_candidates_num2(self):
        p = Profile([[1, 2, 3,5,4], [1, 2,4,5, 3], [4,2, 3,5, 1]])
        self.assertEqual(p.candidates_num(), 5)

        
class Plurality_Tests(unittest.TestCase):
    def test_plurality_ties(self):
        p = Profile([[1, 2, 3], [1, 2, 3], [2, 3, 1], [2, 3, 1]])
        self.assertEqual(plurality(p), [1, 2])
        
    def test_plurality_no_ties(self):
        p = Profile([[1, 2, 3], [1, 2, 3], [2, 3, 1]])
        self.assertEqual(plurality(p), [1])

    def test_plurality_agents(self):
        p = Profile([[1, 2, 3], [1, 2, 3], [2, 3, 1], [1, 2, 3], [2, 1, 3]])
        self.assertEqual(plurality(p), [1])

    def test_plurality_cands_ties(self):
        p = Profile([[1, 2, 3, 4, 5], [2, 4, 5, 1, 3], [4, 5, 2, 3, 1]])
        self.assertEqual(plurality(p), [1, 2, 4] )
        

class k_first_pref_Tests(unittest.TestCase):    
    def test_k_first_pref(self):
        p = Profile([[1, 2, 3], [1, 2, 3], [2, 3, 1]])
        self.assertEqual(p.k_first_pref(2), [[1, 2], [1, 2], [2, 3]])

    def test_k2_first_pref_long(self):
        p = Profile([[1, 2, 3, 4, 5, 6], [2, 3, 5, 7, 9, 6], [3, 2, 1, 0, 4, 5], [4, 3, 5, 7, 9, 6], [5, 3, 5, 7, 9, 6], [6, 3, 5, 7, 9, 10], [7, 3, 5, 2, 9, 6], [8, 3, 5, 7, 9, 6]])
        self.assertEqual(p.k_first_pref(2), [[1, 2], [2, 3], [3, 2], [4, 3], [5, 3], [6, 3], [7, 3], [8, 3]])

    def test_k1_first_pref_long(self):
        p = Profile([[1, 2, 3, 4, 5, 6], [2, 3, 5, 7, 9, 6], [3, 2, 1, 0, 4, 5], [4, 3, 5, 7, 9, 6], [5, 3, 5, 7, 9, 6], [6, 3, 5, 7, 9, 10], [7, 3, 5, 2, 9, 6], [8, 3, 5, 7, 9, 6]])
        self.assertEqual(p.k_first_pref(1), [[1], [2], [3], [4], [5], [6], [7], [8]])

class candidate_positions_Tests(unittest.TestCase):
    def candidate_positions(self):
        p = Profile([[1, 2, 3], [1, 2, 3], [2, 3, 1]])
        self.assertEqual(p.candidate_positions(1), [0, 0, 2])
    def candidate_positions_Big(self):
        p = Profile([[1, 2, 3, 4, 5, 6], [1, 6, 5, 4, 2, 3], [4, 6, 5, 1, 3, 2], [5, 1, 4, 6, 2, 3]])
        self.assertEqual(p.candidate_positions(6), [5, 1, 1, 3])
    
    def candidate_Borda_positions(self):
        p = Profile([[1, 2, 3], [1, 2, 3], [2, 3, 1]])
        self.assertEqual(p.candidate_Borda_positions(1), [2, 2, 0])
    def candidate_Borda_positions_Big(self):
        p = Profile([[1, 2, 3, 4, 5, 6], [1, 6, 5, 4, 2, 3], [4, 6, 5, 1, 3, 2], [5, 1, 4, 6, 2, 3]])
        self.assertEqual(p.candidate_Borda_positions(6), [0, 4, 4, 2])

class k_approval_Tests(unittest.TestCase): 
    def test_k1_approval(self):
        p = Profile([[1, 2, 3], [1, 2, 3], [2, 3, 1]])
        self.assertEqual(k_approval(p, 1), [1])

    def test_k2_approval_tie(self):
        p = Profile([[1, 2, 3], [1, 2, 3], [2, 3, 1], [1, 3, 2]])
        self.assertEqual(k_approval(p, 2), [1, 2])
        
    def test_k4_approval_big(self):
        p = Profile([[1, 2, 3, 4, 5, 6], [2, 3, 4, 5, 1, 6], [3, 2, 1, 6, 4, 5], [4, 3, 5, 2, 1, 6], [5, 1, 2, 4, 3, 6], [6, 1, 5, 2, 4, 3], [1, 3, 5, 2, 4, 6], [2, 3, 5, 1, 4, 6]])
        self.assertEqual(k_approval(p, 4), [2])
        
        

class TestBorda_Truncated(unittest.TestCase):
    def test_trunc_Borda1(self):
        profile = Profile([[1, 2, 3, 4, 5, 6], [1, 6, 5, 4, 2, 3], [4, 6, 5, 1, 3, 2], [5, 1, 4, 6, 2, 3]])
        self.assertEqual(borda_truncated(profile, 1), [1])
    def test_trunc_Borda2_tie(self):
        p = Profile([[1, 2, 3], [2, 1, 3], [2, 3, 1], [2, 3, 1], [2, 1, 3], [1, 2, 3], [1, 2, 3], [3, 1, 2], [3, 1, 2],
                     [3, 1, 2]])
        self.assertEqual(borda_truncated(p, 2), [1, 2])
    def test_trunc_Borda3(self):
        p = Profile([[1, 2, 3, 4, 5, 6], [1, 6, 5, 4, 2, 3], [4, 6, 5, 1, 3, 2], [5, 1, 4, 6, 2, 3]])
        self.assertEqual(borda_truncated(p, 3), [1])
    
    def test_trunc_Borda4(self):
        p = Profile(
            [[1, 2, 3, 4, 5, 6], [5, 1, 6, 4, 2, 3], [5, 6, 4, 1, 3, 2], [5, 1, 4, 6, 2, 3], [3, 4, 2, 6, 1, 5]])
        self.assertEqual(borda_truncated(p, 1), [5])
    def test_trunc_Borda5(self):
        p = Profile([[1, 2, 3], [2, 1, 3], [2, 3, 1], [2, 3, 1], [2, 1, 3], [1, 2, 3], [1, 2, 3], [3, 1, 2], [3, 1, 2],
                     [3, 1, 2], [1, 2, 3]])
        self.assertEqual(borda_truncated(p, 2), [1])
    def test_trunc_Borda6_tie(self):
        p = Profile([[1, 5, 3, 4, 2, 6], [1, 5, 6, 4, 2, 3], [4, 6, 5, 1, 3, 2], [5, 1, 4, 6, 2, 3]])
        self.assertEqual(borda_truncated(p, 3), [1, 5])
    
    def test_trunc_Borda_big(self):
        p = Profile([[1, 2, 3], [2, 1, 3], [2, 3, 1], [2, 3, 1], [2, 1, 3], [1, 2, 3], [1, 2, 3], [3, 1, 2], [3, 1, 2],
                     [3, 1, 2]])
        self.assertEqual(borda_truncated(p, 1), [2])
    

class TestBorda(unittest.TestCase):
    def test_for_borda_no_ties(self):
        p = Profile([[1, 2, 3, 4, 5, 6], [1, 6, 5, 4, 2, 3], [4, 6, 5, 1, 3, 2], [5, 1, 4, 6, 2, 3]])
        self.assertEqual(borda(p), [1])

    def test_for_borda_ties(self):
        p = Profile([[1, 2, 3, 4, 5, 6], [5, 1, 6, 4, 2, 3], [5, 6, 4, 1, 3, 2], [5, 1, 4, 6, 2, 3], [3, 4, 2, 6, 1, 5]])
        self.assertEqual(borda(p), [1, 5])

    def test_for_borda_tiess(self):
        p = Profile([[1, 2, 3], [2, 1, 3], [2, 3, 1], [2, 3, 1], [2, 1, 3], [1, 2, 3], [1, 2, 3], [3, 1, 2], [3, 1, 2], [3, 1, 2]])
        self.assertEqual(borda(p), [1, 2])

class TestScores(unittest.TestCase):
    def test_k_approval_scores(self):
        self.assertEqual(k_approval_scores(3, 6), [1, 1, 1, 0, 0, 0])
    
    def test_k_approval_scores2(self):
        self.assertEqual(k_approval_scores(1, 10), [1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    
    def test_trunc_Borda_scores0(self):
        self.assertEqual(trunc_Borda_scores(3, 6), [3, 2, 1, 0, 0, 0])
    
    def test_trunc_Borda_scores1(self):
        self.assertEqual(trunc_Borda_scores(5, 6), [5, 4, 3, 2, 1, 0])
    
    def test_trunc_Borda_scores2(self):
        self.assertEqual(trunc_Borda_scores(2, 10), [2, 1, 0, 0, 0, 0, 0, 0, 0, 0])
    
    def test_garmonic_scores(self):
        self.assertEqual(garmonic_scores(3), [1, 1/2, 1/3])
        
    def test_garmonic_scores_big(self):
        self.assertEqual(garmonic_scores(10), [1, 1/2, 1/3, 1/4, 1/5, 1/6, 1/7, 1/8, 1/9, 1/10])

    def test_geometric_scores_lesser1(self):
        self.assertEqual([round(i, 4) for i in geometric_scores(0.8, 5)], [0.5904, 0.488, 0.36, 0.2, 0])

    def test_geometric_scores_bigger1(self):
        self.assertEqual([round(i, 4) for i in geometric_scores(1.5, 5)], [5.0625, 3.375, 2.25, 1.5, 1])

    def test_geometric_scores_equal1(self):
        self.assertEqual(geometric_scores(1, 5), [4, 3, 2, 1, 0])

    def test_dict_positions(self):
        p = Profile([[1, 2, 3], [1, 2, 3], [2, 3, 1], [1, 3, 2]])
        self.assertEqual(dict_positions(p), {1:{0:3,1:0,2:1}, 2:{0:1,1:2,2:1}, 3:{0:0,1:2,2:2}})

    def test_dict_positions_Big(self):
        p = Profile([[1, 2, 3, 4, 5, 6], [5, 1, 6, 4, 2, 3], [5, 6, 4, 1, 3, 2], [5, 1, 4, 6, 2, 3], [3, 4, 2, 6, 1, 5]])
        self.assertEqual(dict_positions(p), {1:{0:1,1:2,2:0,3:1,4:1, 5:0}, 2:{0:0,1:1,2:1,3:0,4:2, 5:1}, 3:{0:1,1:0,2:1,3:0,4:1,5:2}, 4:{0:0,1:1,2:2,3:2,4:0, 5:0}, 5:{0:3,1:0,2:0,3:0,4:1, 5:1}, 6:{0:0,1:1,2:1,3:2,4:0, 5:1}})
        
    def test_dict_scores(self):
        p = Profile([[1, 2, 3], [1, 2, 3], [2, 3, 1], [1, 3, 2]])
        self.assertEqual(dict_scores(p, k_approval_scores(1, 3)), {1:3, 2:1, 3:0})
    
    def test_dict_scores2(self):
        p = Profile([[1, 2, 3], [1, 2, 3], [2, 3, 1], [1, 3, 2]])
        self.assertEqual(dict_scores(p, k_approval_scores(2, 3)), {1:3, 2:3, 3:2})
        
    def test_max_key_in_dict(self):
        self.assertEqual(max_key_in_dict({1:3, 2:3, 3:2}), [1,2])
    
    def test_max_key_in_dict2(self):
        self.assertEqual(max_key_in_dict({0:0,1:1,2:1,3:0,4:2, 5:1}), [4])
    
    def test_scoring_rule(self):
        p = Profile([[1, 2, 3], [1, 2, 3], [2, 3, 1], [1, 3, 2]])
        scoring_vector = [1, 0, 0]
        self.assertEqual(scoring_rule(p, scoring_vector), [1])
    
    def test_scoring_rule_big(self):
        p = Profile([[1, 2, 3, 4, 5, 6], [5, 1, 6, 4, 2, 3], [5, 6, 4, 1, 3, 2], [5, 1, 4, 6, 2, 3], [3, 4, 2, 6, 1, 5]])
        scoring_vector = [3, 2, 1, 0, 0, 0]
        self.assertEqual(scoring_rule(p, scoring_vector), [5])

class TestIC(unittest.TestCase):
    def test_for_IC_preferences_size(self):
        p = generate_IC_preferences(4, 6)
        self.assertEqual(numpy.shape(p), (4, 6))

    def test_for_IC_preferences_no_repeat_smallest(self):
        p = generate_IC_preferences(2, 2)
        self.assertNotEqual(p, [[1, 1], [0, 0]])
        self.assertNotEqual(p, [[0, 0], [1, 1]])

    def test_for_IC_preferences_no_repeat_small(self):
        p = generate_IC_preferences(3, 2)
        a = [[1, 1]]
        b = [[0, 0]]
        self.assertNotIn(a, p)
        self.assertNotIn(b, p)

    def test_for_IC_preferences_no_repeat_large(self):
        p = generate_IC_preferences(10000, 2)
        a = [[1, 1]]
        b = [[0, 0]]
        self.assertNotIn(a, p)
        self.assertNotIn(b, p)

    def test_for_IC_preferences_no_repeat_big(self):
        p = generate_IC_preferences(4, 7)
        self.assertNotEqual(p, [[51, 3, 4, 2, 0, 1, 6], [0, 6, 1, 5, 2, 3, 4], [0, 3, 6, 4, 2, 5, 1], [4, 5, 3, 1, 6, 2, 0]])
        self.assertNotEqual(p, [[1, 3, 4, 2, 0, 1, 6], [0, 6, 1, 5, 2, 3, 4], [0, 3, 6, 4, 2, 5, 1], [4, 5, 3, 1, 6, 2, 0]])
        self.assertNotEqual(p, [[5, 5, 5, 5, 5, 5, 5], [0, 6, 1, 5, 2, 3, 4], [0, 3, 6, 4, 2, 5, 1], [4, 5, 3, 1, 6, 2, 0]])


class Test_Borda_utility(unittest.TestCase):
    def test_Borda_utility_borda(self):
        p = Profile([[1, 2, 3, 4, 5, 6], [1, 6, 5, 4, 2, 3], [4, 6, 5, 1, 3, 2], [5, 1, 4, 6, 2, 3]])
        self.assertEqual(borda_utility(p, 1), 16)
    
    def test_Borda_utility_plurality(self):
        p = Profile([[1, 2, 3], [1, 2, 3], [2, 3, 1]])
        self.assertEqual(borda_utility(p, 1), 4)
        
    def test_Borda_utility_k2(self):
        p = Profile([[1, 2, 3], [1, 2, 3], [2, 3, 1], [1, 2, 3]])
        self.assertEqual(borda_utility(p, 2), 5)


class Test_Rawls_utility(unittest.TestCase):
    def test_Rawls_utility_borda(self):
        p = Profile([[1, 2, 3, 4, 5, 6], [1, 6, 5, 4, 2, 3], [4, 6, 5, 1, 3, 2], [5, 1, 4, 6, 2, 3]])
        self.assertEqual(rawls_utility(p, 1), 2)
        
    def test_Rawls_utility_plurality(self):
        p = Profile([[1, 2, 3], [1, 2, 3], [2, 3, 1]])
        self.assertEqual(rawls_utility(p, 1), 0)
    
    def test_Rawls_utility_k2(self):
        p = Profile([[1, 2, 3], [1, 2, 3], [2, 3, 1], [1, 2, 3]])
        self.assertEqual(rawls_utility(p, 2), 1)

class Test_Nash_utility(unittest.TestCase):
    def test_Nash0_utility_borda(self):
        p = Profile([[1, 2, 3, 4, 5, 6], [1, 6, 5, 4, 2, 3], [4, 6, 5, 1, 3, 2], [5, 1, 4, 6, 2, 3]])
        self.assertEqual(nash_utility(p, 1), 200)
        
    def test_Nash0_utility_plurality(self):
        p = Profile([[1, 2, 3], [1, 2, 3], [2, 3, 1]])
        self.assertEqual(nash_utility(p, 1), 0)
    
    def test_Nash0_utility_k2(self):
        p = Profile([[1, 2, 3], [1, 2, 3], [2, 3, 1], [1, 2, 3]])
        self.assertEqual(nash_utility(p, 2), 2)
        

class TestEuclidean_distance(unittest.TestCase):
    def test_euclidean_distance_naive(self):
        point_a = [1, 1, 1, 1]
        point_b = [0, 0, 0, 0]
        self.assertEqual(euclidean_distance(point_a, point_b), 4)    
    
    def test_euclidean_distance_big(self):
        point_a = [10, 5, 3, 6, 2, 3]
        point_b = [8, 0, 7, 5, 6, 9]
        self.assertEqual(euclidean_distance(point_a, point_b), 98)  
    
class TestNaming_function(unittest.TestCase):
    def test_naming_function_small(self):
        nested_list = [['a', 'b', 'c'], ['a', 'b', 'c'], ['b', 'c', 'a']]
        num_names = len(nested_list[0])
        self.assertEqual(naming_function(num_names, nested_list), [{0: 'a', 1: 'b', 2: 'c'}, {0: 'a', 1: 'b', 2: 'c'}, {0: 'b', 1: 'c', 2: 'a'}])    
    
    def test_naming_function_big(self):
        nested_list = [['a', 'b', 'c', 'd', 'e', 'f'], ['a', 'f', 'b', 'd', 'c', 'e'], ['b', 'd', 'c', 'e', 'f', 'a']]
        num_names = len(nested_list[0])
        self.assertEqual(naming_function(num_names, nested_list), [{0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f'}, {0: 'a', 1: 'f', 2: 'b', 3: 'd', 4: 'c', 5: 'e'}, {0: 'b', 1: 'd', 2: 'c', 3: 'e', 4: 'f', 5: 'a'}])    

class TestEuclidean_preferences(unittest.TestCase):
    def test_Euclidean_preferences_00(self):
        self.assertEqual(euclidean_preferences(1, 3, 1).agents_num(), 1)    
    
    def test_Euclidean_preferences_01(self):
        self.assertEqual(euclidean_preferences(10, 3, 4).agents_num(), 10)  
    
    def test_Euclidean_preferences_10(self):
        self.assertEqual(euclidean_preferences(1, 3, 1).candidates_num(), 3) 
    
    def test_Euclidean_preferences_11(self):
        self.assertEqual(euclidean_preferences(1, 22, 4).candidates_num(), 22)
    
    


if __name__ == "__main__":
    unittest.main()
