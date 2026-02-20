import logging
import os
import warnings


def suppress_third_party_noise():
    warnings.filterwarnings("ignore", category=UserWarning, module="torch.utils.data")
    noisy_loggers = [
        "whisper",
        "torch",
        "torchaudio",
        "transformers",
    ]
    for logger_name in noisy_loggers:
        logging.getLogger(logger_name).setLevel(logging.ERROR)

    os.environ["TORCH_CPP_LOG_LEVEL"] = "ERROR"
    os.environ["PYTORCH_JIT_LOG_LEVEL"] = "OFF"

    try:
        import av

        av.logging.set_level(av.logging.ERROR)
    except ImportError:
        pass
