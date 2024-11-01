from src import train, train_jigsaw, global_var
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


parser.add_argument('--label_ratio', type=float, default=0.1)
parser.add_argument('--val_ratio', type=float, default=0.2)
parser.add_argument('--label_budget', type=int, default=1024)
parser.add_argument('--runs', type=int, default=0)
parser.add_argument('--epoch', type=int, default=10)

#new add arguments for testing
parser.add_argument('--new_prob', type=float, default=0.5) 
parser.add_argument('--ratio_org', type=float, default=0.5) 

parser.add_argument('--save_model', default=False, action="store_true") # save the model

# Example: CUDA_VISIBLE_DEVICES=0 python3 run_celeba.py --method plain  --warm_epoch 0  --metric dp --label_ratio 0.05 --val_ratio 0.1 --strategy 2 


# arguments
args = parser.parse_args()

# setup
ROOT = '.'
EXP = 'exps'
RUN = args.runs
META_MODEL_SEED, META_TRAIN_SEED, SEED_INCR = 42, 4242, 424242
EP_STEPS = 1000  
DATA_DIR = '/data2/data'
EXPS_DIR = ROOT + '/exps'


# data
args.data_dir = DATA_DIR
args.dataset = 'jigsaw'

# model
args.model_seed = META_MODEL_SEED + RUN * SEED_INCR


# optimizer
args.lr = 0.0001
args.momentum = 0.9
args.weight_decay = 0.0005
args.nesterov = True

args.opt = OrderedDict(
    name="adam",
    config=OrderedDict(
        learning_rate = args.lr,
        # momentum = args.momentum,
        # nesterov = args.nesterov
    )
)
args.scheduler = None

# training
# default setting for analyzing the impact of label budget
args.num_epochs = args.epoch +  args.warm_epoch



args.EP_STEPS = EP_STEPS
args.train_seed = META_TRAIN_SEED + RUN * SEED_INCR
args.train_batch_size = 64
args.test_batch_size = 4096
# checkpoints
args.log_steps = EP_STEPS
args.save_steps =  EP_STEPS


# experiment
# args.datasize = 202599
args.num_classes = 2
args.balance_batch = False

args.new_data_each_round = args.label_budget

args.train_conf = False
args.remove_pos = True
args.remove_posOrg = False


args.save_dir = EXPS_DIR + f'/{EXP}/{args.method}/run_{RUN}_warm{args.warm_epoch}_metric_{args.metric}'




if __name__ == "__main__":

    global_var.init()
    global_var.set_value('args', args)
    train_jigsaw(args)

