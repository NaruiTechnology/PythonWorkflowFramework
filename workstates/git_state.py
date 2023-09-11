#-------------------------------------------------------------------------------
# This file contains 'Framework Code' and is licensed as such
# under the terms of your license agreement with Intel or your
# vendor. This file may not be modified, except as allowed by
# additional terms of your license agreement.
#
## @file
#
# Copyright (c) 2019, Intel Corporation. All rights reserved.
# This software and associated documentation (if any) is furnished
# under a license and may only be used or copied in accordance
# with the terms of the license. Except as permitted by such
# license, no part of this software or documentation may be
# reproduced, stored in a retrieval system, or transmitted in any
# form or by any means without the express written consent of
# Intel Corporation.
#-------------- -----------------------------------------------------------------
from buildingblocks.decorators import hierarchyValidation
from workstates.popen_state import POpenState
from datamodel.definitions import Consts
import subprocess
import os
import re


class GitState(POpenState):
    @hierarchyValidation(POpenState)
    def DoWork(self):
        self._invokeSubprocess()

    @hierarchyValidation(POpenState)
    def _invokeSubprocess(self):
        gitCommand = list()
        lines = list()
        cwd = os.getcwd()
        try:
            workfolder = self.StateConfig['path']
            if self._isGitRepo(workfolder):
                os.chdir(workfolder)
                gitCommand.append(self.StateConfig['command'])
                parameters = self.StateConfig[Consts.PARAMETERS]
                if isinstance(parameters, list) and len(self.StateConfig[Consts.PARAMETERS]):
                    gitCommand = gitCommand + parameters
                msg = 'Call git command [{}]'.format(' '.join(gitCommand))
                resp = subprocess.Popen(gitCommand,
                                        stdout=subprocess.PIPE,
                                        shell=False).communicate()[0]
                password = self._parentWorkThread._password
                if password is not None:
                    msg = msg.replace(password, '******')
                self._logger.info(msg)
                for line in resp.split(b'\n'):
                    # self._logger.info(line.rstrip())
                    lines.append(line.strip(b'"'))
            else:
                self._logger.error('The directory [{}] is not a git repo'.format(workfolder))
                self._success = False
        except Exception as e:
            self._success = False
            self._logger.error(str(e))
        finally:
            os.chdir(cwd)
        return lines

    @hierarchyValidation(POpenState)
    def _dryRun(self):
        gitCommand = list()
        gitCommand.append(self.StateConfig['command'])
        parameters = self.StateConfig[Consts.PARAMETERS]
        if isinstance(parameters, list) and len(self.StateConfig[Consts.PARAMETERS]):
            gitCommand = gitCommand + parameters
        self._logger.info('Dry run - git command [{}]'.format(' '.join(gitCommand)))

    def _isGitRepo(self, path='.'):
        if path is None or path is '' or not os.path.isdir(path):
            return False
        return subprocess.call(['git', '-C', path, Consts.STATUS],
                               stderr=subprocess.STDOUT,
                               stdout=open(os.devnull, 'w')) == 0

    def _gitClone(self, repo):
        repoUrl = repo # repo.replace('$username$', getpass.getuser())
        self._logger.info('Clone the repo {}'.format(repoUrl))
        resp = subprocess.Popen(['git', 'clone', repoUrl, '-q'],
                                stdout=subprocess.PIPE,
                                shell=True).communicate()[0]
        if resp.strip() != b'':
            self._success = False
            error = list()
            for line in resp.split(b'\n'):
                error.append(line.rstrip())
                self._logger.info(error)
            raise Exception(error)

    def _gitStagedFiles(self):
        resp = subprocess.Popen(['git', Consts.STATUS],
                                stdout=subprocess.PIPE,
                                shell=False).communicate()[0]
        return [re.sub(r'^.\s+', '',
                       re.sub(Consts.REGEX_GIT_STATUS_NEW_PATTERN, '',
                       re.sub(Consts.REGEX_GIT_STATUS_REPLACE_PATTERN, '', x.lstrip('\t'))))
                for x in resp.decode('utf-8').split('\n') if not x.lstrip().lstrip('\t').startswith('deleted')]

    def _gitSortedStagedFiles(self):
        newfiles = list()
        modifiedfiles = list()
        deletedfiles = list()
        resp = subprocess.Popen(['git', Consts.STATUS],
                                stdout=subprocess.PIPE,
                                shell=False).communicate()[0]
        for line in resp.decode('utf-8').split('\n'):
            x = line.lstrip().lstrip('\t')
            if re.match(Consts.REGEX_GIT_STATUS_NEW_PATTERN, x):
                newfiles.append(re.sub(Consts.REGEX_GIT_STATUS_REPLACE_PATTERN, '', x).strip())
            elif re.match(Consts.REGEX_GIT_STATUS_MODIFIED_PATTERN, x):
                modifiedfiles.append(re.sub(Consts.REGEX_GIT_STATUS_REPLACE_PATTERN, '', x).strip())
            elif re.match(Consts.REGEX_GIT_STATUS_DELETED_PATTERN, x):
                deletedfiles.append(re.sub(Consts.REGEX_GIT_STATUS_REPLACE_PATTERN, '', x).strip())
        return newfiles, modifiedfiles, deletedfiles

    def _gitCommitStagedFiles(self, comments=''):
        cwd = os.getcwd()
        try:
            workfolder = self.StateConfig['path']
            if self._isGitRepo(workfolder):
                os.chdir(workfolder)
                newfiles, modifiedfiles, deletedfiles = self._gitSortedStagedFiles()
                if len(modifiedfiles):
                    for f in modifiedfiles:
                        self._gitAddFile(f)
                if len(newfiles) + len(modifiedfiles) + len(deletedfiles) > 0:
                    self._gitCommit(comments=comments)
            else:
                self._logger.error('The directory [{}] is not a git repo - {}'.format(workfolder))
                self._success = False
        except Exception as e:
            self._success = False
            self._logger.error(str(e))
        finally:
            os.chdir(cwd)

    def _invokeGitCommandline(self, command, parameterss):
        commandLine = ['git', command]
        if isinstance(parameterss, list):
            commandLine = commandLine + parameterss
        resp = subprocess.Popen(commandLine,
                                stdout=subprocess.PIPE,
                                shell=False).communicate()[0]
        resp = resp.decode('utf-8')
        self._logger.info('Call git command {}, response = {}.\n'.format(' '.join(commandLine), resp))
        return resp

    def _gitPull(self):
        return str(self._invokeGitCommandline('pull', ['--quiet', '--verbose']))

    def _gitAddFile(self, file):
        path = '{}/{}'.format(os.getcwd(), file)
        return str(self._invokeGitCommandline('add', [path]))

    def _gitCommit(self, comments=''):
        return str(self._invokeGitCommandline('commit', ['-m', comments]))

    def _gitCreateTag(self, tag, comments=''):
        return str(self._invokeGitCommandline('tag', ['-f', '-a', tag, '-m', comments]))

    def _gitPush(self):
        self._invokeGitCommandline('push', ['-f'])
        return str(self._invokeGitCommandline('push', ['--tags']))

    def _gitCurrentCommit(self):
        return str(self._invokeGitCommandline('log', ['-1', '--pretty=format:"%H %D"']))

    def _gitGetParents(self):
        resp = subprocess.Popen(['git', 'log', '--parents', '--pretty=format:"%H %D"'],
                                stdout=subprocess.PIPE,
                                shell=False).communicate()[0]
        parents = tuple([tuple(x.replace('tag: '.encode('utf-8'), b'').strip().split(b' '))
                         for x in resp.split(b'\n')
                         if len(x.split(b' ')[1]) > 2])
        return parents

    def _gitGetChildren(self):
        resp = subprocess.Popen(['git', 'log', '--children', '--pretty=format:"%H %D"'],
                                stdout=subprocess.PIPE,
                                shell=False).communicate()[0]
        children = tuple([tuple(x.replace('tag: '.encode('utf-8'), b'').strip().split(b' '))
                         for x in resp.split(b'\n')
                         if len(x.split(b' ')[1]) > 2])
        return children

    def _queryLog(self):
        cwd = os.getcwd()
        try:
            searchpattern = self._parentWorkThread._mcuRelease['ReleaseTo']
            workfolder = self.StateConfig['path']
            os.chdir(workfolder)
            self._parentWorkThread.LastGitResults = self._gitQueryCommitHistory(searchpattern)
            if len(self._parentWorkThread.LastGitResults) == 0:
                self._logger.warning('Query release history of {} and no commit been found.'.format(searchpattern))
            else:
                for item in self._parentWorkThread.LastGitResults[0:10]:
                    self._logger.info('Query release history of {}, results = {}'.
                                      format(searchpattern, b' : '.join(item)))
            pass
        except Exception:
            self._errorMessage = \
                'Could not find any commit log with tags in format of [yyyyMMdd_{0}] (e.g. 20191023_{0})'\
                .format(searchpattern)
            self._success = False
            self._logger.error(self._errorMessage)
        finally:
            os.chdir(cwd)

    def _gitQueryCommitHistory(self, searchpattern):
        comitHistory = self._invokeSubprocess()
        filteredHistory = [tuple(x.replace('HEAD -> master, tag: '.encode('utf-8'), b'').strip().split(b' '))
                           for x in comitHistory
                           if len(re.findall(searchpattern.encode('utf-8'), x)) > 0]

        for i in range(0, len(filteredHistory)):
            if len(filteredHistory[i]) == 2:
                continue

            filteredHistory[i] = [n for n in filteredHistory[i]
                                  if len(re.findall('([a-f0-9]{40})|((([0-9]{8})|(\w+)?)_(\w+))'.encode('utf-8'), n)) > 0]
            # if len(re.findall('([a-f0-9]{40})|(([0-9]{8})_(\w+))'.encode('utf-8'), n)) > 0]
            reversed(filteredHistory[i])

        filteredHistory = [x[:2] for x in filteredHistory]
        dic = dict((y.replace(b',', b''), x) for x, y in filteredHistory)
        # return sorted(dic.items(), key=lambda kv: (kv[0], kv[1]), reverse=True)
        results = list()
        for k, v in dic.items():
            results.append(tuple([k, v]))
        return results


