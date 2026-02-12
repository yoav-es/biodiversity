#!/usr/bin/env pwsh
param()
if (-not (Test-Path -Path "docker-compose.yml")) {
  Write-Error "Please run from the project root (where docker-compose.yml lives)."
  exit 1
}

Write-Host ""
Write-Host "hello,"
Write-Host "Project: Biodiversity analysis (report generator)"
Write-Host "-----------------------------------------------"

# print package version if available
try {
  $ver = & python -c "import biodiversity; print(biodiversity.__version__)" 2>$null
  if ($LASTEXITCODE -eq 0) { Write-Host "Version: $ver" }
} catch { }

while ($true) {
  Write-Host ""
  Write-Host "Select an option:"
  Write-Host "  1) Create HTML report (execute notebook -> export report.html)"
  Write-Host "  2) Open Jupyter Notebook (containerized; binds to localhost:8888)"
  Write-Host "  3) Exit"
  $choice = Read-Host "Choice [1-3]"

  switch ($choice) {
    '1' {
      Write-Host "Building image (no-cache) and producing HTML report..."
      docker compose build --no-cache
      docker compose run --rm report sh -c "python -m nbconvert --to notebook --execute biodiversity.ipynb --ExecutePreprocessor.timeout=600 --output biodiversity-executed.ipynb && python -m nbconvert --to html biodiversity-executed.ipynb --output report.html"
      Write-Host "Done. Report saved to: $(Resolve-Path report.html)"
    }
    '2' {
      Write-Host "Starting Jupyter server inside container. Open http://localhost:8888 in your browser."
      docker compose run --service-ports --rm report sh -c "python -m notebook --ip=0.0.0.0 --no-browser --NotebookApp.token='' --NotebookApp.password=''"
      Write-Host "Jupyter server stopped."
    }
    '3' {
      Write-Host "Exiting."
      break
    }
    Default {
      Write-Host "Invalid choice: '$choice'. Please enter 1, 2 or 3."
    }
  }
}

