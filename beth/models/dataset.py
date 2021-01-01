"""Inspiration from https://www.kdnuggets.com/2020/07/pytorch-lstm-text-generation-tutorial.html
Used for an experiment to predict next move based on a dataset of moves
"""

import torch
import pandas as pd
from collections import Counter


class Dataset(torch.utils.data.Dataset):
    def __init__(self, data, **kwargs):
        super().__init__()
        self.data = data
        self.words = self.load_words(data)
        self.uniq_words = self.get_uniq_words()

        self.index_to_word = {index: word for index, word in enumerate(self.uniq_words)}
        self.word_to_index = {word: index for index, word in enumerate(self.uniq_words)}

        self.words_indexes = [self.word_to_index[w] for w in self.words]

    def load_words(self, data):
        text = data.str.cat(sep=" ")
        return text.split(" ")

    def get_uniq_words(self):
        word_counts = Counter(self.words)
        return sorted(word_counts, key=word_counts.get, reverse=True)

    def __len__(self):
        return len(self.words_indexes) - self.sequence_length

    def __getitem__(self, index):
        return (
            torch.tensor(self.words_indexes[index : index + self.sequence_length]),
            torch.tensor(
                self.words_indexes[index + 1 : index + self.sequence_length + 1]
            ),
        )
