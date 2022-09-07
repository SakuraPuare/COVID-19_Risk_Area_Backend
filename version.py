import json
import pathlib
from typing import Dict, List

path = pathlib.Path('version')

if not path.exists() and not path.is_dir():
	path.mkdir()


def save_version(version: str, area: Dict[str, Dict]) -> None:
	with open(path / f"{version}.json", 'w', encoding='utf-8') as f:
		f.write(json.dumps(area, ensure_ascii=False))


def load_version(version) -> Dict[str, List]:
	with open(pathlib.Path(f"{version}.json"), 'r') as f:
		return json.loads(f.read())


def has_version(version: str) -> bool:
	file_list = path.iterdir()
	file = pathlib.Path(version + '.json')
	if file in file_list:
		if file.exists() and file.is_file():
			return True
		else:
			return False
