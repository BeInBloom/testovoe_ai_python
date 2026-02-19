import pytest

from src.core.document_collector import DocumentCollector
from src.core.folder_scanner import FolderScanner
from src.core.logger import Logger
from src.readers.factory import ReaderFactory
from src.readers.txt_reader import TxtReader


@pytest.fixture
def logger():
    return Logger(name="test", level="DEBUG")


def test_folder_scanner_recursive(tmp_path, logger):
    # Создаем структуру папок
    (tmp_path / "a.txt").touch()
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "b.txt").touch()
    (tmp_path / ".hidden").touch()

    scanner = FolderScanner(logger=logger, recursive=True)
    files = list(scanner.scan(tmp_path))

    # .hidden должны игнорироваться в теории, но наш сканер возвращает всё
    # в DocumentCollector мы фильтруем . файлы
    assert len(files) == 3


def test_document_collector_filters_hidden(tmp_path, logger):
    (tmp_path / ".hidden").touch()
    (tmp_path / "visible.txt").touch()

    factory = ReaderFactory(readers=[TxtReader()])
    collector = DocumentCollector(
        reader_factory=factory, logger=logger, max_file_size_bytes=100
    )

    docs = collector.collect([tmp_path / ".hidden", tmp_path / "visible.txt"])

    assert len(docs) == 1
    assert docs[0].path.name == "visible.txt"


def test_document_collector_size_limit(tmp_path, logger):
    p = tmp_path / "large.txt"
    p.write_text("A" * 200)  # 200 bytes

    factory = ReaderFactory(readers=[TxtReader()])
    collector = DocumentCollector(
        reader_factory=factory,
        logger=logger,
        max_file_size_bytes=100,  # limit 100 bytes
    )

    docs = collector.collect([p])
    assert len(docs) == 0  # Должен быть отфильтрован по размеру


def test_folder_scanner_permission_denied(tmp_path, logger, mocker):
    mocker.patch("pathlib.Path.iterdir", side_effect=PermissionError)

    scanner = FolderScanner(logger=logger)
    files = list(scanner.scan(tmp_path))
    assert len(files) == 0
