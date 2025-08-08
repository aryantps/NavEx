import contextvars

request_id_ctx_var: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default=None)

def get_request_id() -> str:
    return request_id_ctx_var.get()
