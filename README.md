# kucingNFT

#Simple Web frontend & Backend with Python

Get Testnet BNB from Faucet: https://testnet.binance.org/faucet-smart/


#Simple minting the NFT to other address
https://testnet.bscscan.com/token/0x7391dd5a7a021e3bf1bf26b472d1024088f0c109


How to Test:
1. Setup your Wallet with metamask,
2. Create Network for testnet
    Network Name: Smart Chain - Testnet
    New RPC URL: https://data-seed-prebsc-1-s1.binance.org:8545
    Chain ID: 97
    Currency Symbol: BNB
    Block Explorer URL: https://testnet.bscscan.com
3. Running server :
   cd backend
   python3 app.py
   - make sure you had setup the config.json


How to access: http://68.183.190.243:8083/

```
CREATE DATABASES kucingnft;
CREATE TABLE cats (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    tokenId int,
    address VARCHAR(255) NULL,
    color VARCHAR(255) NULL,
    image VARCHAR(255) NULL,
    rarity int,
    level int,
    skills text,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);


CREATE TABLE transactions (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    address VARCHAR(255) NULL,
    block_hash text,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

Sample query:
INSERT INTO cats SET address='0xb2a18Cee119430f1a86964fbC7eEB99A4496ABB0', tokenId=15, color='brown', image='http://68.183.190.243:8083/images/type001.png', rarity=1, level=0, skills='["wisdom", "support"]', created_at=now();
INSERT INTO transactions SET address='0xb2a18Cee119430f1a86964fbC7eEB99A4496ABB0', block_hash='0x77af8473ec8f067e439a1f306324c0dc7f979ca7cdde60a0b6c80f3082eb4603', created_at=now();
```