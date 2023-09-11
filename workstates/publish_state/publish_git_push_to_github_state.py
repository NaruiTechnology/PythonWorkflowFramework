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
from workstates.publish_state.publish_git_state import PublishGitState
from datamodel.ApiResponse import ApiResponse
import json
import os
import requests


class publish_git_push_to_github_state(PublishGitState):
    @hierarchyValidation(PublishGitState)
    def DoWork(self):
        relnote_file = '{}/release/release_diff.md'.format(self._config.WorkSpace)
        lineCount = 0
        if os.path.isfile(relnote_file):
            with open(relnote_file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line.rstrip('\n').strip() != '':
                        lineCount += 1
        if lineCount <= 1:
            self._warningMessage = 'There is no release notes with updated MCUs, skip push to GitHub'
        else:
            cwd = os.getcwd()
            try:
                releaseLee = self._parentWorkThread._mcuRelease
                if self._verifyCommitHistoryQueryResults():
                    return

                if len(self._parentWorkThread.LastGitResults) > 0:
                    releaseTag = self._parentWorkThread.LastGitResults[0][0].decode('utf-8')
                else:
                    releaseTag = self._parentWorkThread._tag

                dev_root = '{}/release'.format(self._config.WorkSpace)
                stagingFoler = os.path.realpath('{}/{}'.format(dev_root, self._formatedStagingFolder(releaseLee)))
                if not os.path.isdir(stagingFoler):
                    raise BaseException('Cannot find the path [{}]'.format(stagingFoler))

                os.chdir(stagingFoler)

                # releaseLee['ReleaseTo'] = 'Automation_Testing'

                self._invokeGitCommandline('config', ['user.name', 'mcu-administrator'])
                self._invokeGitCommandline('config', ['user.email', 'mcu_administrator@intel.com'])

                parameters = self.StateConfig['parameters']
                gitHub_folder = parameters[0]  # = [otcshare | intel (for Linux release)]
                tokenConfig = parameters[1]
                github_file = self._formatedReleaseRepoName(releaseLee)
                github_path = 'https://github.com/{}/{}'.format(gitHub_folder, github_file)
                resp = self._invokeGitCommandline('pull', [])
                self._logger.info('Sync Staging repo [{}] response = '.format(os.getcwd(), resp))
                os.chdir(os.path.realpath('../microcode_release-sandbox'))
                resp = self._invokeGitCommandline('pull', [])
                self._logger.info('Sync Sandbox repo [{}] response = '.format(os.getcwd(), resp))

                os.chdir(self.StateConfig['path'])

                resp = self._invokeGitCommandline('push', [github_path])
                resp += self._invokeGitCommandline('push', [github_path, releaseTag])
                if resp != '':
                    self._logger.info('Push to GitHub [{}], response = {}'.format(github_path, str(resp)))

                if tokenConfig.strip() != '':
                    github_token = tokenConfig.strip()
                    release_name = '{} Release'.format(releaseTag)
                    relnote_file = dev_root + "/release_diff.md"
                    url = 'https://api.github.com/repos/{}/{}/releases?access_token={}'\
                        .format(gitHub_folder, github_file, github_token)
                    proxies = {'http': 'http://proxy-chain.intel.com:911',
                               'https': 'https://proxy-chain.intel.com:912'}
                    with open(relnote_file, 'r') as body_file:
                        body_text = body_file.read()
                    releaseJson = {"tag_name": releaseTag,
                                   "target_commitish": "master",
                                   "name": release_name,
                                   "body": body_text,
                                   "draft": False,
                                   "prerelease": False}
                    req = requests.post(url, proxies=proxies, json=releaseJson)
                    if not req.ok:
                        response = ApiResponse(json.dumps(req.json()))
                        # errormsg = 'Push to GitHub failed, error message : [{}], error detail = [{}]'\
                        #    .format(response.message, ' '.join(response.errors[0]))
                        errormsg = 'Push to GitHub failed, error message : [{}]'.format(response.message)

                        self._logger.error(errormsg)
                        raise BaseException(errormsg)
                    else:
                        self._logger.info('Release has been generated on GitHub and an email should have gone out. '
                                          'github_file = [{}], status code = [{}]'.format(github_file, req))
            except Exception as e:
                self._errorMessage = str(e)
                self._success = False
                self._logger.error(str(e))
            finally:
                os.chdir(cwd)
