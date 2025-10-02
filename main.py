# main.py
from wakeword import WakeWordDetect
from alsautils import play_wav, AudioConfig

def ding(idx):
    print("Detected - ")
    play_wav(
        path="ding.wav", 
        cfg=AudioConfig(
            device="default", 
            gain=1.0
        )
    )

def main():
    print("Listening…", flush=True)
    detector = WakeWordDetect(
        access_key="F7Ul4dw58XwV61ON+8VuhgsaHq+qPiz0VEFLXs0vJUPRkR4KZLAngw==",
        keyword_paths=["./Astra_en_raspberry-pi_v3_0_0.ppn"],
        # keywords=["jarvis"],
        device="plughw:2,0", gain=5
    )
    detector.run(ding)


if __name__ == '__main__':
    main()