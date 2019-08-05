action "Upload Python dist to PyPI" {
  uses = "re-actors/pypi-action@master"
  env = {
    TWINE_USERNAME = "maxking"
  }
  secrets = ["TWINE_PASSWORD"]
}
