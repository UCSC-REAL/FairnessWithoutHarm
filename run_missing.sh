# # --------- baseline ------------
# CUDA_VISIBLE_DEVICES=4 nohup python3 run_celeba_fair_learn.py --method dynamic_lmd  --lmd 0.0 --mu 1.0  --warm_epoch -1 --conf entropy  --metric dp --label_ratio 0.02 --val_ratio 0.1 --strategy 1 --sel_round $SR > ./logs/fair_train/s1_dp_02_new256_100round_sel_$SR\_case1_random_sel.log &

sel_round="5"

SR='5'
CUDA_VISIBLE_DEVICES=0 nohup python3 run_celeba_fair_learn.py --method dynamic_lmd  --lmd 0.0 --mu 1.0  --warm_epoch -1 --conf entropy  --metric dp --label_ratio 0.02 --val_ratio 0.1 --strategy 4 --sel_round $SR  > ./logs/fair_train/s4_dp_02_new256_100round_sel_$SR\_case1_remove_unfair.log &



CUDA_VISIBLE_DEVICES=0 nohup python3 run_celeba_fair_learn.py --method dynamic_lmd  --lmd 0.0 --mu 1.0  --warm_epoch -1 --conf entropy  --metric dp --label_ratio 0.02 --val_ratio 0.1 --strategy 4 --sel_round $SR --remove_pos > ./logs/fair_train/s4_dp_02_new256_100round_sel_$SR\_case1_remove_unfair_posloss.log &

sleep 1h

CUDA_VISIBLE_DEVICES=0 nohup python3 run_celeba_fair_learn.py --method dynamic_lmd  --lmd 0.0 --mu 1.0  --warm_epoch -1 --conf entropy  --metric dp --label_ratio 0.02 --val_ratio 0.1 --strategy 5 --sel_round $SR --remove_pos > ./logs/fair_train/s5_dp_02_new256_100round_sel_$SR\_case1_remove_unfair_posloss.log &


SR='10'

CUDA_VISIBLE_DEVICES=0 nohup python3 run_celeba_fair_learn.py --method dynamic_lmd  --lmd 0.0 --mu 1.0  --warm_epoch -1 --conf entropy  --metric dp --label_ratio 0.02 --val_ratio 0.1 --strategy 4 --sel_round $SR  > ./logs/fair_train/s4_dp_02_new256_100round_sel_$SR\_case1_remove_unfair.log &

sleep 1h

CUDA_VISIBLE_DEVICES=0 nohup python3 run_celeba_fair_learn.py --method dynamic_lmd  --lmd 0.0 --mu 1.0  --warm_epoch -1 --conf entropy  --metric dp --label_ratio 0.02 --val_ratio 0.1 --strategy 5 --sel_round $SR  > ./logs/fair_train/s5_dp_02_new256_100round_sel_$SR\_case1_remove_unfair.log &

CUDA_VISIBLE_DEVICES=0 nohup python3 run_celeba_fair_learn.py --method dynamic_lmd  --lmd 0.0 --mu 1.0  --warm_epoch -1 --conf entropy  --metric dp --label_ratio 0.02 --val_ratio 0.1 --strategy 4 --sel_round $SR --remove_pos > ./logs/fair_train/s4_dp_02_new256_100round_sel_$SR\_case1_remove_unfair_posloss.log &

sleep 1h

CUDA_VISIBLE_DEVICES=0 nohup python3 run_celeba_fair_learn.py --method dynamic_lmd  --lmd 0.0 --mu 1.0  --warm_epoch -1 --conf entropy  --metric dp --label_ratio 0.02 --val_ratio 0.1 --strategy 5 --sel_round $SR --remove_pos > ./logs/fair_train/s5_dp_02_new256_100round_sel_$SR\_case1_remove_unfair_posloss.log &

 