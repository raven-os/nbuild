import importlib.util
from nbuild.log import flog


def load_manifest(manifest_path):
    spec = importlib.util.spec_from_file_location(
        "build_manifest",
        manifest_path
    )

    if not spec:
        flog(
            "Failed to load Build Manifest "
            f"located at path \"{manifest_path}\""
        )
        exit(1)
    return spec
