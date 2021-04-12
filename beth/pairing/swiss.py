"""
# https://en.wikipedia.org/wiki/Swiss-system_tournament
In chess, each player is pitted (paired) against another player with an equivalent performance score. In "Round 1" of a chess tournament paired using the Swiss System, players usually are seeded according to their known playing strength, for example their "chess rating" assigned to them by their local club, their national federation, or the world chess federation (FIDE). In some events, especially when none or few of the players have an official chess rating, the players are paired randomly. Once play begins, players who win receive a point, those who draw receive one-half of a point, and those who lose receive no points. Win, lose or draw, all players proceed to the next round where winners are pitted against opponents with equal performance scores (e.g. Round 1's winners play each other, Round 1's draws play each other, etc.). In later rounds (typical tournaments have anywhere from 3-9 rounds), players face opponents with the same (or almost the same) score. No player is paired up against the same opponent twice.
The rules for Swiss System chess events also try to ensure that each player plays an equal number of games with white and black. Alternating colors in each round is the most preferable and the same color is never repeated three times in a row.
Players with the same score are ideally ranked according to rating. Then the top half is paired with the bottom half. For instance, if there are eight players in a score group, number 1 is paired to play number 5, number 2 is paired to play number 6 and so on. When the tournament, or a section of the tournament, has an odd-number of players, one player usually is assigned a "Bye"—e.g. a round where the player is not paired.  Modifications are then made to balance colors and prevent players from meeting each other twice.[1]
The first national event in the United States to use the Swiss system was in Corpus Christi, Texas in 1945; and the first Chess Olympiad using it was held in Haifa in 1976.[14]
In chess, the terms Swiss and Monrad are both used, and denote systems with different pairing algorithms. The Monrad pairing system is com

5-8 Players = 3 Rounds
9-16 Players = 4 Rounds
17-32 Players = 5 Rounds
33- 64 Players = 6 Rounds
65-128 Players = 7 Rounds
129-212 Players = 8 Rounds
213- 385 Players = 9 Rounds

R = (P + 7 x Q) /5
In which

R is the number of rounds,
P is the number of participants, and
Q is the number of qualified places 


Todo
- Use score and not elo when pairing for rounds 2+
- Keep track of players having skipped a round
- Display elo or score gap for rounds
"""

import pandas as pd
import numpy as np
from sklearn.cluster import MeanShift
from sklearn.neighbors import NearestNeighbors


ROUNDS_COLS = ["round", "player1", "player2", "color", "result"]


class SwissTournament:
    def __init__(self, players=None, path: str = None):
        """Swiss Tournament matcher

        Args:
            players (list of dict, optional): List of players as dict with keys "name" and "elo". Defaults to None.
            path (str, optional): Path for excel file to be reloaded. Defaults to None.
        """

        if path is not None:
            self.load(path)
        else:
            self._players = pd.DataFrame(players, columns=["name", "elo"]).set_index("name")
            self._rounds = pd.DataFrame(columns=ROUNDS_COLS)

        duplicated_players = self.players.index[self.players.index.duplicated()].tolist()
        if len(duplicated_players) > 0:
            raise Exception(f"Players {duplicated_players} are duplicated in the player list, remove them to use the pairing system")

        print(f"[INFO] Swiss tournament with {len(self.players)} players - current round : {self.current_round}")

    def save(self, path: str) -> None:
        """Save tournament status in excel file
        Helps to be reloaded later

        Args:
            path (str): Excel path for the checkpoint
        """
        writer = pd.ExcelWriter(path, engine="xlsxwriter")
        self.players.reset_index().to_excel(writer, index=False, sheet_name="Players")
        self.rounds.to_excel(writer, index=False, sheet_name="Rounds")
        writer.close()

    def load(self, path: str) -> None:
        """Reload tournament status from excel file

        Args:
            path (str): Excel path for the checkpoint
        """
        self._players = pd.read_excel(path, sheet_name="Players").set_index("name")
        self._rounds = pd.read_excel(path, sheet_name="Rounds")

    @property
    def players(self) -> pd.DataFrame:
        """Property returning the players in the tournament

        Returns:
            pd.DataFrame: Description of players (name and ELO)
        """
        return self._players

    @property
    def rounds(self) -> pd.DataFrame:
        """Property returning the played rounds in the tournament

        Returns:
            pd.DataFrame: Status of game played and to be played
        """

        return self._rounds

    @property
    def current_round(self) -> int:
        """Returns current round

        Returns:
            int: The round number being played
        """

        if len(self.rounds) == 0:
            return 1
        else:
            if not self.is_current_round_finished:
                return self.rounds["round"].max()
            else:
                return self.rounds["round"].max() + 1

    @property
    def is_current_round_finished(self) -> bool:
        """Returns True if current round played is finished
        Looks for null values in the self.rounds dataframe

        Returns:
            bool: True if current round is finished
        """
        if len(self.rounds) == 0:
            return False
        else:
            return self.rounds.loc[self.rounds["round"] == self.rounds["round"].max()]["result"].isnull().sum() == 0

    @property
    def is_odd(self) -> bool:
        """Returns True if we have an odd number of players

        Returns:
            bool: True if number of players is odd
        """
        return len(self.players) % 2 != 0

    def get_rounds_with_scores(self) -> pd.DataFrame:
        """Helper function to see rounds with associated scores and ELO

        Returns:
            pd.DataFrame: Rounds with each players scores and ELOs
        """
        scores = self.compute_players_scores().reset_index()
        return (
            self.rounds.merge(
                scores.rename(columns={"name": "player1", "elo": "elo1", "score": "score1"}),
                on="player1",
                how="left",
            )
            .merge(
                scores.rename(columns={"name": "player2", "elo": "elo2", "score": "score2"}),
                on="player2",
                how="left",
            )
            .assign(diff_elo=lambda x: x["elo1"] - x["elo2"])
            .assign(diff_score=lambda x: x["score1"] - x["score2"])
        )

    @property
    def n_players(self):
        return len(self.players)

    @property
    def players_names(self):
        return self.players.index.tolist()

    @property
    def rounds_matrix(self):

        # Prepare matrix to be filled
        matrix = pd.DataFrame(index=self.players_names, columns=self.players_names)

        # Pivot the round table as matrix and transpose to get opposite views
        win_rounds = self.rounds.pivot(index="player1", columns="player2", values="result")
        lost_rounds = 1 - win_rounds.T

        # Update with both views
        matrix.update(win_rounds)
        matrix.update(lost_rounds)

        # Add odd player results
        odd_players = self.get_odd_players()
        odd_players_rounds = {x: {x: 1} for x in odd_players}
        matrix.update(odd_players_rounds)

        return matrix

    def pair(self, overwrite: bool = False, random_result: bool = False, trials: int = 10, n_neighbors: int = 3) -> pd.DataFrame:
        """Pair players together for a given round
        The pairing algorithm is simple greedy implementation + Nearest Neighbors :
            - If odd number of players remove randomly one player from the pairing round
            - Shuffle the remaining players
            - For each player (iterative approach), find players not played in previous rounds (or the odd player for the round)
            - Among those selected player, use Nearest Neighbors algorithms to find the closest n_neighbors players in ELO (first round) or score (next rounds)
            - Select randomly from those n_neighbors found
            - If over the rounds, matches are not found, retries matching algorithm until you find a combination that works
            - Appends the paired players in self.rounds and returns only this round data

        Args:
            overwrite (bool, optional): Overwrites current round if already started otherwise raises Exception. Defaults to False.
            random_result (bool, optional): To debug purposes, you may want to try random results. Defaults to False.
            trials (int, optional): Number of times to retry if matches are not found. Defaults to 10.
            n_neighbors (int, optional): Number of neighbors on ELO or score to consider for each pairing attempt. Defaults to 3.

        Returns:
            pd.DataFrame: Paired players in a DataFrame (also appended to self.rounds)
        """

        if self.current_round > self.n_players:
            raise Exception(f"You cannot play more rounds ({self.current_round}) than the number of players ({self.n_players})")

        i = 0
        retry = True

        while retry:
            pairs = []
            paired_players = []

            if self.is_odd:
                odd_player = self.get_random_odd_player()
                paired_players.append(odd_player)
            else:
                odd_player = None

            players_names = self.shuffle_players_list()
            players_data = self.compute_players_scores()

            try:
                for player in players_names:

                    if player not in paired_players:

                        paired_player = self.pair_player(player, data=players_data, avoid=paired_players, n=n_neighbors)
                        pair = (player, paired_player)

                        pairs.append(pair)
                        paired_players.extend(pair)

                retry = False
            except Exception as e:
                print(f"[INFO] Failed to find suitable pairs at trial {i}, matching again ...")
                if i == trials:
                    retry = False
                else:
                    i += 1

        # Save pairs in self.rounds
        current_round = self.current_round
        round_data = [
            {
                "round": current_round,
                "player1": player1,
                "player2": player2,
                "color": None,
                "result": None if not random_result else np.random.choice([1.0, 0.5, 0.0]),
            }
            for player1, player2 in pairs
        ]
        if odd_player is not None:
            round_data.append(
                {
                    "round": current_round,
                    "player1": odd_player,
                    "player2": None,
                    "color": None,
                    "result": 1,
                }
            )

        round_data = pd.DataFrame(round_data, columns=ROUNDS_COLS)

        existing_round_data = self.rounds.loc[self.rounds["round"] == current_round]
        if len(existing_round_data) > 0:
            if overwrite:
                print(f"[INFO] Overwriting round {current_round} data")
                self._rounds = self._rounds.drop(existing_round_data.index)
            else:
                raise Exception(f"You already have data for round {current_round} which is not finished")

        self._rounds = self._rounds.append(round_data, ignore_index=True)

        return round_data

    def pair_player(self, player, data=None, avoid=None, n=3):

        if data is None:
            data = self.compute_players_scores()

        score = "elo" if self.current_round == 1 else "score"

        # Get score
        score_value = data.loc[player, score]

        # Find players who never played against the given players
        never_played = self.get_never_played(player)

        # Also avoid players already paired with others in the round or the solo player
        if avoid is not None:
            never_played = [x for x in never_played if x not in avoid]

        # Get players data that could be paired
        never_played_players = data.loc[never_played]

        # Find possible players to be paired using nearest neighbor algorithm
        # The algorithm will find n possible matches on the given score
        # If not enough players we just take the last possible values

        if len(never_played_players) <= n:
            possible_pairs = never_played_players.index.tolist()
        else:
            nn = NearestNeighbors(n_neighbors=n)
            nn.fit(never_played_players[[score]])
            _, ind = nn.kneighbors([[score_value]])
            possible_pairs = never_played_players.iloc[np.squeeze(ind)].index.tolist()

        # Randomly select one of the possible matches
        try:
            paired_player = np.random.choice(possible_pairs)
        except Exception as e:
            raise Exception(f"Cannot choose a paired player for '{player}' from {possible_pairs}.\nNever played players:{never_played_players.index.tolist()}\nOriginal error : {e}")

        return paired_player

    def get_never_played(self, against):
        never_played = self.rounds_matrix.loc[[against]].T.drop(against)
        never_played = never_played.loc[never_played[against].isnull()].index.tolist()
        return never_played

    def get_random_player(self):
        return np.random.choice(self.players_names)

    def get_random_odd_player(self):
        odd_players = self.get_odd_players()
        players = [x for x in self.players_names if x not in odd_players]
        return np.random.choice(players)

    def get_odd_players(self):

        current_round = self.current_round
        n_players = self.n_players

        odd_players = self.rounds.assign(cycle=lambda x: x["round"].map(lambda y: (y - 1) // n_players == (current_round - 1) // n_players)).query("cycle")
        return odd_players.loc[odd_players["player2"].isnull()]["player1"].tolist()

    def compute_players_scores(self):
        scores = self.rounds_matrix.sum(axis=1).fillna(0.0)
        scores.name = "score"
        return self.players.join(scores)

    def shuffle_players_list(self):
        players = self.players_names
        np.random.shuffle(players)
        return players

    def add_result(self, player1, player2, result, round=0, color="WHITE"):
        assert player1 in self.players_names
        assert player2 in self.players_names
        df = pd.DataFrame([[round, player1, player2, color, result]], columns=ROUNDS_COLS)
        self.rounds = self.rounds.append(df, ignore_index=True)

    def group_players(self, on="elo", col="group", eps=150, even_groups=True):

        # Group players on metric column (score or elo) using MeanShift clustering
        ms = MeanShift(bandwidth=eps)
        clusters = ms.fit_predict(self.players[[on]])
        self.players[col] = clusters

        # Reorder cluster to be ascendant on the given metric
        reorder = self.players.groupby("group", as_index=False)[on].mean().sort_values(on)
        reorder["new_group"] = range(len(reorder))
        reorder = reorder.set_index("group")["new_group"].to_dict()
        self.players["group"] = self.players["group"].replace(reorder)

        # Sort players
        self.players = self.players.sort_values(on).reset_index(drop=True)

        # Reorder groups to make each group even + 1 extra people if odd
        # This will facilitate pairing in the next phase
        if even_groups:

            # If total number of players is odd
            # Take one random player that won't play in the round
            # Affects his group number to 1
            if len(self.players) % 2 != 0:
                alone_player_index = np.random.randint(0, len(self.players))
                self.players.loc[alone_player_index, "group"] = -1

            # Iterate for each group
            for group in self.players["group"].unique():

                # Group number positive avoid selecting odd player that won't player in the round
                if group >= 0:

                    # Select all players in a group
                    players_group = self.players.loc[self.players["group"] == group]

                    # If odd group of players, bump best player in the next group
                    if len(players_group) % 2 != 0:
                        player_bumped_index = players_group.index[-1]
                        self.players.loc[player_bumped_index, "group"] += 1
