import numpy as np
import pandas as pd
import time
from copy import deepcopy

from ..move import Move


class TreeNode:
    def __init__(self, board, move=None, stack=None, best_score=0, start_time=None, max_time=None):

        # Prepare attributes
        # In particular copy the board to reproduce and propagate the node
        self.board = deepcopy(board)
        self.move = move
        self.best_score = best_score
        self.score = 0
        self.color = "WHITE" if self.board.turn else "BLACK"
        self.pruned = False
        self.max_time = max_time

        # Early stopping condition
        if self.max_time is not None:
            current_time = time.time()

            if start_time is None:
                self.start_time = time.time()
            else:
                self.start_time = start_time

            if current_time - self.start_time > self.max_time:
                self.pruned = True

        # If a move is provided, push to the copied board
        if move is not None:
            self.board.push(move.move)
            self.score = self.move.score

        # Recursivity attributes
        # Previous moves will be stacked for each node to traverse backward
        if stack is None:
            self.stack = []
        else:
            self.stack = stack

        # Prepare to stack children nodes
        self.children = []

        # Get all the legal moves
        # Important to compute the legal moves after having pushed the move
        # The parser needs te right context of the board
        self.legal_moves = list(self.board.legal_moves)

    def has_children(self):
        return len(self.legal_moves) > 0

    def is_white_turn(self):
        # Help to determine who is the maximizing player
        return self.board.turn

    def is_pruned(self):
        return self.pruned

    def prune(self):
        self.pruned = True

    def __repr__(self):
        if len(self.stack) == 0:
            moves_stack = "..."
        else:
            moves_stack = "-".join([str(x) for x in self.stack])
        return f"{self.color.title()}Node({moves_stack},best_score={self.best_score},score={self.score})"

    def discount_rewards(self, rewards, gamma=1):
        return np.round(np.multiply(gamma ** np.arange(len(rewards)), np.array(rewards)), 2)

    def next_moves(self):

        # Get all the legal moves
        moves = self.legal_moves

        # Parse each move, in particular to get the score
        moves = [Move(m, self.board) for m in moves]

        # We sort by score the moves given the color
        # Indeed self.board.turn = True if it's white turn for example,
        # Then we want a descending order to get the best moves
        moves = sorted(moves, key=lambda x: x.score, reverse=self.board.turn)
        return moves

    def next_nodes(self, sample_moves=None):

        # Parse and analyse each possible move
        moves = self.next_moves()

        # Select randomly among possible moves
        if sample_moves is not None:
            moves = sample_moves(moves)

        # For each move, recursively explore the following moves
        children = []
        for move in moves:
            child_tree = TreeNode(
                self.board,
                move,
                stack=self.stack + [move],
                best_score=self.best_score + move.score,
                start_time=self.start_time,
                max_time=self.max_time,
            )
            children.append(child_tree)
        return children

    def expand(self, depth=5, pruning=True, sample_moves=None):

        # If we reached the final node
        # Because there is no children leaves or because we reach maximum exploration depth
        # If we prune the node, we stop expanding it and we keep the score at this node
        if depth == 0 or not self.has_children() or self.is_pruned():

            # We save the best score at the final node as the final value
            self.best_score = self.score
            self.trace_score = [self.score]

            # Also parsing the move stack to backtrace the moves
            names, scores, moves = zip(*[(x.move_str, x.score, x) for x in self.stack])
            stack = [
                {
                    "names": names,
                    "scores": scores,
                    "total": np.sum(scores),
                }
            ]

            # Return best score and move stack
            return self.score, stack

        # If we did not reach the final node
        else:

            # We initialize a move stack to store and backtrace the moves
            # We also initialize the placeholder for node_children after the recursive function call
            # Finally we initialize the best node for each step (nodes can be equally good of course)
            stacks = []
            node_children = []
            best_child = None

            # Compute the children nodes using helper function on legal moves
            children = self.next_nodes(sample_moves)

            # Initialize the score to beat in the minimax algorithm
            score = -np.inf if self.is_white_turn() else np.inf

            # Iterating over each possible moves
            for child in children:

                # Alpha beta Pruning function
                if pruning:
                    if self.is_white_turn():
                        if child.score < score:
                            child.prune()
                    else:
                        if child.score > score:
                            child.prune()

                # We recursively expand (depth-first search) the child node
                # - child_score is the score after expansion
                # - child.score is the natural score of the node
                child_score, stack = child.expand(depth - 1, pruning, sample_moves)

                # Core Minimax algorithm
                if self.is_white_turn():

                    # If the child has a better score (for white we maximize)
                    # We keep this node and its score as the score to beat
                    if child_score > score:
                        score = child_score
                        best_child = child
                else:

                    # Same thing in reverse for black
                    if child_score < score:
                        score = child_score
                        best_child = child

                # We save the traversed children and the move stack
                stacks.extend(stack)
                node_children.append(child)

            # Finally for a given node we keep track of the best scores (in total and the decomposition in the tree)
            # And we conclude the recursive loop by returning again the best core and move stack
            self.best_score = self.score + best_child.best_score
            self.trace_score = [self.score, *best_child.trace_score]
            self.children = node_children
            return self.best_score, stacks
