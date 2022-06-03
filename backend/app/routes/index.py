import os
import json
from app import app
from flask import request
from app.models.trx import *
from app.models.cats import *
from web3 import Web3
import requests, json,re
import time
from app.utils.reqTrx import *

kucingNFTABI = '[{  "inputs": [{   "internalType": "string",   "name": "name",   "type": "string"  }, {   "internalType": "string",   "name": "symbol",   "type": "string"  }, {   "internalType": "string",   "name": "baseTokenURI",   "type": "string"  }],  "stateMutability": "nonpayable",  "type": "constructor" }, {  "anonymous": false,  "inputs": [{   "indexed": true,   "internalType": "address",   "name": "owner",   "type": "address"  }, {   "indexed": true,   "internalType": "address",   "name": "approved",   "type": "address"  }, {   "indexed": true,   "internalType": "uint256",   "name": "tokenId",   "type": "uint256"  }],  "name": "Approval",  "type": "event" }, {  "anonymous": false,  "inputs": [{   "indexed": true,   "internalType": "address",   "name": "owner",   "type": "address"  }, {   "indexed": true,   "internalType": "address",   "name": "operator",   "type": "address"  }, {   "indexed": false,   "internalType": "bool",   "name": "approved",   "type": "bool"  }],  "name": "ApprovalForAll",  "type": "event" }, {  "anonymous": false,  "inputs": [{   "indexed": false,   "internalType": "address",   "name": "account",   "type": "address"  }],  "name": "Paused",  "type": "event" }, {  "anonymous": false,  "inputs": [{   "indexed": true,   "internalType": "bytes32",   "name": "role",   "type": "bytes32"  }, {   "indexed": true,   "internalType": "bytes32",   "name": "previousAdminRole",   "type": "bytes32"  }, {   "indexed": true,   "internalType": "bytes32",   "name": "newAdminRole",   "type": "bytes32"  }],  "name": "RoleAdminChanged",  "type": "event" }, {  "anonymous": false,  "inputs": [{   "indexed": true,   "internalType": "bytes32",   "name": "role",   "type": "bytes32"  }, {   "indexed": true,   "internalType": "address",   "name": "account",   "type": "address"  }, {   "indexed": true,   "internalType": "address",   "name": "sender",   "type": "address"  }],  "name": "RoleGranted",  "type": "event" }, {  "anonymous": false,  "inputs": [{   "indexed": true,   "internalType": "bytes32",   "name": "role",   "type": "bytes32"  }, {   "indexed": true,   "internalType": "address",   "name": "account",   "type": "address"  }, {   "indexed": true,   "internalType": "address",   "name": "sender",   "type": "address"  }],  "name": "RoleRevoked",  "type": "event" }, {  "anonymous": false,  "inputs": [{   "indexed": true,   "internalType": "address",   "name": "from",   "type": "address"  }, {   "indexed": true,   "internalType": "address",   "name": "to",   "type": "address"  }, {   "indexed": true,   "internalType": "uint256",   "name": "tokenId",   "type": "uint256"  }],  "name": "Transfer",  "type": "event" }, {  "anonymous": false,  "inputs": [{   "indexed": false,   "internalType": "address",   "name": "account",   "type": "address"  }],  "name": "Unpaused",  "type": "event" }, {  "inputs": [],  "name": "DEFAULT_ADMIN_ROLE",  "outputs": [{   "internalType": "bytes32",   "name": "",   "type": "bytes32"  }],  "stateMutability": "view",  "type": "function" }, {  "inputs": [],  "name": "MINTER_ROLE",  "outputs": [{   "internalType": "bytes32",   "name": "",   "type": "bytes32"  }],  "stateMutability": "view",  "type": "function" }, {  "inputs": [],  "name": "PAUSER_ROLE",  "outputs": [{   "internalType": "bytes32",   "name": "",   "type": "bytes32"  }],  "stateMutability": "view",  "type": "function" }, {  "inputs": [{   "internalType": "address",   "name": "to",   "type": "address"  }, {   "internalType": "uint256",   "name": "tokenId",   "type": "uint256"  }],  "name": "approve",  "outputs": [],  "stateMutability": "nonpayable",  "type": "function" }, {  "inputs": [{   "internalType": "address",   "name": "owner",   "type": "address"  }],  "name": "balanceOf",  "outputs": [{   "internalType": "uint256",   "name": "",   "type": "uint256"  }],  "stateMutability": "view",  "type": "function" }, {  "inputs": [{   "internalType": "uint256",   "name": "tokenId",   "type": "uint256"  }],  "name": "burn",  "outputs": [],  "stateMutability": "nonpayable",  "type": "function" }, {  "inputs": [{   "internalType": "uint256",   "name": "tokenId",   "type": "uint256"  }],  "name": "getApproved",  "outputs": [{   "internalType": "address",   "name": "",   "type": "address"  }],  "stateMutability": "view",  "type": "function" }, {  "inputs": [{   "internalType": "bytes32",   "name": "role",   "type": "bytes32"  }],  "name": "getRoleAdmin",  "outputs": [{   "internalType": "bytes32",   "name": "",   "type": "bytes32"  }],  "stateMutability": "view",  "type": "function" }, {  "inputs": [{   "internalType": "bytes32",   "name": "role",   "type": "bytes32"  }, {   "internalType": "uint256",   "name": "index",   "type": "uint256"  }],  "name": "getRoleMember",  "outputs": [{   "internalType": "address",   "name": "",   "type": "address"  }],  "stateMutability": "view",  "type": "function" }, {  "inputs": [{   "internalType": "bytes32",   "name": "role",   "type": "bytes32"  }],  "name": "getRoleMemberCount",  "outputs": [{   "internalType": "uint256",   "name": "",   "type": "uint256"  }],  "stateMutability": "view",  "type": "function" }, {  "inputs": [{   "internalType": "bytes32",   "name": "role",   "type": "bytes32"  }, {   "internalType": "address",   "name": "account",   "type": "address"  }],  "name": "grantRole",  "outputs": [],  "stateMutability": "nonpayable",  "type": "function" }, {  "inputs": [{   "internalType": "bytes32",   "name": "role",   "type": "bytes32"  }, {   "internalType": "address",   "name": "account",   "type": "address"  }],  "name": "hasRole",  "outputs": [{   "internalType": "bool",   "name": "",   "type": "bool"  }],  "stateMutability": "view",  "type": "function" }, {  "inputs": [{   "internalType": "address",   "name": "owner",   "type": "address"  }, {   "internalType": "address",   "name": "operator",   "type": "address"  }],  "name": "isApprovedForAll",  "outputs": [{   "internalType": "bool",   "name": "",   "type": "bool"  }],  "stateMutability": "view",  "type": "function" }, {  "inputs": [{   "internalType": "address",   "name": "to",   "type": "address"  }],  "name": "mint",  "outputs": [],  "stateMutability": "nonpayable",  "type": "function" }, {  "inputs": [],  "name": "name",  "outputs": [{   "internalType": "string",   "name": "",   "type": "string"  }],  "stateMutability": "view",  "type": "function" }, {  "inputs": [{   "internalType": "uint256",   "name": "tokenId",   "type": "uint256"  }],  "name": "ownerOf",  "outputs": [{   "internalType": "address",   "name": "",   "type": "address"  }],  "stateMutability": "view",  "type": "function" }, {  "inputs": [],  "name": "pause",  "outputs": [],  "stateMutability": "nonpayable",  "type": "function" }, {  "inputs": [],  "name": "paused",  "outputs": [{   "internalType": "bool",   "name": "",   "type": "bool"  }],  "stateMutability": "view",  "type": "function" }, {  "inputs": [{   "internalType": "bytes32",   "name": "role",   "type": "bytes32"  }, {   "internalType": "address",   "name": "account",   "type": "address"  }],  "name": "renounceRole",  "outputs": [],  "stateMutability": "nonpayable",  "type": "function" }, {  "inputs": [{   "internalType": "bytes32",   "name": "role",   "type": "bytes32"  }, {   "internalType": "address",   "name": "account",   "type": "address"  }],  "name": "revokeRole",  "outputs": [],  "stateMutability": "nonpayable",  "type": "function" }, {  "inputs": [{   "internalType": "address",   "name": "from",   "type": "address"  }, {   "internalType": "address",   "name": "to",   "type": "address"  }, {   "internalType": "uint256",   "name": "tokenId",   "type": "uint256"  }],  "name": "safeTransferFrom",  "outputs": [],  "stateMutability": "nonpayable",  "type": "function" }, {  "inputs": [{   "internalType": "address",   "name": "from",   "type": "address"  }, {   "internalType": "address",   "name": "to",   "type": "address"  }, {   "internalType": "uint256",   "name": "tokenId",   "type": "uint256"  }, {   "internalType": "bytes",   "name": "_data",   "type": "bytes"  }],  "name": "safeTransferFrom",  "outputs": [],  "stateMutability": "nonpayable",  "type": "function" }, {  "inputs": [{   "internalType": "address",   "name": "operator",   "type": "address"  }, {   "internalType": "bool",   "name": "approved",   "type": "bool"  }],  "name": "setApprovalForAll",  "outputs": [],  "stateMutability": "nonpayable",  "type": "function" }, {  "inputs": [{   "internalType": "bytes4",   "name": "interfaceId",   "type": "bytes4"  }],  "name": "supportsInterface",  "outputs": [{   "internalType": "bool",   "name": "",   "type": "bool"  }],  "stateMutability": "view",  "type": "function" }, {  "inputs": [],  "name": "symbol",  "outputs": [{   "internalType": "string",   "name": "",   "type": "string"  }],  "stateMutability": "view",  "type": "function" }, {  "inputs": [{   "internalType": "uint256",   "name": "index",   "type": "uint256"  }],  "name": "tokenByIndex",  "outputs": [{   "internalType": "uint256",   "name": "",   "type": "uint256"  }],  "stateMutability": "view",  "type": "function" }, {  "inputs": [{   "internalType": "address",   "name": "owner",   "type": "address"  }, {   "internalType": "uint256",   "name": "index",   "type": "uint256"  }],  "name": "tokenOfOwnerByIndex",  "outputs": [{   "internalType": "uint256",   "name": "",   "type": "uint256"  }],  "stateMutability": "view",  "type": "function" }, {  "inputs": [{   "internalType": "uint256",   "name": "tokenId",   "type": "uint256"  }],  "name": "tokenURI",  "outputs": [{   "internalType": "string",   "name": "",   "type": "string"  }],  "stateMutability": "view",  "type": "function" }, {  "inputs": [],  "name": "totalSupply",  "outputs": [{   "internalType": "uint256",   "name": "",   "type": "uint256"  }],  "stateMutability": "view",  "type": "function" }, {  "inputs": [{   "internalType": "address",   "name": "from",   "type": "address"  }, {   "internalType": "address",   "name": "to",   "type": "address"  }, {   "internalType": "uint256",   "name": "tokenId",   "type": "uint256"  }],  "name": "transferFrom",  "outputs": [],  "stateMutability": "nonpayable",  "type": "function" }, {  "inputs": [],  "name": "unpause",  "outputs": [],  "stateMutability": "nonpayable",  "type": "function" }] '
headerConfig = {
    "Server" : "kucing Liar v1.0",
    "Access-Control-Allow-Origin": "*"
}

@app.route('/', methods=['GET', 'POST'])
def index():
	response = { 'code' : 200, 
				 'name' : 'API Kucing NFT', 
				 'version' : '1.0.0' }
	return json.dumps(response), 200, headerConfig
	

@app.route('/api/cats/<string:tokenID>', methods=['GET'])
def catDetails(tokenID):
	data = getCats(tokenID)
	response = { 'code' : 200, 'message' : 'success'}
	if data != None:
		response['data'] = {
					 	'tokenId' : data[1],
					 	'color' : data[3],
					 	'image' : data[4],
					 	'rarity' : data[5],
					 	'level' : data[6],
					 	'skills' : data[7]
					 }
	return json.dumps(response), response['code'], headerConfig
	
@app.route('/api/claim', methods=['POST'])
def claim():
	req_data = request.get_json()
	address, transaction = req_data['address'], req_data['transaction']
	response = { 'code' : 200, 'message' : 'success' }

	err = getTrx(req_data)
	# err = ""
	if len(err) != 0:
		response['code'] = 400
		response['message'] = err
		return json.dumps(response), response['code'], headerConfig
	else:
		#Minting
		chainID = app.config['config']["chain"]["chainID"]
		tokenURI = app.config['config']["chain"]["tokenURI"]
		walletAddress = app.config['config']["chain"]["walletAddress"]
		walletPrivateKey = app.config['config']["chain"]["walletPrivateKey"]
		web3 = Web3(Web3.HTTPProvider(app.config['config']["chain"]["rpcURL"]))
		
		contract = web3.eth.contract(address=web3.toChecksumAddress(tokenURI) , abi=kucingNFTABI)
		nonce = web3.eth.get_transaction_count(walletAddress)
		mint_txn = contract.functions.mint(address).buildTransaction({
            "chainId": chainID,
            "gas": 10000000,
            "gasPrice": web3.toWei("10",'gwei'),
            "nonce": nonce,
        })
		signed_txn = web3.eth.account.sign_transaction(mint_txn, private_key=walletPrivateKey)
		tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
		txHash = str(web3.toHex(tx_token))

		if len(getTrx({'address' : address,'transaction' : txHash})) != 0:
			response['message'] = "Transaction Failed"
			response['code'] = 400
			return json.dumps(response), response['response_code'], headerConfig
		print("minting", txHash)
		print("nonce:", nonce)

		# txHash = "0x0947b117cad106dd273767f41b356418809d388998795713a837645d70fc0cc0"
		while(1):
			time.sleep(1.5)
			tokenID = getLastTrx(txHash)
			print(tokenID)
			if len(tokenID) != 0: break
		
		cat = generateCat()
		minting({
			"address" : address,
			"tokenId" : tokenID,
			"color" : cat['color'],
			"image" : cat['image'],
			"rarity" : cat['rarity'],
			"level" : cat['level'],
			"skills" : cat['skills']
		})
		response['data'] = {
			"tokenId" : tokenID,
			"color" : cat['color'],
			"image" : cat['image'],
			"rarity" : cat['rarity'],
			"level" : cat['level'],
			"skills" : cat['skills']
		}
	
	return json.dumps(response), response['code'], headerConfig