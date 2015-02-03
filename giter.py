#!/usr/bin/env python

import os
import logging

from github import Github
from github.GithubException import UnknownObjectException, GithubException


class Orginfo:
    def __init__(self, github_token=None):
        if github_token:
            self.github_token = github_token
        elif os.environ.get('GITHUB_TOKEN', None):
            self.github_token = os.environ['GITHUB_TOKEN']
        self.gh_instance = Github(self.github_token)

    def _get_org_repos(self, org_name):
        g = self.gh_instance
        org = g.get_organization(org_name)
        return org.get_repos()

    def get_org_repos(self, org_name):
        repos = self._get_org_repos(org_name)
        return [repo.name for repo in repos]

    def get_prod_repos(self, org_name):
        repos = self._get_org_repos(org_name)
        for repo in repos:
            try:
                # skip repos with no 'circle.yml' file
                if repo.get_contents('circle.yml'):
                    yield repo.name
            except (UnknownObjectException, GithubException):
                # no 'circle.yml', so don't return this one
                logging.info(
                    'skipping repo {}; no circle.yml'.format(repo.name))
                pass

if __name__ == '__main__':
    org = Orginfo()
    for repo in org.get_prod_repos('rackspace-orchestration-templates'):
        print repo
