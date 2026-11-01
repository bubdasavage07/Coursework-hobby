from pathlib import Path


class Assets:
    """Keeps the game's image and audio locations in one place."""

    def __init__(self):
        project_folder = Path(__file__).parent
        images_folder = project_folder / "resources" / "images"
        audio_folder = project_folder / "resources" / "audio"

        # Dictionaries are collections: a descriptive name points to each file.
        self.image_paths = {
            "player": images_folder / "dude.png",
            "zombie": images_folder / "badguy.gif",
            "background": images_folder / "grass.png",
            "game_over": images_folder / "gameover.png",
        }

        self.audio_paths = {
            "shoot": audio_folder / "shoot.wav",
            "enemy": audio_folder / "enemy.wav",
            "hit": audio_folder / "explode.wav",
            "music": audio_folder / "moonlight.wav",
        }
