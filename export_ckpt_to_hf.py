import argparse
from models.seq2seq_lm.model import Model
import os
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument('--out','-o',help='path to save')
    # parser.add_argument('ckpt_path')
    args = parser.parse_args()

    ModelClass = Model
    
    # assert os.path.isfile(args.ckpt_path)
    lighting_model = ModelClass.load_from_checkpoint(".log_seq2seq_lm/lightning_logs/version_3/checkpoints/last.ckpt")
    lighting_model.model.save_pretrained("hf_model")
    lighting_model.tokenizer.save_pretrained("hf_model")
    print("Done")
