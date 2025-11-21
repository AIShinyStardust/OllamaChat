from pathlib import Path
import json

class FileIO:
    def __init__():
        pass

    @staticmethod
    def serializeDict(path, data) -> None:
        try:
            fullPath = Path(path)
            fullPath.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as file:
                file.write(json.dumps(data, indent=2, ensure_ascii=False))
        except FileNotFoundError:
            raise FileNotFoundError(f"The file '{path}' does not exist")
        except PermissionError:
            raise PermissionError(f"You don't have permissions to access '{path}'")
        except UnicodeDecodeError:
            raise UnicodeDecodeError(f"Encoding error in '{path}'")
        except Exception as e:
            raise Exception(f"Unknown error: {e}")
        return None

    @staticmethod
    def deserializeDict(path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"The file '{path}' does not exist")
        except PermissionError:
            raise PermissionError(f"You don't have permissions to access '{path}'")
        except UnicodeDecodeError:
            raise UnicodeDecodeError(f"Encoding error in '{path}'")
        except Exception as e:
            raise Exception(f"Unknown error: {e}")
        return None
