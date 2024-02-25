from zonerama_downloader.download_album import download_album
from zonerama_downloader.parse_arguments import parse, args_t


def run_zip(args: args_t) -> None:
    download_album(
        album_id=args.aid, secret_id=args.sid, include_videos=args.v, sleep_for=args.s
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
