from src import train, train_compas, global_var
from src.fair_train import fair_train_validation
from collections import OrderedDict
import argparse



# Options ----------------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument('--method', type=str, default='plain', help="plain fix_lmd dynamic_lmd")
parser.add_argument('--model', type=str, default='mlp', help="mlp")
parser.add_argument('--metric', type=str, default='dp', help="dp eop eod")
parser.add_argument('--lmd', type=float, default=0.0)
parser.add_argument('--tol', type=float, default=0.0) # # get an unfair sample wp tol

parser.add_argument('--mu', type=float, default=1.0)
parser.add_argument('--warm_epoch', type=int, default=0)
parser.add_argument('--sel_layers', type=int, default=4)
parser.add_argument('--strategy', type=int, default=1)
parser.add_argument('--conf', type=str, default='no_conf', help='no_conf, peer, entropy')
parser.add_argument('--aux_data', type=str, default=None, help="imagenet")

parser.add_argument('--exp', type=int, default=1)

parser.add_argument('--label_ratio', type=float, default=0.01)
parser.add_argument('--val_ratio', type=float, default=0.1)
# parser.add_argument('--label_budget', type=int, default=1024)
parser.add_argument('--runs', type=int, default=0)
parser.add_argument('--epoch', type=int, default=50)

#new add arguments for testing
parser.add_argument('--new_prob', type=float, default=0.9) 
parser.add_argument('--ratio_org', type=float, default=0.5) 
parser.add_argument('--train_with_validation', type=bool, default=False) 
parser.add_argument('--save_model', default=False, action="store_true") # save the model


# arguments
args = parser.parse_args()

# setup
ROOT = '.'
EXP = 'exps'
RUN = args.runs
META_MODEL_SEED, META_TRAIN_SEED, SEED_INCR = 42, 4242, 424242
EP_STEPS = 200  
DATA_DIR = '/data2/data'
EXPS_DIR = ROOT + '/exps'


# data
args.data_dir = DATA_DIR
args.dataset = 'compas'

# model
args.model_seed = META_MODEL_SEED + RUN * SEED_INCR

# optimizer
args.lr = 0.01
args.momentum = 0.9
args.weight_decay = 0.0005
args.nesterov = True
# SGD
args.opt = OrderedDict(
    name="sgd",
    config=OrderedDict(
        learning_rate = args.lr,
        momentum = args.momentum,
        nesterov = args.nesterov
    )
)
args.scheduler = None



# training
args.num_epochs = args.epoch +  args.warm_epoch

args.EP_STEPS = EP_STEPS
args.train_seed = META_TRAIN_SEED + RUN * SEED_INCR
args.train_batch_size = 256
args.test_batch_size = 4096

# checkpoints
args.log_steps = EP_STEPS
args.save_steps =  EP_STEPS


# experiment
args.num_classes = 2
args.balance_batch = False
args.new_data_each_round = 128 


args.train_conf = False
args.remove_pos = True
args.remove_posOrg = False


args.save_dir = EXPS_DIR + f'/{EXP}/{args.method}/{args.dataset}/run_{RUN}_metric_{args.metric}'

if __name__ == "__main__":


    if 'mlp' in args.model:
        args.sel_layers = -args.sel_layers
    global_var.init()
    global_var.set_value('args', args)
    
    train_compas(args)
    
    ###using validation data to train for analysis
    args.train_with_validation = False
    if args.train_with_validation:
        args.method='dynamic_lmd'
        args.warm_step=0
        args.epoch=50
        args.warm_epoch = 0
        args.log_steps = 10
        args.train_batch_size = 16

        args.num_epochs = args.epoch +  args.warm_epoch
        fair_train_validation(args)
