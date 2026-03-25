import argparse

import pipeline


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--user_nl_request", required=True)
    args = parser.parse_args()
    response = pipeline.run_pipeline(args.user_nl_request)
    print(response)


if __name__ == "__main__":
    main()
