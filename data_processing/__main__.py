import sys
import requests
import pandas as pd
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

    derived_user_agent = None
    print(type(args.user_agent), args.user_agent)
    if args.user_agent == 'None':
        print('boo')
        if args.os and args.browser:
            user_agents_df = pd.read_csv('user_agent_list.csv', index_col=False)
            derived_user_agent = user_agents_df.loc[(user_agents_df['os'] == args.os) &
                                                    (user_agents_df['browser'] == args.browser)]['user_agent'].iloc[0]

            if not derived_user_agent:
                sys.exit('User agent not found with arguments provided')
            else:
                print('Detected user_agent: {}'.format(derived_user_agent))
        else:
            sys.exit("Insufficient user_agent arguments provided. Module requires both machine os and browser.")


    # get text from page
    url = 'http://wagenweb.org/whatcom/misc/coroner.htm'
    response = requests.get(url=url) if args.user_agent == 'None' else requests.get(url=url, headers={
        'User-Agent': args.user_agent})
    utils.clean_data(response.text)


if __name__ == '__main__':
    main()
