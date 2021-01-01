"""Inspiration from https://www.kdnuggets.com/2020/07/pytorch-lstm-text-generation-tutorial.html
Used for an experiment to predict next move based on a dataset of moves
"""
import torch
import numpy as np
import pandas as pd
from torch import nn, optim
from torch.utils.data import DataLoader
from tqdm.auto import tqdm
from comet_ml import Experiment


class LSTMModel(nn.Module):
    def __init__(
        self,
        dataset,
        lstm_size=128,
        embedding_dim=128,
        num_layers=3,
        dropout=0.2,
        experiment=None,
        **kwargs,
    ):
        super().__init__()
        self.lstm_size = lstm_size
        self.embedding_dim = embedding_dim
        self.num_layers = num_layers
        self.dataset = dataset
        self.dropout = dropout

        n_vocab = len(dataset.uniq_words)
        self.embedding = nn.Embedding(
            num_embeddings=n_vocab,
            embedding_dim=self.embedding_dim,
        )
        self.lstm = nn.LSTM(
            input_size=self.lstm_size,
            hidden_size=self.lstm_size,
            num_layers=self.num_layers,
            dropout=self.dropout,
        )
        self.fc = nn.Linear(self.lstm_size, n_vocab)

    def forward(self, x, prev_state):
        embed = self.embedding(x)
        output, state = self.lstm(embed, prev_state)
        logits = self.fc(output)
        return logits, state

    def save_weights(self, filepath):
        torch.save(self.state_dict(), filepath)

    def load_weights(self, filepath):
        self.load_state_dict(torch.load(filepath))

    def init_state(self, sequence_length):
        return (
            torch.zeros(self.num_layers, sequence_length, self.lstm_size),
            torch.zeros(self.num_layers, sequence_length, self.lstm_size),
        )

    def fit(
        self,
        sequence_length=10,
        batch_size=32,
        max_epochs=100,
        lr=0.001,
        writer=None,
        **kwargs,
    ):

        self.train()

        self.dataset.sequence_length = sequence_length

        try:

            dataloader = DataLoader(self.dataset, batch_size=batch_size)
            criterion = nn.CrossEntropyLoss()
            self.optimizer = optim.Adam(self.parameters(), lr=lr)

            for epoch in range(max_epochs):
                state_h, state_c = self.init_state(self.dataset.sequence_length)

                pbar = tqdm(dataloader, desc=f"Epoch {epoch}")

                for batch, (x, y) in enumerate(pbar):
                    self.optimizer.zero_grad()

                    y_pred, (state_h, state_c) = self(x, (state_h, state_c))
                    loss = criterion(y_pred.transpose(1, 2), y)

                    state_h = state_h.detach()
                    state_c = state_c.detach()

                    loss.backward()
                    self.optimizer.step()

                    loss_value = loss.item()

                    if writer is not None:
                        writer.add_scalar("Loss/train", loss_value, epoch)

                    pbar.set_postfix({"loss": loss_value})

        except KeyboardInterrupt:
            print("... Stopped training in notebook")

    def predict(self, text, next_words=1, as_proba=False):
        self.eval()

        words = text.split(" ")
        state_h, state_c = self.init_state(len(words))
        probas = []

        for i in range(0, next_words):
            x = torch.tensor([[self.dataset.word_to_index[w] for w in words[i:]]])
            y_pred, (state_h, state_c) = self(x, (state_h, state_c))
            last_word_logits = y_pred[0][-1]
            p = torch.nn.functional.softmax(last_word_logits, dim=0).detach().numpy()
            probas.append(p)
            word_index = np.random.choice(len(last_word_logits), p=p)
            words.append(self.dataset.index_to_word[word_index])

        if as_proba:
            probas = pd.DataFrame(probas).T
            probas.index = self.dataset.uniq_words
            return probas
        else:
            return words

    def predict_next(self, game):

        # Get move stack at t and legal moves
        move_stack = " ".join(["start"] + game.get_moves_san())
        legal_moves = game.get_legal_moves_san()

        print(move_stack)
        print(legal_moves)

        # Predict next move probabilities using LSTM
        p = self.predict(move_stack, next_words=1, as_proba=True)[0]

        # Filter probas on legal_moves
        p = p.loc[legal_moves].sort_values(ascending=False)
        p /= p.sum()

        # Sample next move
        selected_move = np.random.choice(p.index, p=p)

        return selected_move
