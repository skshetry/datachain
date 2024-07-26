import subprocess

import pytest


@pytest.mark.benchmark
def test_help(tmp_dir, benchmark):
    assert benchmark(subprocess.check_call, ["datachain", "--help"]) == 0
