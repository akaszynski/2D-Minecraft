import sys
import logging
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='femorph')

    parser.add_argument('--full_screen',
                        help='Run in full screen',
                        action="store_true")

    parser.add_argument(
        '--creative',
        help="No ticks to break blocks",
        action="store_true"
    )
    parser.add_argument('--no_lighting', help="disable lighting", action="store_true")
    parser.add_argument('--window_size', nargs='+', type=int)
    parser.add_argument('--seed', type=int)
    parser.add_argument(
        '--logging',
        help='enable logging',
        action="store_true"
    )
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

    from data import variables
    if args.seed is not None:
        if args.seed < 0:
            raise ValueError("Seed must be between 1 and 99999")
        variables.SEED = args.seed

    from game import main
    main(
        full_screen=bool(args.full_screen),
        window_size=args.window_size,
        creative=bool(args.creative),
        lighting=not bool(args.no_lighting)
    )
