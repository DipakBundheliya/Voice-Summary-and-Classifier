import pyannote.audio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
import torch

class my_dialogue_classifier:

    def __init__(self,audio_file):
        self.audio_file = audio_file
        self.dialogues = []

    def classify(self):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print("Step1")
        diarization_model = pyannote.audio.Pipeline.from_pretrained("pyannote/speaker-diarization@2.1" , use_auth_token="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")
        diarization_model.to(device)
        print("Step2")

        tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
        asr_model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
        asr_model.to(device)
        print("Step2")

        diarization = diarization_model(self.audio_file)
        print("Step3")

        # start_time = 0.0  # start time in seconds
        # end_time = 23.0    # end time in seconds
        # segment = pyannote.core.Segment(start_time, end_time)

        # target_sample_rate = 16000  # Specify the target sample rate
        # mono_strategy = 'downmix'  # Specify the mono strategy for multi-channel audio

        audio = pyannote.audio.Audio(sample_rate=16000, mono='downmix')   
        waveform, sample_rate = audio({"audio": self.audio_file})
        print("Step4")
         
 
        cnt=0
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            start_sample = int(turn.start * sample_rate)
            end_sample = int(turn.end * sample_rate)
            speech = waveform[:, start_sample:end_sample]  # Crop the waveform tensor
            input_values = tokenizer(speech, return_tensors="pt").input_values.to(device)
            logits = asr_model(input_values[0]).logits
            transcript = tokenizer.decode(logits.argmax(-1)[0])
            # print(cnt , "--" , transcript)
            if cnt%2 == 0:
                self.dialogues.append({"speaker 1" : transcript})
            else:
                self.dialogues.append({"speaker 2" : transcript} )
            cnt+=1        


        return self.dialogues
    

