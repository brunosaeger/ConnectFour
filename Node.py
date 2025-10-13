import numpy as np

"""
  Classe Node, é um vértice que possui um valor de utilidade
  e uma lista com a indicação de quem são os filhos
"""
class Node:
  def __init__(self, utility=None):
    self.utility = utility
    self.children = []

  def add_child(self, child):
    self.children.append(child)

  def is_terminal(self):
    return self.utility is not None

  def get_children(self):
    return self.children

  def get_utility(self):
    return self.utility


def minimax(node, depth=1):
  # Quando o jogo começa (depth=1), a primeira jogada sempre será MAX
  if depth % 2 == 1:
    agent = "MAX"
  else:
    agent = "MIN"

  if node.is_terminal():
    return node.get_utility()
  elif agent == "MAX":
    return max_value(node, depth)
  else:
    return min_value(node, depth)

def max_value(node, depth):
  value  = -np.inf
  for child in node.get_children():
    value = max(value, minimax(child, depth+1))
  return value

def min_value(node, depth):
  value  = np.inf
  for child in node.get_children():
    value = min(value, minimax(child, depth+1))
  return value