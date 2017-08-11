import torch

class Config(object):
    corpus_splitting = 1            # 1 for Lin and 2 for Ji
    max_sent_len = 80

    wordvec_path = '~/Projects/GoogleNews-vectors-negative300.bin.gz'
    wordvec_dim = 300

    nonlinear = torch.nn.Tanh()

    sent_repr_dim = 256
    conv_filter_set_num = 3
    conv_kernel_size = [2, 4, 8]

    arg_rep_dim = sent_repr_dim * conv_filter_set_num * 2
    arg_encoder_fc_num = 1
    arg_encoder_fc_dim = 512
    arg_encoder_dropout = 0.4
    
    pair_rep_dim = arg_encoder_fc_dim if arg_encoder_fc_num > 0 else arg_rep_dim

    clf_fc_num = 1
    clf_fc_dim = 512
    clf_class_num = 11
    clf_dropout = 0.4
    
    discr_fc_dim = 1024
    discr_dropout = 0.1


    i2sense = [
        'Temporal.Asynchronous', 'Temporal.Synchrony', 'Contingency.Cause',
        'Contingency.Pragmatic cause', 'Comparison.Contrast', 'Comparison.Concession',
        'Expansion.Conjunction', 'Expansion.Instantiation', 'Expansion.Restatement',
        'Expansion.Alternative','Expansion.List'
    ]
    sense2i = {
        'Temporal.Asynchronous':0, 'Temporal.Synchrony':1, 'Contingency.Cause':2,
        'Contingency.Pragmatic cause':3, 'Comparison.Contrast':4, 'Comparison.Concession':5,
        'Expansion.Conjunction':6, 'Expansion.Instantiation':7, 'Expansion.Restatement':8,
        'Expansion.Alternative':9,'Expansion.List':10
    }
    i2senseclass = ['Temporal', 'Contingency', 'Comparison', 'Expansion']
    senseclass2i = {'Temporal':0, 'Contingency':1, 'Comparison':2, 'Expansion':3}