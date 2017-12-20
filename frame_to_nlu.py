# transform frames data sets to nlu

import json
import baidu_translator

def get_result(path):
    with open(path) as f:
        data_set = json.load(f)
    # s = set()
    result = []
    act_list = []

    # for count
    count = 0    # the number of total turns
    slot_set = set()
    act_set = set()

    for i in range(len(data_set)):  # len(data_set)
        episode_data = data_set[i]
        for j in range(len(episode_data['turns'])):
            turn_data = episode_data['turns'][j]
            if turn_data['author'] == 'user':    # user turn
                count += 1
                nl_en = turn_data['text']
                labels = turn_data['labels']['acts_without_refs']
                nl_ch = baidu_translator.baidu_translator(nl_en)
                turn_result = {}
                cur_s = set()
                for k in range(len(labels)):
                    act = labels[k]['name']
                    slot = labels[k]['args']   # slot = [{"val": "Atlantis","key": "dst_city"},{"val": "1700","key": "budget"}]
                    for q in range(len(slot)):
                        tup = (act, slot[q]['key'], baidu_translator.baidu_translator(str(slot[q]['val'])))
                        cur_s.add(tup)
                        act_set.add(tup[0])
                        slot_set.add(tup[1])
                        del tup
                for k in cur_s:
                    act_list.append(k)
                turn_result['nl_en'] = nl_en
                turn_result['nl_ch'] = nl_ch
                turn_result['label_seq'], flag_no_match = get_label(nl_en, nl_ch, cur_s)
                turn_result['act'] = act_list
                if flag_no_match == 0:
                    result.append(turn_result)
        print('episode ', i, 'completed!!')
    # print('total:', count, '\t', 'usable:', len(result), '\t')
    # print('act_set:', act_set)
    # print('slot_set:', slot_set)
    # print('slot_num:', len(slot_set))
    return result

def get_label(nl_en, nl_ch, s):
    seq = ['O']*len(nl_ch)
    flag_no_match = 0
    for tup in s:
        if tup[2] != None:
            ref = tup[2]
        else:
            ref = baidu_translator.baidu_translator(tup[1])
            # continue
        start_index = nl_ch.find(ref)
        end_index = start_index + len(ref)
        if start_index == -1:
            print('Not find in chinese sequence!!!')
            flag_no_match = 1
            # path = './no_match_all/no_match_'+tup[0]+'_'+tup[1]
            # with open(path, 'a') as f:
            #     f.write(nl_en+'\n')
            #     f.write(nl_ch+'\n')
            #     f.write(ref+' '+str(tup)+'\n')
            #     f.write('---------------------------------\n')
            # with open('./no_match_all/no_match', 'a') as f:
            #     f.write(nl_en+'\n')
            #     f.write(nl_ch+'\n')
            #     f.write(ref+' '+str(tup)+'\n')
            #     f.write('---------------------------------\n')
        else:
            seq[start_index] = 'B-'+tup[1]
            seq[start_index+1:end_index] = ['I-'+tup[1]]*(len(ref)-1)
    seq_out = str()
    for i in range(len(seq)):
        seq_out = seq_out + seq[i] + ' '
    return seq_out, flag_no_match


if __name__ == '__main__':
    file_path = 'frames.json'
    s = get_result(file_path)
    print(len(s))
    with open('data_for_nlu.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(s, ensure_ascii=False))
    for i in range(len(s)):
        seq_in = s[i]['nl_ch']
        seq = ''
        for j in range(len(seq_in)):
            seq += seq_in[j] + ' '
        seq_out = s[i]['label_seq']
        with open('seq.in', 'a', encoding='utf-8') as f:
            f.write(seq+'\n')
        with open('seq.out', 'a', encoding='utf-8') as f:
            f.write(seq_out+'\n')