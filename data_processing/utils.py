import re
import pandas as pd
import sys


def derive_user_agents(args):
    """
    Either creates or passes a valid User-Agent string for
    the requests library to process the GET request

    :param args: The user-input args from __main__
        user_agent (str): Either a valid (found in user_agent_list.csv)
        User-Agent string, or 'None', with valid inputs in the other two
        arguments (--os, --browser).
        --os (str): Executing machine's operating system, lowercase, with
        abbreviations for windows versions (win7, win10, etc.)
        --browser (str): The browser of the executing machine,
        lowercase
    :return derived_user_agent: A string derived from the user input,
    specifying a User-Agent for the GET request
    """
    user_agents_df = pd.read_csv('user_agent_list.csv', index_col=False)
    if args.user_agent == 'None':
        if args.os and args.browser:
            derived_user_agent = user_agents_df.loc[(user_agents_df['os'] == args.os) &
                                                    (user_agents_df['browser'] == args.browser)]['user_agent'].iloc[0]

            if not derived_user_agent:
                sys.exit('User agent not found with arguments provided')
            else:
                print('Detected user_agent: {}'.format(derived_user_agent))
        else:
            sys.exit('Insufficient user_agent arguments provided. Module requires both machine os and browser.')
    else:
        if args.user_agent in user_agents_df['user_agent'].tolist():
            derived_user_agent = args.user_agent
        else:
            sys.exit('Input user_agent not found in list')

    return derived_user_agent


def clean_data(text):
    """
    Takes the text from the website's HTML and extracts the coroner
    records, placing them into a single-column CSV

    :param text: A string of early 20th century coroner records
                derived from the return statement of the GET request
    :return: None
    """
    regex = '<b>(.*?)\n'
    entries = re.findall(regex, text)
    # remove headers
    entries = [x for x in entries if '</b>' in x]
    df = pd.DataFrame({'entry': entries})
    df['entry'] = df['entry'].apply(lambda x: x.replace('</b>', ''))
    df.to_csv('entries.csv', index=False)
    return None
