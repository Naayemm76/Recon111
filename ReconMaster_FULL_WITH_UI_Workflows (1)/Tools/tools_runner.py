
import subprocess
import shlex

# Define supported tools and their basic command templates
SUPPORTED_TOOLS = {
    "nmap": "nmap -sV {target}",
    "theHarvester": "theHarvester -d {target} -b all",
    "sublist3r": "sublist3r -d {target}",
    "amass": "amass enum -d {target}",
    "dnsenum": "dnsenum {target}",
    "whois": "whois {target}",
    "gobuster": "gobuster dir -u http://{target} -w /usr/share/wordlists/dirb/common.txt",
    "whatweb": "whatweb {target}",
    "nikto": "nikto -host {target}"
}

def run_tool(tool_name, target):
    if tool_name not in SUPPORTED_TOOLS:
        return {"error": f"Tool '{tool_name}' is not supported."}

    command = SUPPORTED_TOOLS[tool_name].format(target=shlex.quote(target))
    try:
        result = subprocess.run(shlex.split(command), capture_output=True, text=True, timeout=120)
        return {
            "command": command,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"error": f"Execution of '{tool_name}' timed out."}
    except Exception as e:
        return {"error": str(e)}
