import time


def info(string):
    print(
        "\033[37m[{}]\033[0m\033[32m[INFO]\033[0m {}".format(
            time.strftime("%H:%M:%S"), string
        )
    )


def debug(string):
    print(
        "\033[37m[{}]\033[0m\033[36m[DEBUG]\033[0m {}".format(
            time.strftime("%H:%M:%S"), string
        )
    )


def warn(string):
    print(
        "\033[37m[{}]\033[0m\033[33m[WARNING]\033[0m {}".format(
            time.strftime("%H:%M:%S"), string
        )
    )


def error(string):
    print(
        "\033[37m[{}]\033[0m\033[31m[ERROR]\033[0m {}".format(
            time.strftime("%H:%M:%S"), string
        )
    )


def fatal(string):
    print(
        "\033[37m[{}]\033[0m\033[7;31;31m[FATAL]\033[0m {}".format(
            time.strftime("%H:%M:%S"), string
        )
    )


def success(string):
    print(
        "\033[37m[{}]\033[0m\033[1m\033[32m[SUCCESS]\033[0m {}".format(
            time.strftime("%H:%M:%S"), string
        )
    )