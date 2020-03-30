import argparse
import re
import sys


def check(name):
    """Check a git branch name against gitflow naming conventions.

    This is most likely the function you are looking for.

    """
    if name in (  # First level only branches
            'master',
            'develop',
    ):
        return True
    elif len(name.split('/')) == 2:
        # some have two levels separated by /
        return checkSecondLevel(name)
    else:
        # Default
        print(f'Error: Did not recognise "{name}" as a valid branch.')
        return False


def checkLen(string, min_len, max_len):
    if len(string) < min_len:
        print(
            f'Error: {string} is too short'
            f' (it is {len(string)}, minimum is {min_len})'
        )
        return False
    if len(string) > max_len:
        print(
            f'Error: {string} is too long'
            f' (it is {len(string)}, maximum is {max_len})'
        )
        return False
    else:
        return True


def checkSecondLevel(name):
    """Checks the name to be a valid gitflow branch name containing a `/`.

    This is intended for internal use, and asumes a single `/` to be
    present in `name`.

    """
    category, label = name.split('/')

    if category in (  # valid categories
            'feature',
            'hotfix',
    ):
        return checkLabel(label)
    elif category in (  # Not currently validating release branch names
            'release',
    ):
        return True
    else:
        print(f'Error: Did not recognise "{category}" as a valid category')
        return False


def checkLabel(label):
    """Checks the label to have a description of one or more words
    (lowercase alphanumerics), joined by a dash (`-`), followed by an
    issue reference.

    Example: word-and-numb3r-#1

    """
    # Description
    desc_re = r'(?P<description>[a-z0-9]+(?:-[a-z0-9]+)*)'  # one or more words
    desc_re = r'^' + desc_re  # must be at begining
    m = re.search(desc_re, label)
    if not m:
        print(
            f'Error: No valid description in "{label}"'
            f' (Expected it to start with lowercase alphanumeric and dashes'
            f' like this: ex4mple-description)'
        )
        return False

    if not checkLen(m.groupdict()['description'], 10, 25):
        return False

    # Issue reference
    issue_re = r'(?P<issue>#[0-9]+)'  # hashtag and integer
    issue_re = issue_re + r'$'  # must be at end
    if not re.search(issue_re, label):
        print(
            f'Error: No issue reference in "{label}"'
            f' (Expected it to in like this: ...-#1)'
        )
        return False

    # Dash seperator
    label_re = desc_re + r'-' + issue_re
    if not re.search(label_re, label):
        print(
            f'Error: Missing dash between description and issue reference '
            f' in "{label}"'
        )
        return False

    return True  # no problems found


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Validate branch name according to gitflow',
    )
    parser.add_argument(
        '-t', '--test', dest='test', action='store_const',
        const=True, default=False,
        help='Run the built in tests and exit',
    )
    parser.add_argument(
        'name', metavar='NAME', type=str,
        help='The branch name to check'
    )
    args = parser.parse_args()

    if not args.test:
        success = check(args.name)
        sys.exit(not success)

    print('Starting built-in self-testing')
    print('Expect error messages, but not AssertionError\'s')
    assert check('master')
    assert check('develop')
    assert not check('random')  # no custom at top level
    assert not check('alkshjdg')  # no custom at top level
    assert not check('master/asdasdasdasdasdasd')  # nothing below master
    assert not check('develop/asdasdasdasdasdas')  # nothing below develop
    assert check('feature/some-feature-#9')  # good
    assert not check('feature/2-shrt-fe#1')  # too short
    assert not check('feature/very-long-description-here-#1')  # too long
    print('Done - either all tests passed or you disable `assert`')
