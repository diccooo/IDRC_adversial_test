from pdtb2 import CorpusReader
import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('func', type=str)
parser.add_argument('splitting', type=int)

selected_sense = set([
    'Temporal.Asynchronous', 'Temporal.Synchrony', 'Contingency.Cause',
    'Contingency.Pragmatic cause', 'Comparison.Contrast', 'Comparison.Concession',
    'Expansion.Conjunction', 'Expansion.Instantiation', 'Expansion.Restatement',
    'Expansion.Alternative','Expansion.List'
])

def arg_filter(arg):
    res = []
    for w in arg:
        if w.find('*') < 0:
            res.append(w)
    return res

def preprocess(splitting):
    # 1 for Lin and 2 for Ji
    if splitting == 1:
        train_sec = [
            '02', '03', '04', '05', '06', '07', '08', '09', '10', '11',
            '12', '13', '14', '15', '16', '17', '18', '19', '20', '21',
        ]
        dev_sec = ['22']
        test_sec = ['23']
    elif splitting == 2:
        train_sec = [
            '02', '03', '04', '05', '06', '07', '08', '09', '10', '11',
            '12', '13', '14', '15', '16', '17', '18', '19', '20',
        ]
        dev_sec = ['00', '01']
        test_sec = ['21', '22']
    else:
        raise Exception('wrong splitting')

    arg1_train = []
    arg2_train = []
    conn_train = []
    sense_train = []
    arg1_dev = []
    arg2_dev = []
    conn_dev = []
    sense1_dev = []
    sense2_dev = []
    arg1_test = []
    arg2_test = []
    conn_test = []
    sense1_test = []
    sense2_test = []

    for corpus in CorpusReader('./raw/pdtb2.csv').iter_data():
        if corpus.Relation != 'Implicit':
            continue
        sense_split = corpus.ConnHeadSemClass1.split('.')
        sense_l2 = '.'.join(sense_split[0:2])
        if sense_l2 in selected_sense:
            arg1 = arg_filter(corpus.arg1_words())
            arg2 = arg_filter(corpus.arg2_words())
            if corpus.Section in train_sec:
                arg1_train.append(arg1)
                arg2_train.append(arg2)
                conn_train.append(corpus.Conn1.split())
                sense_train.append([sense_l2, sense_split[0]])
            elif corpus.Section in dev_sec:
                arg1_dev.append(arg1)
                arg2_dev.append(arg2)
                conn_dev.append(corpus.Conn1.split())
                sense1_dev.append([sense_l2, sense_split[0]])
            elif corpus.Section in test_sec:
                arg1_test.append(arg1)
                arg2_test.append(arg2)
                conn_test.append(corpus.Conn1.split())
                sense1_test.append([sense_l2, sense_split[0]])
            else:
                continue
            if corpus.Conn2 is not None:
                sense_split = corpus.Conn2SemClass1.split('.')
                sense_l2 = '.'.join(sense_split[0:2])
                if sense_l2 in selected_sense:
                    if corpus.Section in train_sec:
                        arg1_train.append(arg1)
                        arg2_train.append(arg2)
                        conn_train.append(corpus.Conn2.split())
                        sense_train.append([sense_l2, sense_split[0]])
                    elif corpus.Section in dev_sec:
                        sense2_dev.append([sense_l2, sense_split[0]])
                    elif corpus.Section in test_sec:
                        sense2_test.append([sense_l2, sense_split[0]])
            else:
                if corpus.Section in dev_sec:
                    sense2_dev.append([None, None])
                elif corpus.Section in test_sec:
                    sense2_test.append([None, None])
    
    assert len(arg1_train) == len(arg2_train) == len(conn_train) == len(sense_train)
    assert len(arg1_dev) == len(arg2_dev) == len(conn_dev) == len(sense1_dev) == len(sense2_dev)
    assert len(arg1_test) == len(arg2_test) == len(conn_test) == len(sense1_test) == len(sense2_test)
    print('train size:', len(arg1_train))
    print('dev size:', len(arg1_dev))
    print('test size:', len(arg1_test))

    if splitting == 1:
        pre = './interim/lin/'
    elif splitting == 2:
        pre = './interim/ji/'
    with open(pre + 'train.pkl', 'wb') as f:
        pickle.dump(arg1_train, f)
        pickle.dump(arg2_train, f)
        pickle.dump(conn_train, f)
        pickle.dump(sense_train, f)
    with open(pre + 'dev.pkl', 'wb') as f:
        pickle.dump(arg1_dev, f)
        pickle.dump(arg2_dev, f)
        pickle.dump(conn_dev, f)
        pickle.dump(sense1_dev, f)
        pickle.dump(sense2_dev, f)
    with open(pre + 'test.pkl', 'wb') as f:
        pickle.dump(arg1_test, f)
        pickle.dump(arg2_test, f)
        pickle.dump(conn_test, f)
        pickle.dump(sense1_test, f)
        pickle.dump(sense2_test, f)

def test(splitting):
    if splitting == 1:
        pre = './interim/lin/'
    elif splitting == 2:
        pre = './interim/ji/'
    with open(pre + 'train.pkl', 'rb') as f:
        arg1_train = pickle.load(f)
        arg2_train = pickle.load(f)
        conn_train = pickle.load(f)
        sense_train = pickle.load(f)
    with open(pre + 'dev.pkl', 'rb') as f:
        arg1_dev = pickle.load(f)
        arg2_dev = pickle.load(f)
        conn_dev = pickle.load(f)
        sense1_dev = pickle.load(f)
        sense2_dev = pickle.load(f)
    with open(pre + 'test.pkl', 'rb') as f:
        arg1_test = pickle.load(f)
        arg2_test = pickle.load(f)
        conn_test = pickle.load(f)
        sense1_test = pickle.load(f)
        sense2_test = pickle.load(f)

    assert len(arg1_train) == len(arg2_train) == len(conn_train) == len(sense_train)
    assert len(arg1_dev) == len(arg2_dev) == len(conn_dev) == len(sense1_dev) == len(sense2_dev)
    assert len(arg1_test) == len(arg2_test) == len(conn_test) == len(sense1_test) == len(sense2_test)
    print('train size:', len(arg1_train))
    print(arg1_train[0:5])
    print(arg2_train[0:5])
    print(conn_train[0:5])
    print(sense_train[0:5])
    print('dev size:', len(arg1_dev))
    print(arg1_dev[0:5])
    print(arg2_dev[0:5])
    print(conn_dev[0:5])
    print(sense1_dev[0:5])
    print(sense2_dev[0:5])
    print('test size:', len(arg1_test))
    print(arg1_test[0:5])
    print(arg2_test[0:5])
    print(conn_test[0:5])
    print(sense1_test[0:5])
    print(sense2_test[0:5])

if __name__ == '__main__':
    A = parser.parse_args()
    if A.func == 'pre':
        if A.splitting == 1:
            preprocess(1)
        elif A.splitting == 2:
            preprocess(2)
    elif A.func == 'test':
        if A.splitting == 1:
            test(1)
        elif A.splitting == 2:
            test(2)
