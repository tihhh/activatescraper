
ERROR_LOG = "errors/errors.txt"

#def not the best logger but it works for me
def log_error(url, status_code, content):
    with open(ERROR_LOG, "a", encoding="utf-8") as f:
        f.write(f"{url}\nStatus: {status_code}\n{content[:500]}\n\n")