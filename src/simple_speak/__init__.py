from enum import StrEnum
from subprocess import run
import sys
from typing import Optional


class Synthesizer(StrEnum):
    AMAZON_POLLY = "AMAZON_POLLY"
    ESPEAK_NG = "ESPEAK_NG"
    MAC_OS = "MAC_OS"


class SimpleSpeak:
    def __init__(
        self,
        voice: Optional[str] = None,
        synthesizer: Synthesizer = Synthesizer.MAC_OS,
    ) -> None:
        if synthesizer == Synthesizer.MAC_OS and sys.platform != "darwin":
            raise ValueError("You must run the specified synthesizer on macOS.")

        self.__voice: Optional[str] = voice
        self.__synthesizer: Synthesizer = synthesizer

    def speak(
        self,
        text: str,
        filename: str,
    ) -> None:
        if self.__synthesizer == Synthesizer.MAC_OS:
            run(args=[
                "say",
                text,
                # Specify voice if necessary
                *(
                    [
                        "-v",
                        self.__voice,
                    ] if self.__voice
                    else []
                ),
                "--file-format=mp4f",
                "-o",
                filename + ".mp4",
            ])
        elif self.__synthesizer == Synthesizer.ESPEAK_NG:
            run(args=[
                "espeak-ng",
                text,
                # Specify voice if necessary
                *(
                    [
                        "-v",
                        self.__voice,
                    ] if self.__voice
                    else []
                ),
                "-w",
                filename + ".wav",
            ])
        else:
            raise NotImplementedError("The specified synthesizer is not implemented yet.")
