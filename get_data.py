#!/usr/bin/env python
import json
from subprocess import PIPE, Popen
from collections import defaultdict

# Path to project
cwd = '/Users/alex/my_project/'

author_names = {
    '<alex@louden.com>': 'Alex',
    # ...
}


def make_chart(cwd):
    files = get_git_files()
    total_author_lines = defaultdict(int)

    for filename in files:
        print filename
        blame = get_git_blame(filename)
        author_lines = count_lines_per_author(blame)
        for author, lines in author_lines.iteritems():
            total_author_lines[author] += lines

    print dict(total_author_lines)
    total_author_name_lines = defaultdict(int)

    # Emails to names
    for author_email, lines in total_author_lines.iteritems():
        author_name = author_names.get(author_email)
        total_author_name_lines[author_name] += lines

    data = []
    for name, line_count in total_author_name_lines.iteritems():
        data.append({
            'label': name,
            'value': line_count
        })

    return data


def count_lines_per_author(blame):
    author_lines = defaultdict(int)

    for line in blame:
        if not line.startswith('author-mail '):
            continue
        author = line.split()[1]
        author_lines[author] += 1

    return author_lines


def get_git_blame(filename):
    command = ['git', 'blame', '--line-porcelain', filename]
    return run_command(command).splitlines()


def get_git_files():
    command = ['git', 'ls-files']
    return run_command(command).splitlines()


def run_command(command):
    pipe = Popen(command, cwd=cwd, bufsize=-1, stdout=PIPE)
    return pipe.communicate()[0]


if __name__ == '__main__':
    data = make_chart(cwd)
    print ''
    print json.dumps(data)
