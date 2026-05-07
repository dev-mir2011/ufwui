import re
import subprocess


def helper_list_ufw_rules(sudo_pass: str) -> list:
    cmd = subprocess.run(
        ["sudo", "-S", "ufw", "status", "numbered"],
        input=sudo_pass + "\n",
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


if __name__ == "__main__":
    print(helper_list_ufw_rules("mir"))
