"""
This script is based on https://github.com/korvoj/signposting/blob/1.0.1/entrypoint.py

It has been modified to cover GitLab Pages instead of GitHub Pages.
"""
import json
import os
import urllib.parse
import argparse
import yaml
from wcmatch import glob
import requests

argument_parser = argparse.ArgumentParser(description='Signposting linkset generator')
argument_parser.add_argument('--default-branch', type=str, default='main')
argument_parser.add_argument('--default-profile', type=str, required=True)
argument_parser.add_argument('--exclusions-file', type=str, default='mkdocs.yml')
argument_parser.add_argument('--root-dir', type=str, default='resources')
argument_parser.add_argument('--gl-repository-url', type=str, required=True)
argument_parser.add_argument('--pages-url', type=str, required=True)
args = argument_parser.parse_args()

DEFAULT_BRANCH = args.default_branch
PAGES_URL = args.pages_url
DEFAULT_PROFILE_DISCOVERED_ITEMS = args.default_profile
EXCLUSIONS_FILE_PATH = args.exclusions_file
ROOT_DIR_PATH = args.root_dir
GITLAB_REPOSITORY_URL = args.gl_repository_url
BLOB_CONTENT_URL = f'{GITLAB_REPOSITORY_URL}/-/blob'
RAW_CONTENT_URL = f'{GITLAB_REPOSITORY_URL}/-/raw'


class SignPost:
    def __init__(self, href, type=None, profile=None):
        self.href = href
        self.type = type
        self.profile = profile

    def __repr__(self):
        str_representation = f'href: {self.href}'
        if self.type is not None:
            str_representation += f' type: {self.type}'
        if self.profile is not None:
            str_representation += f' profile: {self.profile}'
        return str_representation

    def to_json(self):
        json_representaton = dict()
        json_representaton['href'] = self.href
        if self.type is not None:
            json_representaton['type'] = self.type
        if self.profile is not None and str.strip(self.profile) != '':
            json_representaton['profile'] = self.profile
        return json_representaton


def read_exclusions_file(exclusions_file_path):
    with open(exclusions_file_path) as stream:
        try:
            yaml_exclusions = yaml.safe_load(stream)
            return yaml_exclusions.get('signposting_exclusions', [])
        except yaml.YAMLError as err:
            print('An error has occurred: ', err)


def fetch_files(root_dir, exclusions):
    url_list = []
    markdown_files = glob.glob(patterns='**/**.md', root_dir=root_dir,
                               exclude=exclusions, flags=glob.GLOBSTAR)
    for markdown_file in markdown_files:
        # print(markdown_file)
        url_encoded_path = urllib.parse.quote(markdown_file)
        if root_dir and root_dir != '':
            url_list.append(
                f'{BLOB_CONTENT_URL}/{DEFAULT_BRANCH}/{root_dir}/{url_encoded_path}')
        else:
            url_list.append(
                f'{BLOB_CONTENT_URL}/{DEFAULT_BRANCH}/{url_encoded_path}')

    return url_list


def parse_citation_cff_authors(citation_cff):
    orcids = [SignPost(href=i['orcid'], type=None) for i in citation_cff.get('authors', []) if
              i.get('orcid') is not None]
    return orcids


def parse_citation_cff_license(citation_cff):
    response = requests.get('https://raw.githubusercontent.com/spdx/license-list-data/main/json/licenses.json')
    if response.status_code != 200:
        print('Error fetching license list, status code: ', response.status_code)
        return
    license_list = response.json().get('licenses', [])
    cff_license = citation_cff.get('license')
    if cff_license is not None:
        for i in license_list:
            if i.get('licenseId', '') == cff_license:
                return SignPost(href=i.get('reference'), type=None)
    raise Exception('No license mapping to SPDX possible')


def parse_citation_cff_repository(citation_cff):
    repository_url = citation_cff.get('repository')
    return SignPost(href=repository_url, type='text/html')


def parse_citation_cff_related(citation_cff):
    doi = citation_cff.get('doi', '')
    doi = f'https://doi.org/{doi}'
    return SignPost(href=doi, type='text/html')


def construct_types():
    return [
        SignPost(href='https://schema.org/LearningResource', type=None),
        SignPost(href='https://schema.org/AboutPage', type=None)
    ]


def construct_described_by():
    return [
        SignPost(type='application/yaml', profile='https://citation-file-format.github.io/1.2.0/schema.json',
                 href=f'{RAW_CONTENT_URL}/{DEFAULT_BRANCH}/CITATION.cff')
    ]


def construct_items(files):
    signposts = []
    for file in files:
        signpost = SignPost(href=file, type='text/markdown', profile=DEFAULT_PROFILE_DISCOVERED_ITEMS)
        signposts.append(signpost)
    return signposts


def generate_linkset(root_dir, exclusions):
    citation_cff = ''
    with open('CITATION.cff') as stream:
        try:
            citation_cff = yaml.safe_load(stream)
        except yaml.YAMLError as err:
            print('An error has occurred: ', err)
            return
    authors = parse_citation_cff_authors(citation_cff)
    spdx_license = parse_citation_cff_license(citation_cff)
    item_repository_url = parse_citation_cff_repository(citation_cff)
    related = parse_citation_cff_related(citation_cff)
    types = construct_types()
    described_by = construct_described_by()
    discovered_files = fetch_files(root_dir=root_dir, exclusions=exclusions)
    all_items = construct_items(discovered_files)
    all_items.append(item_repository_url)

    json_linkset = {
        'linkset': [
            {
                'anchor': PAGES_URL,
                'type': [i.to_json() for i in types],
                'author': [i.to_json() for i in authors],
                'item': [i.to_json() for i in all_items],
                'describedby': [i.to_json() for i in described_by],
                'license': [spdx_license.to_json()],
                'related': [related.to_json()]
            }
        ]
    }

    with open('linkset.json', 'w') as f:
        json.dump(json_linkset, f)
    # print(json_linkset)


if __name__ == '__main__':
    exclusions = read_exclusions_file(EXCLUSIONS_FILE_PATH)
    generate_linkset(root_dir=ROOT_DIR_PATH, exclusions=exclusions)
