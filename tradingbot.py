from datetime import datetime
import signal

import string
import sys
import uuid
import time

import requests
from decimal import *

#class GDAXClient(object):
#https://api.pro.coinbase.com/products/ETH-BTC/book

#://www.coingecko.com/en/coins/ethereum/trading_exchanges= 0

#track book spread in different sheet
#log  qty each
#add the whole bid ask
#add btc/usd and eth/usd
#the movement of underlying
class YoBitClient(object):
    def __init__(self, url, public_key, secret):
        self.url = url + "/api/3"
        self.session = requests.session()
        self.session.auth = (public_key, secret)

    def get_orderbook(self, symbol_code):
        """Get orderbook. """
        return self.session.get("%s/depth/%s" % (self.url, symbol_code)).json()

class HitBTCClient(object):
    def __init__(self, url, public_key, secret):
        self.url = url + "/api/2"
        self.session = requests.session()
        self.session.auth = (public_key, secret)

    def get_symbol(self, symbol_code):
        """Get symbol."""
        return self.session.get("%s/public/symbol/%s" % (self.url, symbol_code)).json()

    def get_all(self):
	return self.session.get("%s/public/symbol" % self.url).json()

    def get_orderbook(self, symbol_code):
        """Get orderbook. """
        return self.session.get("%s/public/orderbook/%s" % (self.url, symbol_code)).json()

    def get_address(self, currency_code):
        """Get address for deposit."""
        return self.session.get("%s/account/crypto/address/%s" % (self.url, currency_code)).json()

    def get_account_balance(self):
        """Get main balance."""
        return self.session.get("%s/account/balance" % self.url).json()

    def get_trading_balance(self):
        """Get trading balance."""
        return self.session.get("%s/trading/balance" % self.url).json()

    def transfer(self, currency_code, amount, to_exchange):
        return self.session.post("%s/account/transfer" % self.url, data={
                'currency': currency_code, 'amount': amount,
                'type': 'bankToExchange' if to_exchange else 'exchangeToBank'
            }).json()

    def new_order(self, client_order_id, symbol_code, side, quantity, price=None):
        """Place an order."""
        data = {'symbol': symbol_code, 'side': side, 'quantity': quantity}

        if price is not None:
            data['price'] = price

        return self.session.put("%s/order/%s" % (self.url, client_order_id), data=data).json()

    def get_order(self, client_order_id, wait=None):
        """Get order info."""
        data = {'wait': wait} if wait is not None else {}

        return self.session.get("%s/order/%s" % (self.url, client_order_id), params=data).json()

    def cancel_order(self, client_order_id):
        """Cancel order."""
        return self.session.delete("%s/order/%s" % (self.url, client_order_id)).json()

    def withdraw(self, currency_code, amount, address, network_fee=None):
        """Withdraw."""
        data = {'currency': currency_code, 'amount': amount, 'address': address}

        if network_fee is not None:
            data['networkfee'] = network_fee

        return self.session.post("%s/account/crypto/withdraw" % self.url, data=data).json()

    def get_transaction(self, transaction_id):
        """Get transaction info."""
        return self.session.get("%s/account/transactions/%s" % (self.url, transaction_id)).json()


if __name__ == "__main__":
    public_key = ""
    secret = ""

    c1 ="eth"
    c2 ="btc"
    try:
       c1 =sys.argv[1]
    except:
	pass
    c2 ="btc"
    try:
       c2 =sys.argv[2]
    except:
	pass

    d =  0
    try:
       d = int(sys.argv[3])
    except:
	pass
    print d
    btc_address = ""
    yoclient = YoBitClient("https://yobit.net/", public_key, secret)
    client = HitBTCClient("https://api.hitbtc.com", public_key, secret)
    all_items = client.get_all()


    sys.stdout.flush()
    h = "pair,date, ex(buy), ask(buy),size, bid, size, ask,size,bid(sell), size, spread, size, total, fee,total-fee,inc"
    fn=open("trades_%s.csv"%d,"wr")
    fn.write("%s\n" % h)
    while True:
    	try:
    	  for i in all_items:
           c1 = 	i['baseCurrency'].lower()
           c2 = 	i['quoteCurrency'].lower()
	   v ="%s_%s" % (c1,c2)
	   if v not in ['1st_btc','1st_eth','adx_eth','aeon_btc','amb_btc','amb_eth','amb_usd','amp_btc','ardr_btc','arn_btc','arn_eth','art_btc','ats_btc','ats_eth','avt_eth','bas_eth','bch_btc','bch_eth','bch_usd','bcn_btc','bcn_eth','bcn_usd','bet_eth','bkb_btc','bmc_btc','bmc_eth','bmc_usd','bos_btc','bqx_eth','btx_btc','bus_btc','cdt_btc','cdt_eth','cdt_usd','cdx_eth','cfi_btc','cfi_eth','cld_btc','cld_eth','cld_usd','cnd_btc','cnd_eth','cnd_usd','coss_btc','coss_eth','csno_btc','ctx_btc','ctx_eth','cvc_usd','dcn_btc','dcn_eth','dcn_usd','ddf_eth','dent_eth','dice_btc','dice_eth','dnt_btc','drpu_btc','dsh_btc','ebet_eth','ebtc_btc','ebtc_eth','ebtc_usd','ebtcold_btc','ebtcold_eth','ebtcold_usd','edg_btc','edo_btc','edo_eth','edo_usd','emgo_btc','emgo_usd','eng_eth','enj_btc','enj_eth','enj_usd','etbs_btc','etp_btc','etp_eth','etp_usd','evx_btc','evx_eth','evx_usd','exn_btc','fcn_btc','fuel_btc','fuel_eth','fuel_usd','fun_btc','fun_eth','fun_usd','fyn_eth','fyp_btc','gvt_eth','hgt_eth','hvn_btc','hvn_eth','ico_btc','icos_btc','icos_eth','icos_usd','icx_btc','icx_eth','icx_usd','ignis_eth','indi_btc','la_eth','life_btc','maid_btc','maid_eth','maid_usd','mana_usd','mcap_btc','mips_btc','mne_btc','msp_eth','myb_eth','ndc_eth','nebl_btc','nebl_eth','neo_btc','neo_eth','neo_usd','nto_btc','nxc_btc','nxt_btc','nxt_eth','nxt_usd','oax_btc','oax_eth','oax_usd','odn_btc','opt_btc','orme_btc','otx_btc','pix_btc','pix_eth','plr_eth','poe_btc','poe_eth','prg_btc','prg_usd','ptoy_btc','ptoy_eth','qau_btc','qau_eth','qtum_eth','qvt_eth','rlc_btc','rvt_btc','sbd_btc','sc_btc','skin_btc','sngls_btc','steem_btc','strat_btc','strat_eth','strat_usd','stx_btc','stx_eth','stx_usd','sur_eth','taas_btc','taas_eth','tgt_btc','tix_eth','tkr_eth','trst_btc','uet_eth','veri_btc','veri_eth','veri_usd','vib_btc','vib_eth','vib_usd','vibe_btc','voise_btc','wings_btc','wmgo_btc','wmgo_usd','xaur_btc','xaur_eth','xdn_btc','xdn_eth','xdn_usd','xmr_btc','xmr_eth','xmr_usd','xrp_btc','xtz_btc','xtz_eth','xtz_usd','xuc_btc','xuc_eth','xuc_usd','yoyow_btc','zsc_btc','zsc_eth','zsc_usd']:
		#time.sleep(1)
                c1 = 	i['baseCurrency'].lower()
                c2 = 	i['quoteCurrency'].lower()
		o1 = client.get_orderbook("%s%s" % (string.upper(c1),string.upper(c2)))
		o2 = yoclient.get_orderbook("%s_%s" % (c1,c2))
		o2 = o2["%s_%s" % (c1,c2)]
		#o1 = client.get_orderbook('ETHBTC')
		#o2 = yoclient.get_orderbook('eth_btc')
		#o1 = client.get_orderbook('LTCBTC')
		#o2 = yoclient.get_orderbook('ltc_btc')
		#o2 = o2['eth_btc']
		#o2 = o2['ltc_btc']
                ex1_ask = float(o2['asks'][d][0])
                ex2_ask = float(o1['ask'][d]['price'])
                ex1_bid = float(o2['bids'][d][0])
                ex2_bid = float(o1['bid'][d]['price'])
                ex1_a_s = float(o2['asks'][d][1])
                ex2_a_s = float(o1['ask'][d]['size'])
                ex1_b_s = float(o2['bids'][d][1])
                ex2_b_s = float(o1['bid'][d]['size'])
		trade = ""
		spread = 0
		qty = 0
		vig = 0
		amt =0
  		if ex1_ask < ex2_bid:
  		        n  = str(datetime.now())[:19]
			qty = ex2_b_s
			if ex1_a_s < ex2_b_s:
				qty = ex1_a_s
			spread = ex2_bid-ex1_ask
			amt = qty*spread
			vig = (qty*ex2_bid*.002)+(qty*ex1_ask*.002)
			trade= "%s,%s,yo,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (i["id"],str(n),ex1_ask,ex1_a_s,ex1_bid,ex1_b_s,ex2_ask,ex2_a_s,ex2_bid,ex2_b_s,spread,qty,qty*spread,vig,amt-vig,i["quantityIncrement"])
  		elif ex2_ask < ex1_bid:
  		        n  = str(datetime.now())[:19]
			qty = ex1_b_s
			if ex2_a_s < ex1_b_s:
				qty = ex2_a_s
			spread = ex1_bid-ex2_ask
			amt = qty*spread
			vig = (qty*ex1_bid*.002)+(qty*ex2_ask*.002)
			trade =  "%s,%s,hit,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (i["id"],str(n),ex2_ask,ex2_a_s,ex2_bid,ex2_b_s,ex1_ask,ex1_a_s,ex1_bid,ex1_b_s,spread,qty,qty*spread,vig,amt-vig,i["quantityIncrement"])
		x = 0
		if vig < (amt+x):
    			fn.write("%s\n" % trade)
    	except KeyboardInterrupt,e2:
		print e2
		fn.close()
    		sys.exit(1)
    	except Exception, ex:
		print ex
		time.sleep(5)

