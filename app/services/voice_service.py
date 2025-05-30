"""
Voice processing service
"""
import torch
import os
from typing import Tuple
from concurrent.futures import ThreadPoolExecutor

try:
    from openvoice import se_extractor
    from openvoice.api import ToneColorConverter
    from openvoice.download_utils import load_or_download_config, load_or_download_model
    from melo.api import TTS
except ImportError as e:
    print(f"Error importing required libraries: {e}")
    print("Please make sure OpenVoice and MeloTTS are installed")
    raise

from app.config.settings import DEVICE, MAX_WORKERS, logger, MODELS

class VoiceService:
    """Service for voice processing operations"""
    
    def __init__(self):
        self.device = DEVICE
        self.executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
        self.tone_color_converter = None
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize OpenVoice models"""
        try:
            config = load_or_download_config()
            self.tone_color_converter = ToneColorConverter(config, device=self.device)
            ckpt = load_or_download_model()
            self.tone_color_converter.load_ckpt(ckpt)
            logger.info("OpenVoice models loaded successfully")
        except Exception as e:
            logger.error(f"Error loading OpenVoice models: {e}")
            self.tone_color_converter = None
    
    def is_models_loaded(self) -> bool:
        """Check if models are loaded"""
        return self.tone_color_converter is not None
    
    def extract_voice_embedding(self, filepath: str) -> Tuple[torch.Tensor, str]:
        """Extract voice embedding from audio file"""
        if not self.is_models_loaded():
            raise Exception("Models not loaded")
        return se_extractor.get_se(filepath, self.tone_color_converter, vad=True)
    
    def generate_cloned_voice(
        self,
        text: str,
        language: str,
        speaker_key: str,
        speed: float,
        target_se: torch.Tensor,
        src_path: str,
        output_path: str = None
    ):
        """Generate cloned voice"""
        # Initialize MeloTTS
        model = MODELS[language]
        speaker_ids = model.hps.data.spk2id
        # Select speaker
        if speaker_key not in speaker_ids:
            available_speakers = list(speaker_ids.keys())
            speaker_key = available_speakers[0] if available_speakers else 'default'

        speaker_id = speaker_ids[speaker_key]
        source_se = self.tone_color_converter.load_source_se(speaker_key.lower())
        # Generate speech with MeloTTS
        model.tts_to_file(text, speaker_id, src_path, speed=speed)
        # Convert voice tone
        encode_message = "@LocaAI"
        return self.tone_color_converter.convert(
            audio_src_path=src_path,
            src_se=source_se,
            tgt_se=target_se,
            output_path=output_path,
            message=encode_message
        )
    
    def get_speakers_for_language(self, language: str) -> list:
        """Get available speakers for a language"""
        try:
            model = TTS(language=language, device=self.device)
            return list(model.hps.data.spk2id.keys())
        except Exception as e:
            logger.warning(f"Could not load speakers for language {language}: {e}")
            return []
    
    def shutdown(self):
        """Shutdown the service"""
        if self.executor:
            self.executor.shutdown(wait=True)
            logger.info("Voice service executor shutdown completed")

# Global voice service instance
voice_service = VoiceService()
