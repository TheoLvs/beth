# beth
![](https://images.chesscomfiles.com/uploads/v1/article/22924.4e040c11.668x375o.d12a4478e7d3@2x.jpeg)
Experimenting with Game AI applied to chess


## Installation
``beth`` is available on PyPi - https://pypi.org/project/beth/, you can simply it using 
```
pip install beth 
``` 

## Idea
In this repo will be experiments around AI & chess. In particular Machine Learning applied to the chess game. <br>
The goal is to create: 

- Algorithms to play chess using Machine Learning, Reinforcement Learning & NLP
- Auto-guide to help human learn and improve at playing chess
- Adaptive AI to match the player ELO and make him improve

> This repo is **under active development**


## Features
### Environment

- [x] Experimenting with the [python chess](https://python-chess.readthedocs.io/en) library
- [x] Implementing ``Game`` framework
- [x] ``HumanPlayer`` to play chess in Jupyter notebook
- [x] ``RandomPlayer`` the most simple bot to easily test out new ideas and debug
- [ ] Read PGN files and load into ML algorithms
- [ ] Measure ELO of an algorithm/AI, or any consistant metric of performance
- [ ] Saving game as gif or video

### Model utils
- [x] Monitor algorithm performance using Comet.ml / tensorboard
- [x] Saving algorithm weights to be reused
- [x] Visualize probabilities to see best moves and if training worked
- [ ] Transform game object into 3D tensor (2D dimension + one hot encoding of pieces positions)
- [ ] Install, test, and integrate CodeCarbon
- [ ] Train on Google Colab

### Algorithms & approaches
- [ ] AlphaGo approach: value function and policy function evaluation using Reinforcement Learning & MCTS
- [ ] AlphaZero approach: self play competition
- [ ] NLP approach: predicting next move using NLP techniques (LSTM, Transformers)
  - [ ] LSTM / RNN / GRU
  - [ ] Transformers
  - [ ] Directly using Hugging Face ``transformers`` [library](https://huggingface.co/transformers/task_summary.html) 
- [ ] Hybrid techniques with both NLP-like + modeling the game as 3D tensor 
- [ ] GameAI techniques (minimax, rules-based)
  - [ ] Super simple approach where at each step Random Play from a PGN file or list of moves. 
- [ ] Test connection to Game engines like stockfish

## References
- https://python-chess.readthedocs.io/en
- https://lichess.org/
- https://www.chess.com/games/

### Sequential Deep Learning
- https://pytorch.org/tutorials/beginner/transformer_tutorial.html

### Game Databases
- https://www.chess.com/games/
- https://www.kaggle.com/datasnaek/chess

### State of the art approaches
- https://ai.facebook.com/blog/rebel-a-general-game-playing-ai-bot-that-excels-at-poker-and-more/
  

### Libraries
- Deep Learning ``jax, trax, rlax, haiku and pytorch-lightning``
- Monitoring (comet.ml, [livelossplot](https://github.com/stared/livelossplot), [tensorboard](https://pytorch.org/tutorials/recipes/recipes/tensorboard_with_pytorch.html))


