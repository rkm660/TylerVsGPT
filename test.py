import itertools
import openai
import json
import re

# Risk tolerance setting
RISK_TOLERANCE = "high_risk"  # Options: "low_risk", "medium_risk", "high_risk"
openai.api_key = "key"


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

    def prompt(self, a, b):
        """Formats the prompt correctly with stock tickers."""
        return f"""You are an expert stock picker. Based on everything you have access to, which is the better stock to own for the next 3-5 years for three investor profiles: low, medium, and high risk? 
        {a} or {b}? 
        Return a "matrix" object with 3 subobjects "low_risk", "medium_risk", and "high_risk", each containing: 
        - "winning_stock_ticker" 
        - "losing_stock_ticker" 
        - "investment_thesis" (an in-depth comparative analysis of why the stock wins for that risk profile).
        """

    def play(self):
        """Plays a round between two stocks by calling OpenAI API."""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert stock analyst."},
                {"role": "user", "content": self.prompt(self.stock_a.ticker, self.stock_b.ticker)}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        # Extract and clean response content
        try:
            raw_content = response["choices"][0]["message"]["content"]
            cleaned_json_string = re.sub(r"```json\n|\n```", "", raw_content).strip()
            result = json.loads(cleaned_json_string)  # Convert to Python dictionary

            # Determine winner and loser based on risk tolerance
            if self.stock_a.ticker == result[RISK_TOLERANCE]["winning_stock_ticker"]:
                winner, loser = self.stock_a, self.stock_b
            else:
                winner, loser = self.stock_b, self.stock_a

            print(winner, loser)
            winner.record_win()  # Increment the winner's score

        except (KeyError, json.JSONDecodeError) as e:
            print(f"Error parsing response from OpenAI API: {e}. Skipping match.")


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
    tickers = ["AAPL", "MDB", "GOOG", "AMZN", "AFRM", "XYZ", "NVDA", "SOFI"]
    tournament = Tournament(tickers)
    tournament.run_tournament()
    tournament.display_results()
