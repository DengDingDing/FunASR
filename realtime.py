from funasr import AutoModel

chunk_size = [0, 10, 5] #[0, 10, 5] 600ms, [0, 8, 4] 480ms
encoder_chunk_look_back = 4 #number of chunks to lookback for encoder self-attention
decoder_chunk_look_back = 1 #number of encoder chunks to lookback for decoder cross-attention

model = AutoModel(model="paraformer-zh-streaming")

import soundfile
import os

# wav_file = os.path.join(model.model_path, "example/asr_example.wav")
wav_file = 'aaa_16k_mono.wav'
speech, sample_rate = soundfile.read(wav_file)
chunk_stride = chunk_size[1] * 960 # 600ms

cache = {}
total_chunk_num = int(len((speech)-1)/chunk_stride+1)
print(f"total_chunk_num: {total_chunk_num}")

results = []  # 新增：用于保存所有识别结果
with open('result.txt', 'w', encoding='utf-8') as f:  # 打开文件用于实时写入
    for i in range(total_chunk_num):
        speech_chunk = speech[i*chunk_stride:(i+1)*chunk_stride]
        is_final = i == total_chunk_num - 1
        res = model.generate(input=speech_chunk, cache=cache, is_final=is_final, chunk_size=chunk_size, encoder_chunk_look_back=encoder_chunk_look_back, decoder_chunk_look_back=decoder_chunk_look_back)
        print(res)
        # 新增：将识别结果拼接到results，并实时写入文件
        if isinstance(res, list):
            for r in res:
                if isinstance(r, dict) and 'text' in r:
                    text = r['text']
                else:
                    text = str(r)
                results.append(text)
                f.write(text)
                f.flush()
        else:
            text = str(res)
            results.append(text)
            f.write(text)
            f.flush()