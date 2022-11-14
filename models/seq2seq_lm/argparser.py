import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_model',default='fnlp/bart-base-chinese',choices=['fnlp/bart-base-chinese','uer/bart-base-chinese-cluecorpussmall','p208p2002/bart-drcd-qg-hl'],type=str)
    parser.add_argument('-d','--dataset',default='drcd',choices=['drcd'],type=str)
    parser.add_argument('--batch_size',type=int,default=10)
    parser.add_argument('--epoch',default=3,type=int)
    parser.add_argument('--lr',type=float,default=3e-5)
    parser.add_argument('--dev',type=int,default=0)
    parser.add_argument('--server',action='store_true')
    parser.add_argument('--run_test',action='store_true')
    parser.add_argument('-fc','--from_checkpoint',type=str,default=None)
    args = parser.parse_args()
        
    return args