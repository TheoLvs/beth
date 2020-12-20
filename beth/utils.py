import os
from dotenv import load_dotenv
from comet_ml import Experiment

def make_experiment(env_file,name = None,tags = None):

    # Get environment values
    load_dotenv(env_file)
    COMETML_KEY = os.environ.get("COMETML_KEY")
    COMETML_PROJECT = os.environ.get("COMETML_PROJECT")

    # Start and configure experiment
    experiment = Experiment(COMETML_KEY,COMETML_PROJECT)

    if name is not None:
        experiment.set_name(name)
    if tags is not None:
        experiment.add_tags(tags)

    return experiment