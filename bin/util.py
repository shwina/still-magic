'''
Utilities.
'''

def report(title, group, values):
    '''Report missing/unused values.'''

    if values:
        print('{}: {}'.format(title, group))
        for v in sorted(values):
            print('  ', v)
