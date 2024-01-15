# config.py

class Config:
    """
    Configuration settings for the application.
    """

    def __init__(self):
        # Default configuration values
        self.cohen = 0.35              # Small effect size
        self.file = "../data/diabetes.csv"  # Default CSV data file name
        self.help = False              # Show help
        self.k = 1                     # Low class frequency kludge
        self.m = 2                     # Low attribute frequency kludge
        self.seed = 31210              # Random number seed
        self.todo = "help"             # Start up action

    def __str__(self):
        return f"""Configurations:
    Cohen: {self.cohen}
    File: {self.file}
    Help: {self.help}
    K: {self.k}
    M: {self.m}
    Seed: {self.seed}
    Todo: {self.todo}
    """

# Usage example
if __name__ == "__main__":
    config = Config()
    print(config)

