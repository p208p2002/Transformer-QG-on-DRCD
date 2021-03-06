from flask import Flask,Response
import json
from flask import request
from utils import MaskedLMGenerator
from loguru import logger

class ServerMixin():
    def run_server(self,max_context_length = 400,max_question_length=32,port=5000):
        if self._type == 'seq2seq_lm':
            max_decode_length = max_question_length
        elif self._type in ['causal_lm','masked_lm']:
            max_context_length = max_context_length + max_question_length
            max_decode_length = max_context_length
        else:
            assert False,'_type match fail'

        self.flask = Flask(__name__)
        # add route
        @self.flask.route('/')
        def index():
            return jsonify(self.hparams)
        
        @self.flask.route('/',methods=['post'])
        def predict():
            context = request.form['context']
            # logger.debug(context)
            model_input = self.tokenizer(context,max_length=max_context_length,truncation=True,return_tensors='pt',add_special_tokens=False)

            if self._type in ['seq2seq_lm','causal_lm']:
                sample_outputs = self.model.generate(
                    input_ids = model_input['input_ids'],
                    attention_mask = model_input['attention_mask'],
                    max_length=max_decode_length,
                    early_stopping=True,
                    temperature=0.85,
                    do_sample=True,
                    top_p=0.9,
                    top_k=10,
                    num_beams=3,
                    no_repeat_ngram_size=5,
                    num_return_sequences=1,
                    eos_token_id=102
                )
                sample_output = sample_outputs[0]
                if self._type in ['causal_lm']:
                    input_ids_len = model_input['input_ids'].shape[-1]
                    sample_output = sample_output[input_ids_len:]
                decode_question = self.tokenizer.decode(sample_output, skip_special_tokens=True)
                decode_question = decode_question.replace(" ","")
                # logger.debug(decode_question)
                return Response(json.dumps({"predict":decode_question},ensure_ascii=False),content_type="application/json; charset=utf-8" )

        self.flask.run(port=port)
