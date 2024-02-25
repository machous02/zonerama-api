from zonerama_downloader.download_album import download_album
from zonerama_downloader.parse_arguments import parse, args_t


def run_zip(args: args_t) -> None:
    download_album(
        album_id=args.album_id, secret_id=args.secret_id, include_videos=args.videos, sleep_for=args.sleep
    )


def main():
    args = parse()

    match args.download_type:
        case "zip":
            run_zip(args)
        case _:
            assert False


if __name__ == "__main__":
    main()
