import os
import re
import subprocess

from dotenv import load_dotenv

load_dotenv()

SUDO_PASS = os.getenv("SUDO_PASSWORD")


def helper_list_ufw_rules() -> list:
    cmd = subprocess.run(
        ["sudo", "-S", "ufw", "status", "numbered"],
        input=SUDO_PASS + "\n",
        capture_output=True,
        text=True,
    )

    rules = []

    for line in cmd.stdout.splitlines():
        match = re.match(
            r"\[\s*(\d+)\]\s+(.*?)\s{2,}(ALLOW IN|DENY IN|REJECT IN|ALLOW OUT|DENY OUT)\s{2,}(.*)",
            line,
        )

        if match:
            rule_num, to, action, source = match.groups()

            is_ipv6 = "(v6)" in to
            to = to.replace("(v6)", "").strip()

            rules.append(
                {
                    "id": int(rule_num),
                    "port": to,
                    "action": action,
                    "from": source.strip(),
                    "ipv6": is_ipv6,
                }
            )

    return rules


def helper_add_ufw_rule(port: int, protocol: str, rule: str):
    valid_rules = {"allow", "deny", "reject", "limit"}
    valid_protocols = {"tcp", "udp", ""}

    rule = rule.lower().strip()
    protocol = protocol.lower().strip()

    if rule not in valid_rules:
        raise ValueError("Invalid rule")

    if protocol not in valid_protocols:
        raise ValueError("Invalid protocol")

    if not (1 <= port <= 65535):
        raise ValueError("Invalid port")

    if protocol == "":
        cmd = subprocess.run(
            ["sudo", "-S", "ufw", rule, f"{port}{protocol}"],
            input=SUDO_PASS + "\n",
            capture_output=True,
            text=True,
        )

    else:
        cmd = subprocess.run(
            ["sudo", "-S", "ufw", rule, f"{port}/{protocol}"],
            input=SUDO_PASS + "\n",
            capture_output=True,
            text=True,
        )

    return cmd.stdout, cmd.stderr


def helper_remove_ufw_rule(rule_id: int):
    cmd = subprocess.run(
        ["sudo", "-S", "ufw", "--force", "delete", str(rule_id)],
        input=f"{SUDO_PASS}\n",
        capture_output=True,
        text=True,
    )

    if cmd.returncode != 0:
        raise RuntimeError(cmd.stderr.strip())

    return cmd.stdout.strip()


def helper_enable_firewall():
    cmd = subprocess.run(
        ["sudo", "-S", "ufw", "--force", "enable"],
        input=f"{SUDO_PASS}\n",
        capture_output=True,
        text=True,
    )

    if cmd.returncode != 0:
        raise RuntimeError(cmd.stderr.strip())

    return cmd.stdout.strip()


def helper_disable_firewall():
    cmd = subprocess.run(
        ["sudo", "-S", "ufw", "disable"],
        input=f"{SUDO_PASS}\n",
        capture_output=True,
        text=True,
    )

    if cmd.returncode != 0:
        raise RuntimeError(cmd.stderr.strip())

    return cmd.stdout.strip()


def helper_get_status():
    cmd = subprocess.run(
        ["sudo", "-S", "ufw", "status"],
        input=f"{SUDO_PASS}\n",
        capture_output=True,
        text=True,
    )

    if cmd.returncode != 0:
        raise RuntimeError(cmd.stderr.strip())

    output = cmd.stdout.strip().lower()

    if "status: active" in output:
        return {"status": "active"}
    elif "status: inactive" in output:
        return {"status": "inactive"}

    return {"status": "unknown", "raw": cmd.stdout.strip()}


if __name__ == "__main__":
    print(helper_get_status())
