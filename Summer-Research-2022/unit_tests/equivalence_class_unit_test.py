
# testing each method of EquivalenceClass for functionality
# testing with list: [1, 0+1]
# adding: 1
import unittest
from equivalence_class import EquivalenceClass
import sys
  
# adding Folder_2 to the system path
sys.path.insert(0, 'C:/dev/Summer Research 2022/')

class unitTest(unittest.TestCase):

  # test functions for testing purposes
  def mult2(self, number):
      return number * 2

  def stringCheck(self, string):
    return string[0]

  # test all branches for constructor
  def test_init_empty(self):
    x = EquivalenceClass([], self.mult2)
    self.assertTrue(len(x._list) == 0)

  def test_init_non_empty(self):
    x = EquivalenceClass([1, 1], self.mult2)
    self.assertEqual(x._canonical, 1, "The canonical value is not the expected value")

  def test_init_non_list(self):
    with self.assertRaises(Exception):
      x = EquivalenceClass(1, self.mult2)

  # throws exception when non equivalent
  def test_init_non_equivalent(self):
    with self.assertRaises(Exception):
      x = EquivalenceClass([1, 0], self.mult2)

  # test that the input function can be used to verify equivalency
  def test_func(self):

    list = [3+3, 6, 9-3] 
    x = EquivalenceClass(list, self.mult2)
    isEquivalence = x.check_equivalence_set(list)
    self.assertTrue(isEquivalence, "Expected true, but input function caused check_equivalence to return false")

  # test adding a valid and invalid element to the class
  def test_add_true(self):
    x = EquivalenceClass([1], self.mult2)
    x.add(1)
    self.assertEqual(len(x._list), 2, "The item was not added")

  def test_add_false(self):
    with self.assertRaises(Exception):
      x = EquivalenceClass([1], self.mult2)
      x.add(2)

  # test that equivalence is recognized
  def test_equivalence_set(self):

    x = EquivalenceClass([1, 0+1], self.mult2)
    self.assertEqual(x.check_equivalence_set(x._list), True, "The class is not an equivalence class")

  # test that equivalence is recognized for both primitives (ints) and objects (strings)
  # for both true and false cases, and for the same object
  def test_equivalence_num_true(self):
    x = EquivalenceClass([1], self.mult2)
    boolean = x.check_equivalence(1, 1)
    self.assertTrue(boolean, "The equivalent numbers do not return true")

  def test_equivalence_num_false(self):
    x = EquivalenceClass([1], self.mult2)
    boolean = x.check_equivalence(1, 0)
    self.assertFalse(boolean, "The non-equivalent numbers do not return false")

  def test_equivalence_var_true(self):
    x = EquivalenceClass(["c"], self.stringCheck)
    boolean = x.check_equivalence("cat", "chicken")
    self.assertTrue(boolean, "The equivalent strings do not return true")

  def test_equivalence_var_false(self):
    x = EquivalenceClass(["c"], self.stringCheck)
    boolean = x.check_equivalence("cat", "lhicken")
    self.assertFalse(boolean, "The non-equivalent strings do not return false")

  def test_equivalence_var_same(self):
    x = EquivalenceClass(["c"], self.stringCheck)
    boolean = x.check_equivalence("cat", "cat")
    self.assertTrue(boolean, "The equivalent strings do not return true")

  # an empty set will throw an exception upon construction
  def test_equivalence_set_empty(self):
    with self.assertRaises(Exception):
      x = EquivalenceClass([], self.mult2)
      x.check_equivalence_set(x._set)

  def test_equivalence_set_true(self):
    x = EquivalenceClass([1, 1], self.mult2)
    boolean = x.check_equivalence_set(x._list)
    self.assertTrue(boolean, "The equivalence set is wrongly returning false for equivalency")

  # a non equivalent set will throw an exception upon construction
  def test_equivalence_set_false(self):
    with self.assertRaises(Exception):
      x = EquivalenceClass([1, 0], self.mult2)
      x.check_equivalence_set(x._set)

  # test getter method normally, then adding one element, then another element
  def test_get_normal(self):
    x = EquivalenceClass([1], self.mult2)
    self.assertEquals(x.get_list(), [1])
    
  def test_get_add_one(self):
    x = EquivalenceClass([1], self.mult2)
    x.add(1)
    self.assertEquals(x.get_list(), [1, 1])

  def test_get_add_another(self):
    x = EquivalenceClass([1], self.mult2)
    x.add(1)
    self.assertEquals(x.get_list(), [1, 1])
    x.add(1)
    self.assertEquals(x.get_list(), [1, 1, 1])

if __name__ == "__main__":
  unittest.main()