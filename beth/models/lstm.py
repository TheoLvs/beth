"""Inspiration from https://www.kdnuggets.com/2020/07/pytorch-lstm-text-generation-tutorial.html
Used for an experiment to predict next move based on a dataset of moves
"""
import torch
import numpy as np
from torch import nn, optim
from torch.utils.data import DataLoader
from tqdm.auto import tqdm


class LSTMModel(nn.Module):
    def __init__(self, dataset,lstm_size = 128,embedding_dim = 128,num_layers = 3):
        super().__init__()
        self.lstm_size = lstm_size
        self.embedding_dim = embedding_dim
        self.num_layers = num_layers

        n_vocab = len(dataset.uniq_words)
        self.embedding = nn.Embedding(
            num_embeddings=n_vocab,
            embedding_dim=self.embedding_dim,
        )
        self.lstm = nn.LSTM(
            input_size=self.lstm_size,
            hidden_size=self.lstm_size,
            num_layers=self.num_layers,
            dropout=0.2,
        )
        self.fc = nn.Linear(self.lstm_size, n_vocab)

    def forward(self, x, prev_state):
        embed = self.embedding(x)
        output, state = self.lstm(embed, prev_state)
        logits = self.fc(output)
        return logits, state

    def init_state(self,sequence_length):
        return (torch.zeros(self.num_layers, sequence_length, self.lstm_size),
                torch.zeros(self.num_layers, sequence_length, self.lstm_size))


    def fit(self,dataset,batch_size = 32,max_epochs = 100,lr = 0.001,writer = None):

        self.train()

        dataloader = DataLoader(dataset, batch_size=batch_size)
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.parameters(), lr=lr)

        for epoch in range(max_epochs):
            state_h, state_c = self.init_state(dataset.sequence_length)

            pbar = tqdm(dataloader,desc=f"Epoch {epoch}")

            for batch, (x, y) in enumerate(pbar):
                optimizer.zero_grad()

                y_pred, (state_h, state_c) = self(x, (state_h, state_c))
                loss = criterion(y_pred.transpose(1, 2), y)

                state_h = state_h.detach()
                state_c = state_c.detach()

                loss.backward()
                optimizer.step()


                loss_value = loss.item()

                if writer is not None:
                    writer.add_scalar("Loss/train", loss_value, epoch)

                pbar.set_postfix({'loss': loss_value })


    def predict(self,dataset, text, next_words=100):
        self.eval()

        words = text.split(' ')
        state_h, state_c = self.init_state(len(words))

        for i in range(0, next_words):
            x = torch.tensor([[dataset.word_to_index[w] for w in words[i:]]])
            y_pred, (state_h, state_c) = self(x, (state_h, state_c))

            last_word_logits = y_pred[0][-1]
            p = torch.nn.functional.softmax(last_word_logits, dim=0).detach().numpy()
            word_index = np.random.choice(len(last_word_logits), p=p)
            words.append(dataset.index_to_word[word_index])

        return words