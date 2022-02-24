from urllib.parse import urlparse, urljoin
import requests
from flask import Flask, render_template
from flask import request
from bs4 import BeautifulSoup
import re

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def scan():
    if request.method == 'GET':
        return render_template("home/scan-empty.html")
    elif request.method == 'POST':
        combinedurls = []
        url = request.form["domain"]
        page = requests.get(url)
        combinedurls.append(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        domain_name = urlparse(url).hostname

        save = []
        secondlayer = set()


        for a_tag in soup.findAll("a"):
            href = a_tag.attrs.get("href")
            if href == "" or href is None:
                # href empty tag
                continue
            # join the URL if it's relative (not absolute link)
            href = urljoin(url, href)
            if domain_name in href:
                if 'http' in href:
                    save.append(href)
                    combinedurls.append(href)

        for intilink in save:
            if 'http' in intilink:
                page3 = requests.get(intilink)
                soup2 = BeautifulSoup(page3.text, 'html.parser')


            for a_tag2 in soup2.findAll("a"):
                href2 = a_tag2.attrs.get("href")
                if href2 == "" or href2 is None:
                    # href empty tag
                    continue
                # join the URL if it's relative (not absolute link)
                href2 = urljoin(url, href2)
                if domain_name in href2:
                    if 'http' in href2:
                        secondlayer.add(href2)
                        combinedurls.append(href2)


        counter1 = 0
        counter2 = 0


        internallink = 0
        for list in secondlayer:
            try:
                if 'http' in list:
                    scan = requests.get(list)

                    combinedurls.append(list)

                    soup = BeautifulSoup(scan.text, "html.parser")
                    # going into each internal weblinks and getting the js script links
                    src = [sc["src"] for sc in soup.select("script[src]")]

                if len(src) > 1:

                    internallink += 1

                    # constructing the paths
                    for checkdomainlist in src:

                        parsed = urlparse(checkdomainlist)
                        parsedurl = urlparse(url)
                        global resultdomain
                        resultdomain = parsedurl.hostname
                        replacedomain = parsed._replace(netloc=parsedurl)

                        # checking if the path format is bad or not
                        if '/' != str(replacedomain.path[0]):
                            counter1 += 1
                            combinedurls.append("%s/%s" % (url, replacedomain.path))
                        else:
                            counter2 += 1
                            combinedurls.append("%s%s" % (url, replacedomain.path))



            except Exception as e:
                print(e)



        goodurls = counter1
        badurls = counter2
        allurllist = len(combinedurls)
        dataformat = set(combinedurls)
        finalscrapinglinkcount = len(set(combinedurls))


        google_api = """AIza[0-9A-Za-z\\-_]{35}"""
        artifactory = """(?:\s|=|:|"|^)AKC[a-zA-Z0-9]{10,}"""
        artifactorypass = """(?:\s|=|:|"|^)AP[\dABCDEF][a-zA-Z0-9]{8,}"""
        authbasic = """basic [a-zA-Z0-9_\\-:\\.=]+"""
        awsclient = """(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}"""
        awsmwskey = """amzn\.mws\.[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"""
        base64 = """(eyJ|YTo|Tzo|PD[89]|aHR0cHM6L|aHR0cDo|rO0)[a-zA-Z0-9+/]+={0,2}"""
        basicauthcred = """(?<=:\/\/)[a-zA-Z0-9]+:[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]+"""
        cloudanarybasicauth = """cloudinary:\/\/[0-9]{15}:[0-9A-Za-z]+@[a-z]+"""
        fbaccesstoken = """EAACEdEose0cBA[0-9A-Za-z]+"""
        fboauth = """[f|F][a|A][c|C][e|E][b|B][o|O][o|O][k|K].*['|\"][0-9a-f]{32}['|\"]"""
        github = """[g|G][i|I][t|T][h|H][u|U][b|B].*['|\"][0-9a-zA-Z]{35,40}['|\"]"""
        googlecloud = """AIza[0-9A-Za-z\\-_]{35}"""
        googleoauth = """ya29\\.[0-9A-Za-z\\-_]+"""
        googleyoutubeoauth = """[0-9]+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\\.com"""
        herokuapi = """[h|H][e|E][r|R][o|O][k|K][u|U].{0,30}[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}"""
        ipv4 = """\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"""
        ipv6 = """(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))"""
        urlshttp = """https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"""
        urlwithout = """[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"""
        genericapi = """[a|A][p|P][i|I][_]?[k|K][e|E][y|Y].*['|\"][0-9a-zA-Z]{32,45}['|\"]"""
        rsaprivatekey = """-----BEGIN RSA PRIVATE KEY-----"""
        pgpprivatekey = """-----BEGIN PGP PRIVATE KEY BLOCK-----"""
        mailchampapikey = """[0-9a-f]{32}-us[0-9]{1,2}"""
        mailgunapikey = """key-[0-9a-zA-Z]{32}"""
        picaticapikey = """sk_live_[0-9a-z]{32}"""
        slacktoken = """xox[baprs]-([0-9a-zA-Z]{10,48})?"""
        slackwebhook = """https://hooks.slack.com/services/T[a-zA-Z0-9_]{10}/B[a-zA-Z0-9_]{10}/[a-zA-Z0-9_]{24}"""
        stripeapikey = """sk_live_[0-9a-zA-Z]{24}"""
        squareaccesstoken = """sqOatp-[0-9A-Za-z\\-_]{22}"""
        squareoauthsecret = """sq0csp-[ 0-9A-Za-z\\-_]{43}"""
        twilioapikey = """SK[0-9a-fA-F]{32}"""
        twitterclientid = """(?i)twitter(.{0,20})?['\"][0-9a-z]{18,25}"""
        twitteroauth = """[t|T][w|W][i|I][t|T][t|T][e|E][r|R].{0,30}['\"\\s][0-9a-zA-Z]{35,44}['\"\\s]"""
        twittersecretkey = """[t|T][w|W][i|I][t|T][t|T][e|E][r|R].*[1-9][0-9]+-[0-9a-zA-Z]{40}"""
        vaulttoken = """[sb]\.[a-zA-Z0-9]{24}"""
        firebase = """.*firebaseio\.com"""
        braintree = """access_token\\$production\\$[0-9a-z]{16}\\$[0-9a-f]{32}"""




        regex = [google_api, artifactory, artifactorypass, authbasic, awsclient, awsmwskey,
                 base64, basicauthcred, cloudanarybasicauth, fbaccesstoken, fboauth,
                 github, googlecloud, googleoauth, googleyoutubeoauth,
                 herokuapi, ipv4, ipv6, urlwithout, urlshttp,
                 genericapi, rsaprivatekey, pgpprivatekey, mailchampapikey,
                 mailgunapikey, picaticapikey, slacktoken,
                 slackwebhook, stripeapikey, squareaccesstoken, squareoauthsecret,
                 twilioapikey, twitterclientid, twitteroauth, twittersecretkey,
                 vaulttoken, firebase, braintree]

        finaldata = []

        for linkz in set(combinedurls):

            if 'http' in linkz:

                access = requests.get(linkz).text

                reg = re.findall(regex[int(request.form["regex"])], access)
                if len(reg) < 1:
                    notfound = 'Empty'
                    finaldata.append("%s,%s" % (linkz, notfound))
                else:
                    finaldata.append("%s,%s" % (linkz, reg))

        finalurls = []
        for datanow in finaldata:
            splitdata = datanow.split(',')
            finalurls.append(splitdata)


        return render_template("home/scan.html",  finalurls=finalurls, finalscrapinglinkcount=finalscrapinglinkcount, dataformat=dataformat, goodurls=goodurls, badurls=badurls, allurllist=allurllist, resultdomain=domain_name, internallink=internallink)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('home/error.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('home/error.html'), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0')