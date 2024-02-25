import argparse


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--download_type", type=str, default="zip", choices=("zip"))
    parser.add_argument("-o", "--output", type=str, required=True)
    parser.add_argument("-aid", "--album_id", type=str, required=True)
    parser.add_argument("-sid", "--secret_id", type=str)
    parser.add_argument("-v", "--videos", action="store_false")
    parser.add_argument("-s", "--sleep", type=float, default=5.0)

    return parser.parse_args()
