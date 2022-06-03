import re, requests

def getLastTrx(txHash):
    tokenURI = "0x7391dd5a7a021e3bf1bf26b472d1024088f0c109"
    trxUrl = 'https://testnet.bscscan.com/tx/{}'.format(txHash)
    responseBSC = requests.get(trxUrl, headers={
    	        'authority': 'bscscan.com',
    	        'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
    	    }).text
    try:
        tokenID = re.findall(r"href='/token/{}\?a\=(.*?)'".format(tokenURI), responseBSC, re.I|re.M)[2]
    except:
        tokenID = ""
    return tokenID
