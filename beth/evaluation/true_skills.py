raise NotImplementedError()


class Rating:
    def __init__(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma

    @property
    def variance(self):
        return self.sigma ** 2

    def __repr__(self):
        return f"Player({self.mu}+-{self.sigma})"


def reverse_sigmoid(x, alpha=1):
    return 1 - 1 / (1 + np.exp(-x / alpha))


class Matchup:
    def __init__(self, winner, loser, beta=4, alpha=2):

        self.winner = winner
        self.loser = loser
        self.beta = beta
        self.alpha = alpha

    def make_c(self):
        return np.sqrt(2 * self.beta ** 2 + self.winner.variance + self.loser.variance)

    def V(self, x):
        #         return norm.pdf(x)/norm.cdf(x)
        return reverse_sigmoid(x, alpha=self.alpha)

    def W(self, x):
        V = self.V(x)
        return V * (V + x)

    def update(self):

        c = self.make_c()
        t = (self.winner.mu - self.loser.mu) / c

        print(t)

        mu_winner = self.winner.mu + self.winner.variance / c * self.V(t)
        mu_loser = self.loser.mu - self.loser.variance / c * self.V(t)
        print(self.winner.mu, mu_winner)

        variance_winner = self.winner.variance * (1 - (self.winner.variance / c ** 2) * self.W(t))
        variance_loser = self.loser.variance * (1 - (self.loser.variance / c ** 2) * self.W(t))

        winner = Rating(mu_winner, np.sqrt(variance_winner))
        loser = Rating(mu_loser, np.sqrt(variance_loser))
        return winner, loser
