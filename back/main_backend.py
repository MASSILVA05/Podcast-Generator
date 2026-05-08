# Version5/back/main_backend.py
import sys
from pathlib import Path
import os

# Ajoute le dossier parent au PYTHONPATH pour permettre les imports de 'back'
sys.path.append(str(Path(__file__).resolve().parent.parent))

import json
from datetime import datetime
from typing import List, Dict, Any

from back.segmentation.pipeline_segmentation import run_full_pipeline
from back.scenario.scenario_generator import generate_dialogue_from_segments, save_script
import json
import subprocess
import sys
from pathlib import Path

class BackendPipelineError(Exception):
    pass


def save_segments(
    segments: List[Dict[str, Any]],
    output_path: str = "segments.json"
) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(segments, f, ensure_ascii=False, indent=2, default=str)


def save_run_metadata(
    resources: List[str],
    podcast_duration: str,
    script_path: str,
    segments_path: str,
    audio_path: str,
    output_path: str = "run_metadata.json"
) -> None:
    metadata = {
        "generated_at": datetime.now().isoformat(),
        "resources": resources,
        "podcast_duration": podcast_duration,
        "script_path": script_path,
        "segments_path": segments_path,
        "audio_path": audio_path
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)


def run_backend_pipeline(
    resources: List[str],
    podcast_duration: str,
    podcast_language: str = "Français",
    participants: List[str] = None,
    output_dir: str = "outputs"
) -> Dict[str, Any]:
    """
    Reçoit les ressources envoyées par le front,
    puis lance :
    extraction -> segmentation -> scénarisation -> TTS -> sauvegarde
    """
    if not resources:
        raise BackendPipelineError("Aucune ressource envoyée par le front.")

    if not podcast_duration:
        raise BackendPipelineError("Aucune durée envoyée par le front.")

    if not participants:
        participants = ["Voix_01", "Voix_02"]

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    script_output_path = output_path / f"podcast_script_{timestamp}.txt"
    segments_output_path = output_path / f"segments_{timestamp}.json"
    audio_output_path = output_path / f"podcast_audio_{timestamp}.mp3"
    metadata_output_path = output_path / f"run_metadata_{timestamp}.json"

    segments = run_full_pipeline(resources)

    if not segments:
        raise BackendPipelineError("Aucun segment généré.")

    save_segments(segments, str(segments_output_path))

    script = generate_dialogue_from_segments(
        segments=segments,
        podcast_duration=podcast_duration,
        participants=participants
    )

    if not script.strip():
        raise BackendPipelineError("Le script généré est vide.")

    save_script(script, str(script_output_path))

    audio_result_path = run_tts_in_separate_env(
    script=script,
    podcast_language=podcast_language,
    participants=participants,
    audio_output_path=str(audio_output_path),
    )

    save_run_metadata(
    resources=resources,
    podcast_duration=podcast_duration,
    script_path=str(script_output_path),
    segments_path=str(segments_output_path),
    audio_path=str(audio_result_path),
    output_path=str(metadata_output_path)
    )

    return {
        "success": True,
        "resources_count": len(resources),
        "segments_count": len(segments),
        "script_path": str(script_output_path),
        "segments_path": str(segments_output_path),
        "audio_path": str(audio_result_path),
        "metadata_path": str(metadata_output_path),
        "script": script,
        "segments": segments,
    }
    
def run_tts_in_separate_env(
    script: str,
    podcast_language: str,
    participants: list,
    audio_output_path: str,
) -> str:
    project_root = Path(__file__).resolve().parent.parent
    tts_python = project_root / "venv_tts" / "bin" / "python"
    tts_runner = project_root / "back" / "TTs" / "tts_runner.py"

    payload = {
        "script": script,
        "podcast_language": podcast_language,
        "participants": participants,
        "output_path": audio_output_path,
    }

    payload_path = project_root / "outputs" / "tts_payload.json"
    payload_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    result = subprocess.run(
        [str(tts_python), str(tts_runner), str(payload_path)],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise BackendPipelineError(
            f"Erreur TTS séparé : {result.stderr or result.stdout}"
        )

    try:
        data = json.loads(result.stdout.strip())
        return data["audio_path"]
    except Exception as e:
        raise BackendPipelineError(
            f"Réponse TTS invalide : {result.stdout}\nErreur: {e}"
        )