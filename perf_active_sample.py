import numpy as np
import collections
import pandas
result_dict = collections.defaultdict(list)


# root = './logs/fair_sampling/vit/'
# root = './logs/fair_sampling/res18/'

root = './logs/fair_sampling/compas/'


def get_result(file_name):
    avg_cnt = 3
    if 'vit' in root:
        remove = 0
    else:
        remove = 0
    with open(root+file_name+'.log') as file:
        test_list = []
        val_list = []
        warm_list = []
        idx_test, idx_val = -remove, -remove
        for line in file.readlines():
            if 'test' in line:
                line_ = line.strip('\n').split('|')
                acc = float(line_[-2].strip(' ').split(' ')[2])
                fair = float(line_[-1].strip(' ').split(' ')[3])
                test_list.append((acc, fair, idx_test))
                idx_test += 1
            elif 'val' in line:
                line_ = line.strip('\n').split('|')
                acc = float(line_[-2].strip(' ').split(' ')[2])
                fair = float(line_[-1].strip(' ').split(' ')[3])
                val_list.append((acc, fair, idx_val))
                idx_val += 1
            elif 'warm' in line:
                line_ = line.strip('\n').split('|')
                acc = float(line_[-2].strip(' ').split(' ')[2])
                fair = float(line_[-1].strip(' ').split(' ')[3])
                warm_list.append((acc, fair, idx_val))


    base_perf = warm_list[-avg_cnt:]
    test_list = test_list[remove:]
    val_list = val_list[remove:]
    if len(test_list) == len(val_list):
        # select top k by acc and fair, respectively
        k = avg_cnt
        acc_val = sorted(val_list, key=lambda x: x[0])[::-1]
        fair_val = sorted(val_list, key=lambda x: x[1])
        
        # print(acc_val)
        # print(fair_val)
        # get average
        acc_avg_sel_by_fair_val = np.mean([test_list[i[2]][0] for i in fair_val[:k]])
        fair_avg_sel_by_fair_val = np.mean([test_list[i[2]][1] for i in fair_val[:k]])
        acc_avg_sel_by_acc_val = np.mean([test_list[i[2]][0] for i in acc_val[:k]])
        fair_avg_sel_by_acc_val = np.mean([test_list[i[2]][1] for i in acc_val[:k]])

        # save result as a dict
        # result_dict[file_name] = [(acc_avg_sel_by_acc_val, fair_avg_sel_by_acc_val), (acc_avg_sel_by_fair_val, fair_avg_sel_by_fair_val)] # [acc_focused, fair_focused]     
        result_dict[file_name] = [f'({acc_avg_sel_by_acc_val:.3f}, {fair_avg_sel_by_acc_val:.3f})', f'({acc_avg_sel_by_fair_val:.3f}, {fair_avg_sel_by_fair_val:.3f})'] # [acc_focused, fair_focused, fair_and_better_than_base_acc]          
    else:
        raise RuntimeError('test_list has a different length from val_list')

def print_result(result, file_path):
    df = pandas.DataFrame(result)
    print(df)
    df.to_csv(file_path, index=False)
    print(f'result is saved to {file_path}')


def get_table(focus):
    if focus == 'acc':
        sel = 0
    else:
        sel = 1
    result = []
    for stg in strategy:
        for layer in sel_layers:
            # if stg == 1 and layer == 4:
            #     break
            rec = []
            for label in label_key:
                for metric in metrics:
                    file_name = f'{label}_s{stg}_{metric}_{layer}'
                    if 'res18' in root:
                        file_name = 'res18_' + file_name
                    rec.append(result_dict[file_name][sel]) # acc_focused: 0, fairness focused: 1
            result.append(rec)
    # print(result)
    file_path = f'result_{focus}_focused.csv'
    print_result(result, file_path)

def get_table_new(focus):
    sel = 0
    # if focus == 'acc':
    #     sel = 0
    # else:
    #     sel = 1
    result = []
    for stg in strategy:
        for layer in sel_layers:
            if stg == 1 and layer == 4:
                break
            rec = []
            for label in label_key:
                for metric in metrics:
                    file_name = f'{label}_s{stg}_{metric}_{layer}'
                    if 'res18' in root:
                        file_name = 'res18_' + file_name
                    rec.append(result_dict[file_name][sel]) # acc_focused: 0, fairness focused: 1
            result.append(rec)
    # print(result)
    file_path = f'result_{focus}_focused.csv'
    print_result(result, file_path)

sel_layers = [4]
strategy = [1, 2, 5]
if 'vit' in root:
    label_key = ['Smiling', 'Straight_Hair', 'Attractive', 'Pale_Skin', 'Young', 'Big_Nose']
else:
    label_key = ['label']
metrics = ['dp', 'eop', 'eod']

# read logs, then save the processed results to dict
for layer in sel_layers:
    for stg in strategy:
        for label in label_key:
            for metric in metrics:
                # if stg == 1:
                #     file_name = f'{label}_s{stg}_{metric}_2'
                # else:
                file_name = f'{label}_s{stg}_{metric}_{layer}'
                if 'res18' in root:
                    file_name = 'res18_' + file_name
                get_result(file_name)
        
# get table
get_table(focus = 'acc')
get_table(focus = 'fairness')
# print(result_dict)

