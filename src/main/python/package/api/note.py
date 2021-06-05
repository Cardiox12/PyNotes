import os
import json
from uuid import uuid4
from glob import glob

from package.api.constants import NOTES_DIR


def get_notes():
    notes = []
    files = glob(os.path.join(NOTES_DIR, "*.json"))

    for file in files:
        with open(file, "r") as f:
            data = json.load(f)

            note_uuid = os.path.splitext(os.path.basename(file))[0]
            note_title = data.get("title")
            note_content = data.get("content")

            notes.append(
                Note(
                    title=note_title,
                    content=note_content,
                    uuid=note_uuid
                )
            )

    return notes


class Note:
    def __init__(self, title="", content="", uuid=None):
        self.title = title
        self.content = content
        self.uuid = uuid if uuid else str(uuid4())

    def __repr__(self):
        return f"<PyNotes, title=({self.title}), uuid=({self.uuid}), filename=({self.filename})>"

    def __str__(self):
        return self.title

    @property
    def filename(self):
        return f"{self.uuid}.json"

    @property
    def path(self):
        return os.path.join(NOTES_DIR, self.filename)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if isinstance(value, str):
            self._content = value
        else:
            raise TypeError(f"Content must be a string, not {type(value)}")

    def save(self):
        if not os.path.exists(NOTES_DIR):
            os.mkdir(NOTES_DIR)

        data = {
            "title": self.title,
            "content": self._content
        }
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)

    def delete(self):
        os.remove(self.path)
        if os.path.exists(self.path):
            return False
        return True


if __name__ == '__main__':
    notes = get_notes()
    print(notes)
