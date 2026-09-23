"""Interface en ligne de commande d'InfraWatch."""
from __future__ import annotations

import argparse
import json
import sys

from .monitor import take_snapshot
from .report import render_html


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="infra-watch",
        description="Monitoring et audit d'infrastructure léger.",
    )
    parser.add_argument("--services", nargs="*", default=[],
                        help="Services systemd à vérifier (ex: ssh nginx)")
    parser.add_argument("--disks", nargs="*", default=["/"],
                        help="Points de montage à auditer")
    parser.add_argument("--format", choices=["json", "html"], default="json")
    parser.add_argument("--output", "-o", help="Fichier de sortie (stdout sinon)")
    args = parser.parse_args(argv)

    snapshot = take_snapshot(services=args.services, disk_paths=args.disks)

    if args.format == "html":
        content = render_html(snapshot)
    else:
        content = json.dumps(snapshot.to_dict(), indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Rapport écrit dans {args.output}", file=sys.stderr)
    else:
        print(content)
    return 0 if snapshot.worst_status != "critical" else 2


if __name__ == "__main__":
    raise SystemExit(main())
