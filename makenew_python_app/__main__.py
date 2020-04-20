import asyncio
import platform

from . import create_dependencies, boot


def main():
    boot(create_dependencies)


if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    main()
