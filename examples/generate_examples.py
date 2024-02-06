import ast
import inspect
from typing import Dict, List, Union
from coinmetrics.api_client import CoinMetricsClient
import os
import logging
logging.basicConfig(level=logging.INFO)

EXAMPLE_TEMPLATE = """
from coinmetrics.api_client import CoinMetricsClient

api_key = "<API_KEY>"
client = CoinMetricsClient(api_key)

data = client.{method}({required_params}).first_page()
print(data)
"""

def return_query(base_string, **kwargs):
    """
    Creates a formatted string based on the key word arguments being passed
    """
    return base_string.format(**kwargs)

def extract_api_calls(source_code) -> Dict[str, List[str]]:
    tree = ast.parse(source_code)

    class APIClientVisitor(ast.NodeVisitor):
        def __init__(self):
            self.functions = {}

        def visit_FunctionDef(self, node: ast.FunctionDef):
            method_name = node.name
            if not any(string in method_name for string in ["get", "catalog", "reference", "security", "blockchain"]) or method_name.startswith("_"):
                return
            endpoint = self.get_endpoint_from_node(node)
            required_params = self.get_required_params_from_node(node)
            self.functions[endpoint] = {
                "method": method_name,
                "params": required_params
            }
            
        @staticmethod
        def get_required_params_from_node(node: ast.FunctionDef) -> List:
            arguments = node.args
            required_args = []

            for arg, default in zip(arguments.args, arguments.defaults):
                arg_name = arg.arg
                if arg_name == 'self':
                    continue
                arg_type = ast.get_source_segment(source_code, arg.annotation)
                arg_is_required = arg_type == arg_type.split('Optional')[0]
                if arg_is_required:
                    required_args.append(arg_name)
            return required_args

        @staticmethod
        def get_endpoint_from_node(node: ast.FunctionDef) -> str:
            method_name = node.name
            for stmt in node.body:
                if isinstance(stmt, ast.Return):
                    if "stream" in method_name:
                        if type(stmt.value.args[0]) == str:
                            endpoint = stmt.value.args[0]
                        else:
                            endpoint = stmt.value.args[0].value
                    elif "catalog" in method_name and not "_v2" in method_name:
                        endpoint = stmt.value.args[0].value.args[0].value
                    elif any([method_name.startswith(prefix) for prefix in ["get_", "reference", "security", "blockchain_"]]) or (method_name.startswith("catalog") and method_name.endswith("v2")):
                        if isinstance(stmt.value.args[1], ast.Call):
                            endpoint = APIClientVisitor.get_endpoint_from_list_args(stmt.value.args[1].args[0].values)
                        if isinstance(stmt.value.args[1], ast.JoinedStr):
                            joined_str = stmt.value.args[1]
                            endpoint = APIClientVisitor.get_endpoint_from_joined_ast_v2(joined_str.values)
                        elif isinstance(stmt.value.args[1], ast.Constant):
                            endpoint = stmt.value.args[1].value
                    else:
                        raise ValueError(f"Function type for function: {node.name} not accounted for")
                    if not endpoint.startswith("/"):
                        endpoint = "/" + endpoint
                    return endpoint

        @staticmethod
        def get_endpoint_from_joined_ast_v2(list_of_const_fvs: List[Union[ast.Constant, ast.FormattedValue]]) -> str:
            result_string = ""
            for item in list_of_const_fvs:
                if isinstance(item, ast.Constant):
                    result_string += item.value
                elif isinstance(item, ast.FormattedValue):
                    result_string += "{" + item.value.id + "}"
            return result_string

        @staticmethod
        def get_endpoint_from_list_args(list_args: List[Union[ast.Constant, ast.FormattedValue]]):
            result_str = ""
            for arg in list_args:
                if isinstance(arg, ast.Constant):
                    result_str += arg.value
                else:
                    result_str += "{" + arg.value.id + "}"
            return result_str

    visitor = APIClientVisitor()
    visitor.visit(tree)
    return visitor.functions

def write_examples(function_dict):
    for endpoint, metadata in function_dict.items():
        method = metadata['method']
        params = metadata['params']
        param_str = ", ".join([f"{param}='<arg values>'" for param in params])
        example = return_query(EXAMPLE_TEMPLATE, method=method, required_params=param_str)
        endpoint_dir ="/".join(endpoint.strip("/").split("/")[:-1])
        dir_path = f"examples/api_doc_examples/{endpoint_dir}"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        py_file = f"examples/api_doc_examples/{endpoint.strip('/')}.py"
        with open(py_file, "w+") as f:
            logging.info(f"Writing {py_file}")
            f.write(example)

if __name__ == "__main__":
    function_dict = extract_api_calls(inspect.getsource(CoinMetricsClient))
    write_examples(function_dict)