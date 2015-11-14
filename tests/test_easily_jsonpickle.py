# Testing tools
import nose
from nose.tools import *

# SUT
from easily_jsonpickle import *

# Aux
import json
import jsonpickle

# DEBUG
import pdb

# Prepare "class infrastructure"
@easily_to_json("to_json", "from_json", ["name", "children"])
class A:
  def to_json(self, d):
    pass
  @classmethod
  def from_json(cls, d):
    a = cls()
    a.name = d["name"]
    a.children = jsonpickle.decode(json.dumps(d["children"]))
    return a

class B:
  pass

# Actual tests
def test_encode_decode():
  a = A();
  a.name = "dontcare";
  a.children = ["hello", "bye"];
  json_str = jsonpickle.encode(a)
  a_decoded = jsonpickle.decode(json_str)
  assert_equal(a_decoded.children, ["hello", "bye"])

def test_creates_references():
  # Remove SkipTest once reference handling is made easier and thus implemented
  # in the above classes.
  raise nose.SkipTest()
  a = A()
  a1 = A()
  a2 = A()
  b = B()
  a.name = "a"
  a1.name = "a1"
  a2.name = "a2"
  b.name = "b"
  a.children = [a1,a2]
  a1.children = [b]
  a2.children= []
  b.children = [a2]
  json_str = jsonpickle.encode(a)
  # Idea here: If it can't do references, then it will have a new copy of the
  # "a2" object in three different places. Otherwise, there will just be one.
  assert_equal(json_str.count("a2"), 1)
