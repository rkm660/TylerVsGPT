import itertools

class Stock:
    """
    Represents a stock in the ranking system.
    Each stock tracks its win count.
    """
    def __init__(self, ticker):
        self.ticker = ticker
        self.wins = 0  # Number of wins
    
    def record_win(self):
        """Increments the win count."""
        self.wins += 1

    def __repr__(self):
        """Returns a string representation of the stock's ranking."""
        return f"{self.ticker} (Wins: {self.wins})"

class Game:
    """
    Simulates a match between two stocks.
    """
    def __init__(self, stock_a, stock_b):
        self.stock_a = stock_a
        self.stock_b = stock_b
    
    def play(self):
        """
        Determines the winner deterministically.
        The winner is chosen by alphabetical order (placeholder logic).
        """
        if self.stock_a.ticker < self.stock_b.ticker:
            winner, loser = self.stock_a, self.stock_b
        else:
            winner, loser = self.stock_b, self.stock_a

        winner.record_win()  # Only the winner gets a win count

class Tournament:
    """
    Runs a deterministic round-robin tournament where every stock plays against every other stock exactly once.
    """
    def __init__(self, tickers):
        self.stocks = {ticker: Stock(ticker) for ticker in tickers}
        self.matchups = list(itertools.combinations(self.stocks.values(), 2))
        self.rounds_played = 0

    def run_tournament(self):
        """
        Runs a full round-robin tournament, ensuring every stock plays against every other stock once.
        """
        for stock_a, stock_b in self.matchups:
            game = Game(stock_a, stock_b)
            game.play()
            self.rounds_played += 1

    def display_results(self):
        """
        Displays the final rankings after all matches have been played.
        Stocks are ranked by total wins.
        """
        sorted_stocks = sorted(self.stocks.values(), key=lambda s: s.wins, reverse=True)
        print(f"Tournament completed in {self.rounds_played} rounds")
        for stock in sorted_stocks:
            print(stock)

if __name__ == "__main__":
    tickers = ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "META", "NVDA", "NFLX"]
    tournament = Tournament(tickers)
    tournament.run_tournament()
    tournament.display_results()
