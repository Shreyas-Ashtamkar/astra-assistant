# alsa_recorder.py
from dataclasses import dataclass
from typing import Generator, Iterable, Optional
from alsaaudio import PCM, PCM_PLAYBACK, PCM_CAPTURE, PCM_NORMAL, PCM_FORMAT_S16_LE
import numpy as np, wave, struct, logging

logging.basicConfig(level=logging.INFO)

@dataclass
class AudioConfig:
    device: str = "plughw:1,0"   # ALSA device string, e.g. "plughw:1,0"
    rate: int = 44100            # 16000 for Porcupine
    channels: int = 2            # mono=1, stereo=2
    chunk: int = 512             # frames per read/write
    gain: float = 1.0            # linear multiplier for samples


def _apply_gain_bytes(pcm_bytes: bytes, gain: float) -> bytes:
    """Apply linear gain to 16-bit PCM bytes."""
    if gain == 1.0:
        return pcm_bytes
    s = np.frombuffer(pcm_bytes, dtype=np.int16).astype(np.float32)
    s = np.clip(s * gain, -32768, 32767).astype(np.int16)
    return s.tobytes()


class ALSARecorder:
    def __init__(self, cfg: AudioConfig):
        self.cfg = cfg
        self.pcm = PCM(
            type=PCM_CAPTURE,
            mode=PCM_NORMAL,
            device=cfg.device,
            channels=cfg.channels,
            rate=cfg.rate,
            format=PCM_FORMAT_S16_LE,
            periodsize=cfg.chunk,
        )
        self._closed = False

    def frames(self) -> Generator[bytes, None, None]:
        while not self._closed:
            n, data = self.pcm.read()
            if n > 0:
                yield data

    def close(self):
        if not self._closed:
            try:
                self.pcm.close()
            except Exception as e:
                logging.warning(f"Failed closing recorder: {e}")
            self._closed = True

    def __enter__(self): return self
    def __exit__(self, *_): self.close()


class ALSAPlayer:
    def __init__(self, cfg: AudioConfig):
        self.cfg = cfg
        self.pcm = PCM(
            type=PCM_PLAYBACK,
            mode=PCM_NORMAL,
            device=cfg.device,
            channels=cfg.channels,
            rate=cfg.rate,
            format=PCM_FORMAT_S16_LE,
            periodsize=cfg.chunk,
        )

    def write_frames(self, pcm_bytes: bytes):
        fsz = self.cfg.channels * 2  # bytes per frame
        pcm_bytes = pcm_bytes[: len(pcm_bytes) - (len(pcm_bytes) % fsz)]
        for i in range(0, len(pcm_bytes), self.cfg.chunk * fsz):
            self.pcm.write(pcm_bytes[i : i + self.cfg.chunk * fsz])

    def play_iter(self, frames_iter: Iterable[bytes], apply_gain: bool = True):
        for b in frames_iter:
            if apply_gain and self.cfg.gain != 1.0:
                b = _apply_gain_bytes(b, self.cfg.gain)
            self.write_frames(b)

    def close(self):
        try:
            self.pcm.close()
        except Exception as e:
            logging.warning(f"Failed closing player: {e}")

    def __enter__(self): return self
    def __exit__(self, *_): self.close()


def write_wav(path: str, pcm_bytes: bytes, rate: int, channels: int):
    with wave.open(path, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        wf.writeframes(pcm_bytes)


def play_pcm_bytes(pcm_bytes: bytes, rate: int, channels: int, cfg: Optional[AudioConfig] = None):
    cfg = cfg or AudioConfig(rate=rate, channels=channels)
    with ALSAPlayer(cfg) as p:
        if cfg.gain != 1.0:
            pcm_bytes = _apply_gain_bytes(pcm_bytes, cfg.gain)
        p.write_frames(pcm_bytes)


def porcupine_frame_iter(rec: ALSARecorder, frame_len: int) -> Generator[tuple[int, ...], None, None]:
    """Read exactly frame_len samples for Porcupine."""
    buf = b""
    need = frame_len * 2
    for chunk in rec.frames():
        buf += chunk
        while len(buf) >= need:
            frame, buf = buf[:need], buf[need:]
            yield struct.unpack_from("<" + "h" * frame_len, frame)


def record_seconds_to_wav(seconds: float, cfg: Optional[AudioConfig] = None, out="output_alsa.wav"):
    cfg = cfg or AudioConfig()
    with ALSARecorder(cfg) as rec:
        frames = []
        total = int(cfg.rate / cfg.chunk * seconds)
        for _, chunk in zip(range(total), rec.frames()):
            frames.append(chunk)
    pcm_bytes = _apply_gain_bytes(b"".join(frames), cfg.gain)
    write_wav(out, pcm_bytes, cfg.rate, cfg.channels)
    logging.info(f"Saved {out}")


def play_wav(path: str, cfg: Optional[AudioConfig] = None):
    cfg = cfg or AudioConfig()
    with wave.open(path, "rb") as wf:
        if wf.getsampwidth() != 2:
            raise ValueError("Only 16-bit PCM WAV supported.")
        rate, ch = wf.getframerate(), wf.getnchannels()
        with ALSAPlayer(AudioConfig(device=cfg.device, rate=rate, channels=ch, chunk=cfg.chunk, gain=cfg.gain)) as p:
            while True:
                data = wf.readframes(cfg.chunk)
                if not data:
                    break
                if cfg.gain != 1.0:
                    data = _apply_gain_bytes(data, cfg.gain)
                p.write_frames(data)


if __name__ == "__main__":
    # Example 1: record and play
    record_seconds_to_wav(
        seconds=5,
        out="output_alsa.wav",
        cfg=AudioConfig(rate=44100, channels=2, chunk=512, gain=2.0),
    )

    play_wav(
        path="output_alsa.wav",
        cfg=AudioConfig(device="default", gain=1.0),
    )
