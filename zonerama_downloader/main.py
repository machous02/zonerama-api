from zonerama_downloader.parse_arguments import parse, args_t
from zonerama_downloader.classes.zonerama_album import ZoneramaAlbum


def run_zip(args: args_t) -> None:
    album = ZoneramaAlbum(args.album_id, None, args.secret_id)
    album.download(destination_folder=args.output, include_videos=args.videos, sleep_for=args.sleep)


def main():
    args = parse()

    match args.download_type:
        case "zip":
            run_zip(args)
        case _:
            assert False


if __name__ == "__main__":
    main()
