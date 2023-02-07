from src import train, global_var
from collections import OrderedDict
import argparse



# Options ----------------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument('--method', type=str, default='plain', help="plain fix_lmd dynamic_lmd admm")
# parser.add_argument('--fe_sel', type=int, default=0, help="0--5")
parser.add_argument('--metric', type=str, default='dp', help="dp eop eod")
# parser.add_argument('--model_sel', type=int, default=1, help="VGG-Face, Facenet Facenet512,OpenFace, DeepFace, DeepID, ArcFace, Dlib, SFace")
# parser.add_argument('--e1', type=float, default=0.0)
# parser.add_argument('--e2', type=float, default=0.0)
parser.add_argument('--lmd', type=float, default=0.0)
parser.add_argument('--tol', type=float, default=0.0) # # get an unfair sample wp tol
# parser.add_argument('--train_conf', action='store_true', default=False)
# parser.add_argument('--remove_pos', action='store_true', default=False)
# parser.add_argument('--remove_posOrg', action='store_true', default=False)

parser.add_argument('--mu', type=float, default=1.0)
parser.add_argument('--warm_epoch', type=int, default=0)
parser.add_argument('--sel_layers', type=int, default=2)
parser.add_argument('--strategy', type=int, default=1)
parser.add_argument('--conf', type=str, default='no_conf', help='no_conf, peer, entropy')
parser.add_argument('--label_key', type=str, default='Smiling', help="5_o_Clock_Shadow Arched_Eyebrows Attractive Bags_Under_Eyes Bald Bangs Big_Lips Big_Nose Black_Hair Blond_Hair Blurry Brown_Hair Bushy_Eyebrows Chubby Double_Chin Eyeglasses Goatee Gray_Hair Heavy_Makeup High_Cheekbones Male Mouth_Slightly_Open Mustache Narrow_Eyes No_Beard Oval_Face Pale_Skin Pointy_Nose Receding_Hairline Rosy_Cheeks Sideburns Smiling Straight_Hair Wavy_Hair Wearing_Earrings Wearing_Hat Wearing_Lipstick Wearing_Necklace Wearing_Necktie Young")

parser.add_argument('--label_ratio', type=float, default=0.01)
parser.add_argument('--val_ratio', type=float, default=0.1)

# Example: CUDA_VISIBLE_DEVICES=0 python3 run_celeba.py --method plain  --warm_epoch 0  --metric dp --label_ratio 0.05 --val_ratio 0.1 --strategy 2 



# setup
ROOT = '.'
EXP = 'exps'
RUN = 0
META_MODEL_SEED, META_TRAIN_SEED, SEED_INCR = 42, 4242, 424242
EP_STEPS = 200  # 200
DATA_DIR = '/data2/data'
EXPS_DIR = ROOT + '/exps'

# arguments
# args = SimpleNamespace()
args = parser.parse_args()
# data
args.data_dir = DATA_DIR
args.dataset = 'celeba'

# model
args.model = 'resnet18_lowres' 
# args.model = 'vit-b_8'
args.model_seed = META_MODEL_SEED + RUN * SEED_INCR
# args.load_dir = None
# args.ckpt = 0


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
# args.scheduler = None
args.scheduler = OrderedDict(
    name = "piecewise_constant_schedule",
    config = OrderedDict(
        init_value = args.lr,
        boundaries_and_scales = {10000: 1.0}, # fix lr, no decay
    )
)


# training
args.num_epochs = 10
args.EP_STEPS = EP_STEPS
args.train_seed = META_TRAIN_SEED + RUN * SEED_INCR
args.train_batch_size = 256
# args.train_batch_size = 64
args.test_batch_size = 4096
# args.augment = True
# args.track_forgetting = True
# checkpoints
args.log_steps = EP_STEPS
args.save_steps =  EP_STEPS


# experiment
args.datasize = 202599
args.num_classes = 2
# args.attr_key = "attributes"
# args.feature_key = "image"
args.attr_key = 1
args.feature_key = 0
args.idx_key = 2
# args.label_key = "Smiling" 
# args.label_key = "Attractive" 
args.group_key = "Male"
args.img_size = 32
args.balance_batch = False
args.new_data_each_round = 256 # 1024
# args.sampling_rounds = args.num_epochs * 2

args.train_conf = False
args.remove_pos = True
args.remove_posOrg = False


# method_list = [
#         "Facenet", 
#         "Facenet512", 
#         "OpenFace", 
#         "ArcFace", 
#         "Dlib", 
#         "SFace",
#         ]
# if args.fe_sel == 6:
#     args.feature_extractor = 'None'
# else:
#     args.feature_extractor = method_list[args.fe_sel]
args.save_dir = EXPS_DIR + f'/{EXP}/{args.method}/run_{RUN}_{args.label_key}_warm{args.warm_epoch}_metric_{args.metric}'
if __name__ == "__main__":

    # data conversion for torch loader
    attributes_names = ['5_o_Clock_Shadow', 'Arched_Eyebrows', 'Attractive', 'Bags_Under_Eyes', 'Bald', 'Bangs', 'Big_Lips', 'Big_Nose', 'Black_Hair', 'Blond_Hair', 'Blurry', 'Brown_Hair', 'Bushy_Eyebrows', 'Chubby', 'Double_Chin', 'Eyeglasses', 'Goatee', 'Gray_Hair', 'Heavy_Makeup', 'High_Cheekbones', 'Male', 'Mouth_Slightly_Open', 'Mustache', 'Narrow_Eyes', 'No_Beard', 'Oval_Face', 'Pale_Skin', 'Pointy_Nose', 'Receding_Hairline', 'Rosy_Cheeks', 'Sideburns', 'Smiling', 'Straight_Hair', 'Wavy_Hair', 'Wearing_Earrings', 'Wearing_Hat', 'Wearing_Lipstick', 'Wearing_Necklace', 'Wearing_Necktie', 'Young']
    
    args.group_key = attributes_names.index(args.group_key)
    args.label_key = attributes_names.index(args.label_key)

    if args.model == 'resnet18_lowres':
        args.sel_layers = args.sel_layers
    elif args.model == 'vit-b_8':
        args.sel_layers = -args.sel_layers
    global_var.init()
    global_var.set_value('args', args)
    train(args) # disparity mitigation with our method
