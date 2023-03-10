import os
import json
from uuid import uuid4
from glob import glob

from api.constants import NOTES_DIR


def get_notes():
    notes = []
    fichiers = glob(os.path.join(NOTES_DIR, "*.json"))
    for fichier in fichiers:
        with open(fichier, "r") as f:
            note_data = json.load(f)
            note_uuid = os.path.splitext(os.path.basename(fichier))[0]
            note_title = note_data.get("title")
            note_content = note_data.get("content")
            note = Note(uuid=note_uuid, title=note_title, content=note_content)
            notes.append(note)
    return notes


class Note:
    def __init__(self, title="", content="", uuid=None):
        self.uuid = uuid or str(uuid4())
        self.title = title
        self.content = content

    def __repr__(self):
        return f"{self.title} ({self.uuid})"

    def __str__(self):
        return self.title

    @property
    def path(self):
        return os.path.join(NOTES_DIR, f"{self.uuid}.json")

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if isinstance(value, str):
            self._content = value
        else:
            raise TypeError("Valeur invalide (besoin d'une chaîne de caractères).")

    def save(self):
        if not os.path.exists(NOTES_DIR):
            os.makedirs(NOTES_DIR)

        data = {"title": self.title, "content": self.content}
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)

    def delete(self):
        os.remove(self.path)
        return not os.path.exists(self.path)


if __name__ == '__main__':
    notes = get_notes()
    print(notes)
