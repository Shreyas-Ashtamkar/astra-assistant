# wakeword_fast.py
import signal, sys
import pvporcupine as pvc
from alsautils import ALSARecorder, AudioConfig, porcupine_frame_iter

class WakeWordDetect:
    def __init__(self, access_key, keyword_paths=None, keywords=None,
                 device="plughw:2,0", gain=3):
        self.ppn = pvc.create(access_key=access_key,
                              keyword_paths=keyword_paths, keywords=keywords)
        self.rec = ALSARecorder(AudioConfig(
            device=device, rate=self.ppn.sample_rate, channels=1,
            chunk=self.ppn.frame_length, gain=gain))
        self.stop = False
        signal.signal(signal.SIGINT, self._stop)
        signal.signal(signal.SIGTERM, self._stop)

    def _stop(self, *_): self.stop = True

    def run(self, on_wake):
        # on_wake(index) -> True to stop, False/None to continue
        try:
            for frame in porcupine_frame_iter(self.rec, self.ppn.frame_length):
                if self.stop: break
                idx = self.ppn.process(frame)
                if idx >= 0:
                    if on_wake(idx): break
        finally:
            try: self.rec.close()
            finally:
                self.ppn.delete()

if __name__ == "__main__":
    print("Listening…", flush=True)
    W = WakeWordDetect(
        access_key="F7Ul4dw58XwV61ON+8VuhgsaHq+qPiz0VEFLXs0vJUPRkR4KZLAngw==",
        keyword_paths=["./Astra_en_raspberry-pi_v3_0_0.ppn"],
        # keywords=["computer"],
        device="plughw:2,0", gain=5
    )
    W.run(lambda i: (print("Woke Up! \a", flush=True), False)[1])
