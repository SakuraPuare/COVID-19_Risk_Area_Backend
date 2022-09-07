import json
import pathlib
from typing import Dict, List, Union

import query

path = pathlib.Path('version')

if not path.exists() and not path.is_dir():
	path.mkdir()


def list_version() -> Union[List, None]:
	file_list = list(path.iterdir())
	if len(file_list) == 0:
		return None
	else:
		return sorted([str(i).split('.')[0] for i in file_list if i.is_file()])


def save_version(version: str, area: Dict[str, Dict]) -> None:
	with open(path / f"{version}.json", 'w', encoding='utf-8') as f:
		f.write(json.dumps(area, ensure_ascii=False))


def load_version(version) -> Dict[str, List]:
	with open(path / pathlib.Path(f"{version}.json"), 'r',encoding='utf-8') as f:
		return json.loads(f.read())


def has_version(version: str) -> bool:
	file_list = path.iterdir()
	file = path / pathlib.Path(version + '.json')
	if len(list(file_list)) == 0:
		return False
	if file in list(path.iterdir()):
		if file.exists() and file.is_file():
			return True
		else:
			return False


def load_last_version() -> Dict[str, list]:
	version_list = list_version()
	if version_list is None:
		return query.main()
	else:
		return version_list[-1]


if __name__ == '__main__':
	v = load_last_version()
	pass
