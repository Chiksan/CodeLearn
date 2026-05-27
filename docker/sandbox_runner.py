import sys
import io
import json
import traceback
import signal


def run_code(code: str) -> dict:
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()
    try:
        exec(compile(code, "<sandbox>", "exec"), {})
        output = sys.stdout.getvalue()
        error = sys.stderr.getvalue()
    except Exception:
        output = sys.stdout.getvalue()
        error = traceback.format_exc()
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
    return {"output": output, "error": error}


def timeout_handler(signum, frame):
    raise TimeoutError("Превышено время выполнения")


if __name__ == "__main__":
    signal.signal(signal.SIGALRM, timeout_handler)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
            code = request.get("code", "")
            signal.alarm(5)
            result = run_code(code)
            signal.alarm(0)
        except TimeoutError:
            result = {"output": "", "error": "Превышено время выполнения (5 сек)"}
        except Exception as e:
            result = {"output": "", "error": str(e)}

        print(json.dumps(result), flush=True)
