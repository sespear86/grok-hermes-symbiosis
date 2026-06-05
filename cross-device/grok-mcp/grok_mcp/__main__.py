"""Entry: python -m grok_mcp (Hermes: hermes mcp add grok --args -m grok_mcp)."""

from grok_mcp.server import run_stdio


def main() -> None:
    run_stdio()


if __name__ == "__main__":
    main()