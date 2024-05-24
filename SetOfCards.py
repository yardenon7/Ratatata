class SetOfCards:
  """A class to represent a set of cards."""

  def __init__(self, cards):
    """Initializes the set of cards with a list of card numbers.

    Args:
        cards: A list of card numbers.
    """
    self.cards = cards

  def __str__(self):
    return str(self.cards)

  def get_cards(self):
    """Returns the list of card numbers."""
    return self.cards

  def set_a_card(self, i, value):
    self.cards[i] = value

  def get_a_specific_card(self, i):
    return self.cards[i]

