import requests
import argparse
import utils


def main():
    # prompt for user agent w/ argparse but allow for None so user can do a dry run to see if that works
    parser = argparse.ArgumentParser()
    parser.add_argument('user_agent', type=str, help='The agent-user employed by requests to parse a response; '
                                                     'typically consisting of an OS and a browser. Use "None" for a '
                                                     'dry-run.')
    parser.add_argument('--os', type=str, help='Operating System: chromeos (Chrome OS), osx (Mac OS X), '
                                               'Windows (win7, win10, etc.')
    parser.add_argument('--browser', type=str, help='Browser: chrome (Chrome), safari (Safari), edge (Edge)')
    args = parser.parse_args()

    derived_user_agent = utils.derive_user_agents(args)
    # get text from page
    url = 'http://wagenweb.org/whatcom/misc/coroner.htm'
    response = requests.get(url=url, headers={'User-Agent': derived_user_agent})
    utils.clean_data(response.text)


if __name__ == '__main__':
    main()
