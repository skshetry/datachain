import pytest

from datachain.catalog import get_catalog
from datachain.lib.dc import DataChain
from datachain.lib.webdataset_laion import process_laion_meta


@pytest.mark.benchmark
def test_laion(datasets, benchmark):
    def run_script(uri, catalog, **kwargs):
        return (
            DataChain.from_storage(uri, catalog=catalog, **kwargs)
            .gen(emd=process_laion_meta)
            .map(
                stem=lambda file: file.get_file_stem(),
                params=["emd.file"],
                output=str,
            )
            .save("laion_emb")
        )

    catalog = get_catalog()
    dataset = datasets / "laion-tiny.npz"
    assert dataset.is_file()

    dc = benchmark(run_script, dataset.as_uri(), catalog)
    assert dc.name == "laion_emb"
