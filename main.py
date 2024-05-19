from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Input, Label
from textual.containers import Container
import csv
import os
from typing import Dict, List
import datetime


class FileDB:
    def __init__(self, path):
        self.path = path
        self._fieldnames = ["name", "url", "created_at"]
        self._create_if_not_exist()

    def _create_if_not_exist(self) -> None:
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                writer = csv.writer(f)
                writer.writerow(self._fieldnames)

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
            writer = csv.DictWriter(f, delimiter=",", fieldnames=self._fieldnames)
            writer.writerow(data)
        return 1


class YTApp(App):
    def __init__(self, db_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = FileDB(db_path)

    CSS_PATH = "style.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        # TODO: add validators to make sure that this is a url
        yield Container(Label("Add new channel to track"), id="add-url-text")
        yield Container(
            Input(
                placeholder="name", type="text", id="add-new-name", name="input_name"
            ),
            Input(placeholder="url", type="text", id="add-new-url", name="input_url"),
            id="add-data",
        )
        yield Container(Button("Add", variant="primary"), id="submit-add-data")
        yield Footer()

    def on_input_submitted(self):
        name_input_widget = self.query_one("#add-new-name", Input)
        url_input_widget = self.query_one("#add-new-url", Input)
        new_data = {
            "name": name_input_widget.value,
            "url": url_input_widget.value,
            "created_at": datetime.datetime.now(),
        }
        res = self.db.add(new_data)
        if res == 1:
            name_input_widget.value = ""
            url_input_widget.value = ""
            name_input_widget.focus()

    def on_mount(self) -> None:
        self.title = "Youtube Video Aggregator"
        self.sub_title = "a tool to download from your favorite creators"

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark


if __name__ == "__main__":
    db = FileDB("data.csv")
    app = YTApp("data.csv")
    app.run()
