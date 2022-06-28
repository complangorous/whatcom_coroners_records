import re
import pandas as pd

def clean_data(text):
    regex = '<b>(.*?)\n'
    entries = re.findall(regex, text)
    # remove headers
    entries = [x for x in entries if '</b>' in x]
    df = pd.DataFrame({'entry': entries})
    df.to_csv('entries.csv', index=False)
