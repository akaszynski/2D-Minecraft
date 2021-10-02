import sys
import logging
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='femorph')

    parser.add_argument('--full_screen',
                        help='Run in full screen',
                        action="store_true")

    parser.add_argument('--window_size', nargs='+', type=int)
    parser.add_argument('--logging',
                        help='Run in full screen',
                        action="store_true")
    args = parser.parse_args()

    if args.logging:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                # logging.FileHandler("debug.log"),
                logging.StreamHandler()
            ]
        )

    from game import main
    main(full_screen=bool(args.full_screen), window_size=args.window_size)
