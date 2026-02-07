#!/usr/bin/env bash
# Execute the notebook and produce an executed notebook artifact.
set -euo pipefail
python -m nbconvert --to notebook --execute biodiversity.ipynb --output biodiversity-executed.ipynb --ExecutePreprocessor.timeout=600
echo "Executed notebook saved to biodiversity-executed.ipynb"
