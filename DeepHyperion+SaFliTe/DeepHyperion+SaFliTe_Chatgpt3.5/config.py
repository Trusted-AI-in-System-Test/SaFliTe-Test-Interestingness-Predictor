# Make sure that any of this properties can be overridden using env.properties
import os
from os.path import join
import json
import uuid

class MissingEnvironmentVariable(Exception):
    pass

EXEC_DONE        = 0

# GA Setup
POPSIZE          = int(os.getenv('DH_POPSIZE', '30'))
NUM_EXEC          = int(os.getenv('DH_EXEC', '100'))
CASE_STUDY        = str(os.getenv('DH_CASE_STUDY', "case_studies/mission2.yaml"))
NAME = "" #"DeepHyperion"
RUN = "1"

# Mutation Hyperparameters


SELECTIONOP    = str(os.getenv('DH_SELECTIONOP', 'ranked')) # random or ranked or dynamic_ranked
SELECTIONPROB    = float(os.getenv('DH_SELECTIONPROB', '0.5'))
RANK_BIAS    = float(os.getenv('DH_RANK_BIAS', '1.5')) # value between 1 and 2
RANK_BASE    = str(os.getenv('DH_RANK_BASE', 'contribution_score')) # perf or density or contribution_score



#------- NOT TUNING ----------

FEATURES             = os.getenv('FEATURES', ["Distance", "Angle"]) #, "Height"]
NUM_CELLS           = int(os.getenv("NUM_CELLS", '25'))


try:
    THE_HASH = str(os.environ['THE_HASH'])
except Exception:
    THE_HASH = str(uuid.uuid4().hex)
    # print("Generate random Hash", str(THE_HASH))




def to_json(folder):

    config = {
        'name': str(NAME),
        'hash': str(THE_HASH),
        'popsize': str(POPSIZE),
        'num execution': str(NUM_EXEC),
        'run': str(RUN),
        'features': str(FEATURES),
        'ranked prob': str(SELECTIONPROB),
        'rank bias' : str(RANK_BIAS),
        'rank base' : str(RANK_BASE),
        'selection': str(SELECTIONOP),

    }
    filedest = join(folder, "config.json")
    with open(filedest, 'w') as f:
        (json.dump(config, f, sort_keys=True, indent=4))
