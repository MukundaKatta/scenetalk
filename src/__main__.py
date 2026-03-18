"""CLI for scenetalk."""
import sys, json, argparse
from .core import Scenetalk

def main():
    parser = argparse.ArgumentParser(description="SceneTalk — AI Image Describer for Blind Users. Generate detailed scene descriptions for visually impaired users.")
    parser.add_argument("command", nargs="?", default="status", choices=["status", "run", "info"])
    parser.add_argument("--input", "-i", default="")
    args = parser.parse_args()
    instance = Scenetalk()
    if args.command == "status":
        print(json.dumps(instance.get_stats(), indent=2))
    elif args.command == "run":
        print(json.dumps(instance.generate(input=args.input or "test"), indent=2, default=str))
    elif args.command == "info":
        print(f"scenetalk v0.1.0 — SceneTalk — AI Image Describer for Blind Users. Generate detailed scene descriptions for visually impaired users.")

if __name__ == "__main__":
    main()
