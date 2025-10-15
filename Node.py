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


# --------------------------------------------------------------
def alphabeta(node, alpha=-np.inf, beta=np.inf, depth=1):
  # verifica se é a vez do MAX ou do MIN, max começa com o humano
  if depth % 2 == 1:
    agent = "MAX"
  else:
    agent = "MIN"


  if node.is_terminal():
    return node.get_utility()
  
  elif agent == "MAX":
    return max_value_ab(node, alpha, beta, depth) #chama recursivamente
  else:
    return min_value_ab(node, alpha, beta, depth)
  
def max_value_ab(node, alpha, beta, depth):
  value  = -np.inf 
  #pega cada filho do nó
  for child in node.get_children():
    # a funcão compara todos os nós filhos e pega o maior valor
    value = max(value, alphabeta(child, alpha, beta, depth+1))
    #poda beta
    if value >= beta: 
      #se o valor for maior ou igual vale a pena subir pois pode alterar o estado da árvore
      return value
    alpha = max(alpha, value)
  return value

#explicação do max vale pro min
def min_value_ab(node, alpha, beta, depth):
  value  = np.inf
  for child in node.get_children():
    value = min(value, alphabeta(child, alpha, beta, depth+1))
    #poda alpha
    if value <= alpha:
      return value
    beta = min(beta, value)
  return value


# --------------------------------------------------------------
def ordered_alphabeta(node, alpha=-np.inf, beta=np.inf, depth=1):
  # verifica se é a vez do MAX ou do MIN, max começa com o humano
  if depth % 2 == 1:
    agent = "MAX"
  else:
    agent = "MIN"


  if node.is_terminal():
    return node.get_utility()
  
  elif agent == "MAX":
    return max_value_ordered_ab(node, alpha, beta, depth) #chama recursivamente
  else:
    return min_value_ordered_ab(node, alpha, beta, depth)
  
def max_value_ordered_ab(node, alpha, beta, depth):
  value  = -np.inf 
  #pega cada filho do nó
  children = node.get_children()
  #ordena os filhos em ordem decrescente
  children.sort(key=lambda x: x.get_utility() if x.is_terminal() else 0, reverse=True)
  
  for child in children:
    # a funcão compara todos os nós filhos e pega o maior valor
    value = max(value, ordered_alphabeta(child, alpha, beta, depth+1))
    #poda beta
    if value >= beta: 
      #se o valor for maior ou igual vale a pena subir pois pode alterar o estado da árvore
      return value
    alpha = max(alpha, value)
  return value

#explicação do max vale pro min
def min_value_ordered_ab(node, alpha, beta, depth):
  value  = np.inf
  children = node.get_children()
  #ordena os filhos em ordem crescente
  children.sort(key=lambda x: x.get_utility() if x.is_terminal() else 0)
  
  for child in children:
    value = min(value, ordered_alphabeta(child, alpha, beta, depth+1))
    #poda alpha
    if value <= alpha:
      return value
    beta = min(beta, value)
  return value