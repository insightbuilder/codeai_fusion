from . import server
import asyncio


def main():
    """Main entry point"""
    asyncio.run(server.main())


__all__ = ["main", "server"]
