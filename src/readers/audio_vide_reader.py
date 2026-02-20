from collections.abc import Iterable
from pathlib import Path
from typing import Literal

from faster_whisper import WhisperModel
from faster_whisper.transcribe import Segment, Word

from src.domain.models import ContentType, DocumentContent

WhisperModelSize = Literal[
    "tiny", "base", "small", "medium", "large", "large-v2", "large-v3"
]
DeviceType = Literal["cpu", "cuda", "auto"]
ComputeType = Literal["int8", "float16", "float32", "int8_float16"]


class AudioVideoReader:
    SUPPORTED_EXTENSIONS = {
        ".mp3",
        ".wav",
        ".ogg",
        ".flac",
        ".m4a",
        ".mp4",
        ".mkv",
        ".avi",
        ".mov",
        ".webm",
    }

    DEFAULT_BEAM_SIZE = 5
    UNRECOGNIZED_TAG: str = " [НЕРАЗБОРЧИВО]"

    def __init__(
        self,
        model_size: WhisperModelSize = "small",
        prob_threashold: float = 0.6,
        device: DeviceType = "cpu",
        compute_type: ComputeType = "int8",
    ):
        self._model = WhisperModel(model_size, device=device, compute_type=compute_type)
        self._threashold = prob_threashold

    def supports(self, file_path: Path) -> bool:
        return file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS

    def get_supported_extensions(self) -> list[str]:
        return list(self.SUPPORTED_EXTENSIONS)

    def read(self, file_path: Path) -> DocumentContent:
        return DocumentContent(
            file_path=file_path,
            content_type=ContentType.TEXT,
            text_content=self._extract_text(file_path),
            mime_type="text/plain",
        )

    def _extract_text(self, file_path: Path) -> str:
        raw_segments = self._transcribe(file_path)
        clean_segments = self._process_segments(raw_segments)
        return " ".join(clean_segments)

    def _transcribe(self, file_path: Path) -> Iterable[Segment]:
        segments, _ = self._model.transcribe(
            str(file_path),
            word_timestamps=True,
            beam_size=self.DEFAULT_BEAM_SIZE,
        )

        return segments

    def _process_segments(self, segments: Iterable[Segment]) -> list[str]:
        processed = []

        for segment in segments:
            clean_text = self._format_segment(segment)
            if clean_text:
                processed.append(clean_text)

        return processed

    def _format_segment(self, segment: Segment) -> str:
        words = segment.words or []
        formated_words = [self._evalate_word(word) for word in words]
        return "".join(formated_words)

    def _evalate_word(self, word: Word) -> str:
        if word.probability < self._threashold:
            return self.UNRECOGNIZED_TAG
        return word.word
