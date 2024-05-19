from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Input
import csv
import os
from typing import Dict, List


class FileDB:
    def __init__(self, path):
        self.path = path
        self._create_if_not_exist()

    def _create_if_not_exist(self) -> None:
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                writer = csv.writer(f)
                writer.writerow(["name", "url", "created_at"])

    def read(self) -> List[Dict[str, str]]:
        data = []
        with open(self.path, "r") as f:
            d = csv.DictReader(f)
            for i in d:
                data.append(i)
        return data

    def add(self, data: Dict[str, str]) -> int:
        existing_data = self.read()
        if len(existing_data) > 0:
            for v in existing_data:
                if data["name"] == v["name"]:
                    return 0
        with open(self.path, "a", newline="") as f:
            writer = csv.DictWriter(
                f, delimiter=",", fieldnames=["name", "url", "created_at"]
            )
            writer.writerow(data)
        return 1


class YTApp(App):
    CSS_PATH = "style.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        # TODO: add validators to make sure that this is a url
        yield Input(placeholder="name", type="text", id="add-new-name")
        yield Input(placeholder="url", type="text", id="add-new-url")
        yield Button("Button 1", variant="primary")
        yield Button("Button 2")
        yield Footer()

    def on_mount(self) -> None:
        self.title = "Youtube Video Aggregator"
        self.sub_title = "a tool to download from your favorite creators"

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark


if __name__ == "__main__":
    db = FileDB("data.csv")
    app = YTApp()
    app.run()
