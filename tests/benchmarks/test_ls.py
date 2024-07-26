import pytest

from datachain.cli import main


@pytest.mark.benchmark
def test_ls(tmp_dir, benchmark):
    bucket = "s3://ldb-public/remote/data-lakes/Stanford-dog-breeds/"
    assert benchmark(main, ["ls", bucket, "--anon"]) == 0
