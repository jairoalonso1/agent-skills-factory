from pathlib import Path
import importlib.util
import pytest

MODULE_PATH = Path(__file__).parents[1] / 'scripts' / 'validate_html_report.py'
spec = importlib.util.spec_from_file_location('validate_html_report', MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)

def test_valid_html(tmp_path):
    path = tmp_path / 'report.html'
    path.write_text('<!doctype html><html lang="es-CO"><head><title>Ficha</title></head><body><main>OK</main></body></html>', encoding='utf-8')
    result = module.validate(path)
    assert result['valid'] is True
    assert result['title'] == 'Ficha'
    assert len(result['sha256']) == 64

def test_missing_body_is_invalid(tmp_path):
    path = tmp_path / 'report.html'
    path.write_text('<html lang="es"><head><title>Ficha</title></head></html>', encoding='utf-8')
    result = module.validate(path)
    assert result['valid'] is False
    assert 'Missing <body> element' in result['errors']

def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        module.validate(tmp_path / 'missing.html')

def test_empty_file_raises(tmp_path):
    path = tmp_path / 'empty.html'
    path.write_text('', encoding='utf-8')
    with pytest.raises(ValueError):
        module.validate(path)
