import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='femorph')

    parser.add_argument('--full_screen',
                        help='Run in full screen',
                        action="store_true")

    args = parser.parse_args()

    from game import main
    main(full_screen=bool(args.full_screen))
