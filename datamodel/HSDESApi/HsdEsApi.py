import requests
from requests_kerberos import HTTPKerberosAuth
from datamodel.ApiResponse import ApiResponse
from datamodel.HSDESApi.HsdApiPayload import HsdApiQueryPayload
import urllib3
import json
import os


class HsdEsApi(object):
    def __init__(self, restApiUrl):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.__headers = {'Content-type': 'application/json'}
        self.__restApiUrl = restApiUrl
        self.__lasterror = None

    @property
    def LastError(self):
        return self.__lasterror

    @property
    def Header(self):
        return self.__headers

    def GetArticle(self, articleID):
        success = False
        response = None
        for i in range(0, 3):
            if success:
                break
            try:
                url = '{}/article/{}'.format(self.__restApiUrl, articleID)
                resp = requests.get(url, verify=False, auth=HTTPKerberosAuth(), headers=self.Header)
                response = ApiResponse(json.dumps(resp.json()))
                success = True
            except BaseException as e:
                print(str(e))
                self.__init__()

        return response

    def GetRefLinks(self, articleID):
        response = None
        try:
            url = '{}/article/{}/links'.format(self.__restApiUrl, articleID)
            resp = requests.get(url, verify=False, auth=HTTPKerberosAuth(), headers=self.Header)
            response = ApiResponse(json.dumps(resp.json()))
        except BaseException as e:
            print(str(e))
        return response

    def Query(self, payload):
        url = '{}/query/{}'.format(self.__restApiUrl, str(payload))
        response = requests.get(url, verify=False, auth=HTTPKerberosAuth(), headers=self.Header)
        if response is not None and response.ok:
            jsonString = json.dumps(response.json())
            ret = ApiResponse(jsonString)
            if response.status_code > 200:
                self.__lasterror = response.content.decode('utf-8')
                return None
            return ret
        return None

    def QueryAll(self, queryId):
        start = 1
        end = 1
        payload = HsdApiQueryPayload(str(queryId))
        payload['start_at'] = str(start)
        payload['max_results'] = str(end)
        response = self.Query(payload)

        if response is not None:
            end = response.total
            payload = HsdApiQueryPayload(str(queryId))
            payload['start_at'] = str(start)
            payload['max_results'] = str(end)
            return self.Query(payload)
        return None

    def DownloadAttachment(self, articleId, savepath):
        article = self.GetArticle(articleId)
        if article is not None:
            data = article.data[0]
            url = '{}/article/{}/children?' \
                  'tenant={}&child_subject=attachment'.format(self.__restApiUrl, data['id'], data['tenant'])
            response = requests.get(url, verify=False, auth=HTTPKerberosAuth(), headers=self.Header)
            if response is not None:
                results = ApiResponse(json.dumps(response.json()))
                if os.path.isdir(savepath):
                    try:
                        f = os.path.realpath('{}/{}'.format(savepath, results.data[0]['document.file_name']))
                        with open(f, 'wb') as w:
                            w.write(response.content)
                    except IOError as e:
                        return str(e)
        return None

    def DownloadAttachment(self, articleId, filetype, savepath):
        filename, content = self.GetAttachment(articleId, filetype)
        if filename is not None and filetype != '' and content is not None:
            if filename is not None and filetype != '' and content is not None:
                if os.path.isdir(savepath):
                    try:
                        f = os.path.realpath('{}/{}'.format(savepath, filename))
                        with open(f, 'wb') as w:
                            w.write(content)
                    except IOError as e:
                        return str(e)
        return None

    def GetAttachment(self, articleId, filetype):
        fileName = None
        downloadResponse = None
        article = self.GetArticle(articleId)
        if article is not None:
            data = article.data[0]
            url = '{}/article/{}/children?' \
                  'tenant={}&child_subject=attachment'.format(self.__restApiUrl, data['id'], data['tenant'])
            response = requests.get(url, verify=False, auth=HTTPKerberosAuth(), headers=self.Header)
            if response is not None:
                results = ApiResponse(json.dumps(response.json()))

                if not(results.data is None or len(results.data) == 0):
                    idx = 0
                    fileName = None
                    for i in range(0, len(results.data)):
                        item = results.data[i]
                        f = item['document.file_name']
                        if f.lower().endswith(filetype.lower()):
                            idx = i
                            fileName = f
                            break
                    try:
                        downloadUrl = '{}/binary/{}?verbose=true'.format(self.__restApiUrl, results.data[idx]['id'])
                        downloadResponse = requests.get(downloadUrl,
                                                        verify=False, auth=HTTPKerberosAuth(), headers=self.Header)
                        return fileName, downloadResponse.content
                    except BaseException as e:
                        print(str(e))
        return fileName, downloadResponse

    def DownloadAttachementById(self, attachmwnrId):
        try:
            downloadUrl = '{}/binary/{}?verbose=true'.format(self.__restApiUrl, attachmwnrId)
            downloadResponse = requests.get(downloadUrl, verify=False, auth=HTTPKerberosAuth(), headers=self.Header)
            return downloadResponse.content
        except BaseException as e:
            print(str(e))
        return None

    def UpdateArticle(self, articleId, payload):
        url = '{}/article/{}?fetch=false'.format(self.__restApiUrl, str(articleId))
        response = requests.put(url, verify=False, auth=HTTPKerberosAuth(),
                                headers=self.Header, data=json.dumps(payload))
        return response


# ------- Unit test ------------------
if __name__ == '__main__':
    url = 'https://hsdes-api.intel.com/rest'
    api = HsdEsApi(url)
    val = "20191227"
    articleId = 1706857347
    payload = {
        "tenant": "server_platf_ae",
        "subject":"bug",
        "fieldValues": [
            {"tag": val}
        ]
    }
    response = api.UpdateArticle(articleId, payload)
    response = api.GetArticle(articleId)  #1306564264)


    start = 1
    delta = 1000
    max = 9900
    count = start
    while True:
        if count >= max:
            break
        api = HsdEsApi(url)
        articleId = 1306564255
        payload = {
            "tenant": "microcode_repository",
            "subject": "item",
            "fieldValues": [
                {"tag": "20191228"}
            ]
        }
        response = api.UpdateArticle(articleId, payload)
        response = api.GetArticle(articleId)  #1306564264)

        # https://hsdes.intel.com/appstore/community/#/2207766272?queryId=2207804418&articleId=1306564255
        # https://hsdes-api.intel.com/rest/doc/#!/article/getRecord
        # https: // hsdes - api.intel.com / rest / binary / 1306564264?verbose = true
        payload = HsdApiQueryPayload(2207804418)
        payload['start_at'] = str(start)  # '4351'
        payload['max_results'] = str(delta)  #'10000'
        results = api.Query(payload)
        if results is not None:
            for item in results.data:

                responsItem = ApiResponse(json.dumps(item))
                # api.DownloadAttachment(responsItem.id, 'inc', r'D:\Projects\ReleaseAutomation\ReleaseDropBox\Demo')
                filename, content = api.GetAttachment(responsItem.id, 'inc')
                # api.DownloadAttachment(responsItem.id, 'inc', r'T:\_Personal\henryli\DevUEFI\HSDMCUs')
                pass

    pass
