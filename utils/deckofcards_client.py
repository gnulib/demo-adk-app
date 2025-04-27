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
        """
        params = {'cards': cards}
        url = f"{self.BASE_URL}/{deck_id}/pile/{pile_name}/add/"
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def list_pile(self, deck_id, pile_name):
        """
        List cards in a named pile.
        """
        url = f"{self.BASE_URL}/{deck_id}/pile/{pile_name}/list/"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def draw_from_pile(self, deck_id, pile_name, count=None, cards=None):
        """
        Draw cards from a named pile.
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
        """
        params = {}
        if cards is not None:
            params['cards'] = cards
        url = f"{self.BASE_URL}/{deck_id}/pile/{pile_name}/return/"
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()
