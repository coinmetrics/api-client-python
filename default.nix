{ lib
, buildPythonPackage
, fetchPypi
, mypy
, orjson
, pandas
, poetry-core
, pytestCheckHook
, pytest-mock
, pythonOlder
, python-dateutil
, requests
, typer
, types-python-dateutil
, types-requests
, types-ujson
, websocket-client
, tqdm
}:

buildPythonPackage rec {
  pname = "coinmetrics-api-client";
  version = "2023.8.30.20";
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
  ];

  nativeCheckInputs = [
    mypy
    pytestCheckHook
    pytest-mock
    types-python-dateutil
    types-requests
    types-ujson
  ] ++ passthru.optional-dependencies.pandas;

  pythonImportsCheck = [
    "coinmetrics.api_client"
  ];

  preCheck = ''
    mypy -p coinmetrics -p test
  '';

  passthru = {
    optional-dependencies = {
      pandas = [ pandas ];
    };
  };

  meta = with lib; {
    description = "Coin Metrics API v4 client library";
    homepage = "https://coinmetrics.github.io/api-client-python/site/index.html";
    license = licenses.mit;
    maintainers = with maintainers; [ centromere ];
  };
}
