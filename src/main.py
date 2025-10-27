# src/main.py
import argparse
from src.nodes.base_node import BaseNode
from src.utils.config import PEERS  # masih bisa kita ambil dari config

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Distributed Node Runner")
    parser.add_argument("--node", type=str, default="node1", help="Node ID (ex: node1, node2)")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host address")
    parser.add_argument("--port", type=int, default=8000, help="Port number")
    args = parser.parse_args()

    node = BaseNode(args.node, args.host, args.port, PEERS)
    print(f"🚀 Starting node {args.node} at {args.host}:{args.port}")
    node.run()

