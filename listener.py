from st_route import st_route
from typing import Union, Any, Dict, List, Tuple
import json

global session_state

def init_session_state(ss):
  global session_state
  session_state = ss

@st_route(path='listener/(.*)', globally=True)
def API_listener(
        path_args: List[str],
        path_kwargs: Dict[str, Any],
        method: str,
        body: bytes,
        arguments: Dict[str, Any]
) -> Union[int, bytes, str, Tuple[int, Union[bytes, str]], Tuple[int, Union[bytes, str], Dict[str, Any]]]:
    """
    path_args: path regex unnamed groups
    path_kwargs: path regex named groups
    method: HTTP method
    body: the request body in bytes
    arguments: The query and body arguments
    returns with any of the followings:
      int: HTTP response code
      bytes/str: HTTP 200 with body. str encoded with python default
      Tuple[int, bytes/str]: HTTP response code with body
      Tuple[int, bytes/str, Dict[str, Any]]: HTTP response code with body and additional headers
    If you don't need any of the arguments, just use **kwargs.
    """
    global session_state
    if not session_state["LISTENER"]: return 404, "NOT FOUND"
    if path_args[0].decode() != session_state["LISTENER_KEY"]: return 403, "FORBIDDEN"
    try:
      json_data = json.loads(body.decode())
    except:
      return 400, "BAD REQUEST"
    
    if "expr" not in json_data: return 400, "BAD REQUEST"
    folder = json_data.get("folder", "")
    name = json_data.get("name", "")
    expr = json_data["expr"]
    
    session_state["INBOUND_EXPRESSIONS"].append({"folder":folder,"name":name,"expr":expr})
    return 200, "OK"