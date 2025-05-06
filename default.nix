{ lib
, buildPythonPackage
, fetchPypi
, mypy
, orjson
, pandas
, poetry-core
, polars
, pythonOlder
, python-dateutil
, pytestCheckHook
, pytest-mock
, requests
, tqdm
, typer
, types-python-dateutil
, types-requests
, types-ujson
, websocket-client
}:

buildPythonPackage rec {
  pname = "coinmetrics-api-client";
  version = "2025.5.6.13";
  format = "pyproject";

  disabled = pythonOlder "3.9";

  __darwinAllowLocalNetworking = true;

  src = ./.;

  nativeBuildInputs = [
    poetry-core
  ];

  propagatedBuildInputs = [
    orjson
    python-dateutil
    requests
    typer
    websocket-client
    tqdm
    pandas
    polars
  ];

  nativeCheckInputs = [
    mypy
    pytestCheckHook
    pytest-mock
    types-python-dateutil
    types-requests
    types-ujson
  ];

  pythonImportsCheck = [
    "coinmetrics.api_client"
  ];

  preCheck = ''
    mypy -p coinmetrics -p test
  '';

  passthru = {
    optional-dependencies = {
      pandas = [ pandas ];
      polars = [ polars ];
    };
  };

  meta = with lib; {
    description = "Coin Metrics API v4 client library";
    homepage = "https://coinmetrics.github.io/api-client-python/site/index.html";
    license = licenses.mit;
    maintainers = with maintainers; [ centromere ];
  };
}