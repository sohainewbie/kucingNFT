/*
author: kucingliar aka sohay
all env with testnet
*/

$(document).ready(function(){
	let envChain = "Testnet";
	let tokenAddress = "0x7391dd5a7a021e3bf1bf26b472d1024088f0c109"; // Address Kucing NFT
	let tokenWBNB = "0xae13d989dac2f0debff460ac112a837c89baa7cd"; // address wbnb
	let ownerAddress = "0x4520264a1ea327be31a22606ceb1b23c74470fe4";
    let account = localStorage.getItem("account") || "";
	let chainId = localStorage.getItem("chainId") || null;
	const web3 = new window.Web3(window.ethereum);
	$("#env").text(envChain);
	if(envChain === "Testnet") {
		$("#setup-balance").show();
	}
	
	let chainCongfig = {
							chainId: "97",
							chainName: 'Binance Smart Chain - Testnet',
							nativeCurrency: {
								name: 'BNB',
								symbol: 'BNB',
								decimals: 18
							},
							rpcUrls: ['https://data-seed-prebsc-1-s1.binance.org:8545'],
							blockExplorerUrls: ['https://testnet.bscscan.com']
						};
	const canConnect = typeof window.ethereum !== "undefined";
	
 	const checkConnection = async () => {

		window.ethereum.on('chainChanged', (_chainId) => window.location.reload());
		if (account && chainId !== null) {
            $("#connectBtn").val("Disconnect");
		} else {
			$("#connectBtn").val("Connect");
		}

		window.ethereum.on('accountsChanged', function (accounts) {
			console.log("account changed");
			disconnectAccount();
		});

// 		loadBlocks();
	};
	checkConnection(); 
	$("#connectBtn").click(connectAccount);
    
    async function connectAccount() {
    	var statusConnection = $("#connectBtn").val();
    	if(statusConnection == "Disconnect"){
    		return disconnectAccount();
    	}
    	
		if (canConnect) {
			console.log("Connecting via web3");
			try {
				web3.currentProvider.on("disconnect", function () {
					disconnectAccount();
				});
				chainId = await web3.eth.getChainId();
				if(chainId === chainCongfig.chainId){
    				window.ethereum.request({
    						method: 'wallet_addEthereumChain',
    						params: [chainCongfig]
    					});	
    					
				}

				const accounts = await web3.eth.requestAccounts();
				console.log(accounts)
				account = accounts[0];
				localStorage.setItem("account", account);
				localStorage.setItem("chainId", chainId);
				console.log(account + " connected.");
				getBalanceAccount(account)

				$("#address").text(account);
                $("#connectBtn").val("Disconnect");
                $("#wallet-info").show();
                $("#claim").show();
			} catch (err) {
			    console.log(err)
				console.log("Failed to connect via web3");
				disconnectAccount();
			}
		}
	}
	
	function disconnectAccount() {
		console.log("disconnected");
		localStorage.removeItem("account");
		localStorage.removeItem("chainId");
		$("#connectBtn").val("Connect");
		$("#wallet-info").hide();
		$("#claim").hide();
		$("#address").text("");
	}
	
	
	async function getBalanceAccount(account) {
		const contract = new web3.eth.Contract(kucingNFTAbiJson, tokenAddress);
		const tokenBalance = await contract.methods.balanceOf(account).call();
		const tokenName = await contract.methods.name().call();

		const wbnbContract = new web3.eth.Contract(wbnbabiJson, tokenWBNB);
		const balanceWBNB = await wbnbContract.methods.balanceOf(account).call();

		// note that this number includes the decimal places (in case of BUSD, that's 18 decimal places)
		const getBusd = Number(web3.utils.fromWei(balanceWBNB)).toFixed(4)

		$("#nftTotal").text(tokenBalance);
		$("#nftName").text(tokenName);
		$("#address").text(`${account} / ${getBusd} WBNB`);
		$("#claim").show();
	}

	if(account.length !== 0){
		$("#wallet-info").show();
		getBalanceAccount(account);
	}
  
  async function payment(account) {
  		$('#claim').attr('disabled','disabled');
  		$('#loading').show()
  		let amount = 0.0035;
		const wbnbContract = new web3.eth.Contract(wbnbabiJson, tokenWBNB);
        let transaction = await wbnbContract.methods.transfer(ownerAddress, '0x' + ((amount * 1000000000000000000).toString(16)));
        console.log(`transaction:`, transaction)
        try{
			let receipt = await transaction.send({
                        from: account
            })

            $.ajax( {
            		  url :"http://68.183.190.243:8083/api/claim", 
					  type:"POST",
            		  data : JSON.stringify({ "address": account, "transaction": receipt.blockHash }),
    				  dataType:"json",
    				  contentType : 'application/json'
            }).done(function( data ) {
            	let image = data['data']['image'];
            	let tokenId = data['data']['tokenId']
            	let color = data['data']['color'];
            	let rarity = data['data']['rarity'];
            	let level = data['data']['level'];
            	let skills = data['data']['skills'];
			    console.log( image );
			    $("#resultClaim").show()
			    $("#nftImage").attr("src",image);
			    $("#tokenId").text(`tokenId: ${tokenId}`);
			    $("#color").text(`color: ${color}`);
			    $("#rarity").text(`rarity: ${rarity}`);
			    $("#level").text(`level: ${level}`);
			    $("#skills").text(`skills: ${skills}`);
			    $('#claim').removeAttr('disabled');
			    getBalanceAccount(account);
			    $('#loading').hide();
			 }, "json");			 
			 
        } catch (err) {
        	alert(err.message)
        	$('#claim').removeAttr('disabled');
        	$('#loading').hide()
        }
  }
  $("#claim").click(function(){
		checkConnection();
		var statusConnection = $("#connectBtn").val();
		if(!canConnect || statusConnection == "Connect"){
			return alert("Please connect the wallet first !!!")
		}
		console.log(account)
		payment(account)
		
		
		var debug = 2;
		if(debug === 1){
            $.ajax( {
            		  url :"http://68.183.190.243:8083/api/claim", 
					  type:"POST",
            		  data : JSON.stringify({ "address": account, "transaction": "0xf5a639d18bccd48aab983fe9b113c38b5890ded75bf9dd5eefae804883305545" }),
    				  dataType:"json",
    				  contentType : 'application/json'
            }).done(function( data ) {
            	let image = data['data']['image'];
            	let tokenId = data['data']['tokenId']
            	let color = data['data']['color'];
            	let rarity = data['data']['rarity'];
            	let level = data['data']['level'];
            	let skills = data['data']['skills'];
			    console.log( image );
			    $("#resultClaim").show()
			    $("#nftImage").attr("src",image);
			    $("#tokenId").text(`TokenId: ${tokenId}`);
			    $("#color").text(`Color: ${color}`);
			    $("#rarity").text(`Rarity: ${rarity}`);
			    $("#level").text(`Level: ${level}`);
			    $("#skills").text(`Skills: ${skills}`);
			 }, "json");			
		}
	
	})
});          

