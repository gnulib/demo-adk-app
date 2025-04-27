import requests

class DeckOfCardsClient:
    """
    Python REST client for the Deck of Cards API.
    API Docs: https://deckofcardsapi.com/
    """

    BASE_URL = "https://deckofcardsapi.com/api/deck"

    def __init__(self, session=None):
        self.session = session or requests.Session()

    def shuffle_new_deck(self, deck_count=None, jokers_enabled=None, cards=None):
        """
        Shuffle a new deck (optionally partial, with jokers, or multiple decks).

        Args:
            deck_count (int, optional): Number of decks to use.
            jokers_enabled (bool, optional): Whether to include jokers.
            cards (str, optional): Comma-separated card codes for a partial deck.

        Returns:
            dict: JSON response from the API.
        """
        params = {}
        if deck_count is not None:
            params['deck_count'] = deck_count
        if jokers_enabled is not None:
            params['jokers_enabled'] = 'true' if jokers_enabled else 'false'
        if cards is not None:
            params['cards'] = cards
        url = f"{self.BASE_URL}/new/shuffle/"
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def draw_cards(self, deck_id, count=None):
        """
        Draw cards from a deck.

        Args:
            deck_id (str): The deck ID or "new".
            count (int, optional): Number of cards to draw.

        Returns:
            dict: JSON response from the API.
        """
        params = {}
        if count is not None:
            params['count'] = count
        url = f"{self.BASE_URL}/{deck_id}/draw/"
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def reshuffle_deck(self, deck_id, remaining=None):
        """
        Reshuffle an existing deck.

        Args:
            deck_id (str): The deck ID.
            remaining (bool, optional): Shuffle only remaining cards.

        Returns:
            dict: JSON response from the API.
        """
        params = {}
        if remaining is not None:
            params['remaining'] = 'true' if remaining else 'false'
        url = f"{self.BASE_URL}/{deck_id}/shuffle/"
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def new_unshuffled_deck(self, deck_count=None, jokers_enabled=None, cards=None):
        """
        Create a new, unshuffled deck.

        Args:
            deck_count (int, optional): Number of decks to use.
            jokers_enabled (bool, optional): Whether to include jokers.
            cards (str, optional): Comma-separated card codes for a partial deck.

        Returns:
            dict: JSON response from the API.
        """
        params = {}
        if deck_count is not None:
            params['deck_count'] = deck_count
        if jokers_enabled is not None:
            params['jokers_enabled'] = 'true' if jokers_enabled else 'false'
        if cards is not None:
            params['cards'] = cards
        url = f"{self.BASE_URL}/new/"
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def add_to_pile(self, deck_id, pile_name, cards):
        """
        Add drawn cards to a named pile.

        Args:
            deck_id (str): The deck ID.
            pile_name (str): Name of the pile.
            cards (str): Comma-separated card codes to add.

        Returns:
            dict: JSON response from the API.
        """
        params = {'cards': cards}
        url = f"{self.BASE_URL}/{deck_id}/pile/{pile_name}/add/"
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def list_pile(self, deck_id, pile_name):
        """
        List cards in a named pile.

        Args:
            deck_id (str): The deck ID.
            pile_name (str): Name of the pile.

        Returns:
            dict: JSON response from the API.
        """
        url = f"{self.BASE_URL}/{deck_id}/pile/{pile_name}/list/"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def draw_from_pile(self, deck_id, pile_name, count=None, cards=None):
        """
        Draw cards from a named pile.

        Args:
            deck_id (str): The deck ID.
            pile_name (str): Name of the pile.
            count (int, optional): Number of cards to draw.
            cards (str, optional): Comma-separated card codes to draw.

        Returns:
            dict: JSON response from the API.
        """
        params = {}
        if count is not None:
            params['count'] = count
        if cards is not None:
            params['cards'] = cards
        url = f"{self.BASE_URL}/{deck_id}/pile/{pile_name}/draw/"
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def return_cards(self, deck_id, cards=None):
        """
        Return cards from hand to the main deck.

        Args:
            deck_id (str): The deck ID.
            cards (str, optional): Comma-separated card codes to return.

        Returns:
            dict: JSON response from the API.
        """
        params = {}
        if cards is not None:
            params['cards'] = cards
        url = f"{self.BASE_URL}/{deck_id}/return/"
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def return_cards_to_pile(self, deck_id, pile_name, cards=None):
        """
        Return cards from a pile to the main deck.

        Args:
            deck_id (str): The deck ID.
            pile_name (str): Name of the pile.
            cards (str, optional): Comma-separated card codes to return.

        Returns:
            dict: JSON response from the API.
        """
        params = {}
        if cards is not None:
            params['cards'] = cards
        url = f"{self.BASE_URL}/{deck_id}/pile/{pile_name}/return/"
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()


# Global instance of DeckOfCardsClient
deck_client = DeckOfCardsClient()


def shuffle_new_deck(deck_count, jokers_enabled, cards):
    """
    Shuffle a new deck (optionally partial, with jokers, or multiple decks).

    Args:
        deck_count (int): Number of decks to use.
        jokers_enabled (bool): Whether to include jokers.
        cards (str): Comma-separated card codes for a partial deck.

    Returns:
        dict: JSON response from the API.
    """
    return deck_client.shuffle_new_deck(deck_count, jokers_enabled, cards)


def draw_cards(deck_id, count):
    """
    Draw cards from a deck.

    Args:
        deck_id (str): The deck ID or "new".
        count (int): Number of cards to draw.

    Returns:
        dict: JSON response from the API.
    """
    return deck_client.draw_cards(deck_id, count)


def reshuffle_deck(deck_id, remaining):
    """
    Reshuffle an existing deck.

    Args:
        deck_id (str): The deck ID.
        remaining (bool): Shuffle only remaining cards.

    Returns:
        dict: JSON response from the API.
    """
    return deck_client.reshuffle_deck(deck_id, remaining)


def new_unshuffled_deck(deck_count, jokers_enabled, cards):
    """
    Create a new, unshuffled deck.

    Args:
        deck_count (int): Number of decks to use.
        jokers_enabled (bool): Whether to include jokers.
        cards (str): Comma-separated card codes for a partial deck.

    Returns:
        dict: JSON response from the API.
    """
    return deck_client.new_unshuffled_deck(deck_count, jokers_enabled, cards)


def add_to_pile(deck_id, pile_name, cards):
    """
    Add drawn cards to a named pile.

    Args:
        deck_id (str): The deck ID.
        pile_name (str): Name of the pile.
        cards (str): Comma-separated card codes to add.

    Returns:
        dict: JSON response from the API.
    """
    return deck_client.add_to_pile(deck_id, pile_name, cards)


def list_pile(deck_id, pile_name):
    """
    List cards in a named pile.

    Args:
        deck_id (str): The deck ID.
        pile_name (str): Name of the pile.

    Returns:
        dict: JSON response from the API.
    """
    return deck_client.list_pile(deck_id, pile_name)


def draw_from_pile(deck_id, pile_name, count, cards):
    """
    Draw cards from a named pile.

    Args:
        deck_id (str): The deck ID.
        pile_name (str): Name of the pile.
        count (int): Number of cards to draw.
        cards (str): Comma-separated card codes to draw.

    Returns:
        dict: JSON response from the API.
    """
    return deck_client.draw_from_pile(deck_id, pile_name, count, cards)


def return_cards(deck_id, cards):
    """
    Return cards from hand to the main deck.

    Args:
        deck_id (str): The deck ID.
        cards (str): Comma-separated card codes to return.

    Returns:
        dict: JSON response from the API.
    """
    return deck_client.return_cards(deck_id, cards)


def return_cards_to_pile(deck_id, pile_name, cards):
    """
    Return cards from a pile to the main deck.

    Args:
        deck_id (str): The deck ID.
        pile_name (str): Name of the pile.
        cards (str): Comma-separated card codes to return.

    Returns:
        dict: JSON response from the API.
    """
    return deck_client.return_cards_to_pile(deck_id, pile_name, cards)
