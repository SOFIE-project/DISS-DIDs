from indy import anoncreds, crypto, did, ledger, pool, wallet
from indy.error import ErrorCode, IndyError
import json
import sys
import asyncio

pool_name             = 'SOFIE'
pool_genesis_txn_path = "/home/sofie/Indy_Testbed_Setup/config/SOFIE/pool_transactions_genesis"
as_id                 = "auth-server"
as_wallet_pass        = ""
cred_def_id = "KecCwQfSjPPYWhpZprpxqK:3:CL:KecCwQfSjPPYWhpZprpxqK:2:AUEB-job-certificate:1.2:AUEBCERT1"
cred_def_json = '{"ver":"1.0","id":"KecCwQfSjPPYWhpZprpxqK:3:CL:KecCwQfSjPPYWhpZprpxqK:2:AUEB-job-certificate:1.2:AUEBCERT1","schemaId":"KecCwQfSjPPYWhpZprpxqK:2:AUEB-job-certificate:1.2","type":"CL","tag":"AUEBCERT1","value":{"primary":{"n":"108966698464648955369904211456205961379230207915900874157408586410679744402660895775703011854611805154260148344616983809174220222243002731998952936070390429313402044311805025338814221784359133318415432944437773525713538856264813364539967344359687253014395154545723953621469282069246727057718223963597133730664015099863036577563474268525743060816924404618840171414595393888614299539064938799498678950699481243080129316456889586727661584274104424982227033121907866736261227763641124664057795224232784889312331078105761830771799938487743859770529288614239313022233748152926049408933741826123979218508758472643936103673773","s":"10629230947319756631354864316828132085516779690425108342976660578952616178961848727346021761298768905305083165684614226824453627945314726722368855718444616679189460525509326534917163584243045777612735063565891414946748698095078810219926913749889558872001830421641891196027307557163491570537487490958014841387328343160391621200562211935368354230563932219469117693023312587124786633772154558206611352803737519458272374723078793166085485004195408865131335463901914186715170815433814507434825686869307249636683581690264627034167594012653762045502664605774040157633749840616967506100129764222373319416225691643571148665740","r":{"position":"100728234777654801540988701277386836868615460806593895817856703275479072020982835993317603556553235521677993750049638518486451089513040601952723866702459237729790469652338115666803216378248462270806051594635667158792184030798078505365519485291074633040592357084705207537495704255724921498648557474739462839897212344748581578244997879278248383993298928214111321267590793093851122848194198837240291555293916331447018125554873194243155297862465503773851050395370480848826551781089916361454936128444062058196849580034790958257155527392195292163296844224985973644007727656646434438832009689067505844672671818021606839303884","master_secret":"79279000746969503722314266196487144681130602337969492459458670768775330387885040524816384048096881727378539146381906226292140341551604569210619203791285063495760623907463256930360393923970770298136520548190209855926063698464216493361978554298012923855634605404217151994144009147411060131322524409011265192399255288327450582255730800822625210495464758689629793503593003048569424634228162608134062809939167074345158462894827430471309919633379712317826640471631513295611303275983327698584366041371127117402160506561792638738682865377617245754032117417264292288824796657408759237072524185996375441659700702702029090954291","full_name":"68919341701920655111399935834794892427491078355277520762194372325044505122671775192905591585788812699720472872045474609802541918595871554534920681045054007974343045594472193214506507955835524010154444379502612394576380640329390912649382162466565651312255445058909154989148984082451978748962540302348034744784524448658764521352132649507401616145251763285390642088262487690301944720468642873929141977840186011191255746268748663778694044052214836592951999504096945165214283813019510023211866244288306964406714733859470739582943852654815663609489615123434801915412545801636031655091460790963966806220564230400649148821914"},"rctxt":"55939536935152480324665255661544353183481045398252673766171831794588320873721134984508377210574665908252037579875889540741378035860501409851207893764388825038426950965828301269696736221662976594207734946849157160934033097943400996038253558221058750251973898705187608375579276493355687961749696432447612246074117582993540938234667509640607251842926779219713662391656989919866503969657766229482623567100897055816823001635953585363592199069282248340212485086755494635866235480238809758260774723480842282515408802775364578523688431117310015253024702563332911998962191719397491757424081098716601176060243278871977369071804","z":"10014386179494452748535586318967531756133881139159988517588252471271078399411905933311420533916443758389351414253734222146244839319708243014641279142663645267240838388176647236781700354881250634308404002536822811020395622559141297350931142043552208162855840270564572568690003784700631515171208027153048925285397299088814148110409936427512572244053817518966549587533466532953939731407564548403876184201986646457856833081052796313879602908128286349035395938105302700859026924065556892543784075623194764833212080517898808478704837739524978432676438288419955825190368731135788150437352798295610904382129801742102130604962"}}}'
schema_id = "KecCwQfSjPPYWhpZprpxqK:2:AUEB-job-certificate:1.2"

async def run(action,nonce, proof):
    try:
        pool_config = json.dumps({"genesis_txn": str(pool_genesis_txn_path)})
        await pool.set_protocol_version(2)
        pool_handle = await pool.open_pool_ledger(pool_name, pool_config)
        

        proof_request = {
            'nonce': nonce,
            'name': 'professors',
            'version': '0.1',
            'requested_attributes': {
                'attr1_referent': {
                    'name': 'position',
                    'restrictions': [{'cred_def_id': cred_def_id}]
                }
            },
            "requested_predicates": {}
        }
        if action == "generate":
            print(json.dumps(proof_request))
            sys.exit()

        as_wallet_config = json.dumps({"id": as_id})
        as_wallet_credentials = json.dumps({"key": as_wallet_pass})
        as_wallet = await wallet.open_wallet(as_wallet_config, as_wallet_credentials)
        as_dids = json.loads(await did.list_my_dids_with_meta(as_wallet))
        as_did =  as_dids[0]['did']
        
        proof_req_json = json.dumps(proof_request)
        schemas_json = {}
        get_schema_request = await ledger.build_get_schema_request(as_did, schema_id)
        get_schema_response = await ledger.submit_request(pool_handle, get_schema_request)
        (received_schema_id, received_schema) = await ledger.parse_get_schema_response(get_schema_response)
        schemas_json[received_schema_id] = json.loads(received_schema)
        cred_defs_json = {}
        cred_defs_json[cred_def_id] = json.loads(cred_def_json)
        revoc_regs_json = json.dumps({})
        assert await anoncreds.verifier_verify_proof(proof_req_json, proof, json.dumps(schemas_json), json.dumps(cred_defs_json), revoc_regs_json, "{}")
        print(json.loads(proof)['requested_proof']['revealed_attrs']['attr1_referent']['raw'])
        await pool.close_pool_ledger(pool_handle)
        sys.exit()

    except IndyError as e:
        print('Error occurred: %s' % e)



def main():
    if len(sys.argv) < 3:
        print ("Usage server.py generate <nonce> or \n server.py verify <nonce> <proof>")
        sys.exit()
    action = sys.argv[1]
    nonce = sys.argv[2]
    proof = ""
    if len(sys.argv) == 4:
        proof = sys.argv[3]

    if action != "generate" and action != "verify":
        print ("Usage server.py <action> <nonce> where action can be either 'generate' or 'verify'")
        sys.exit()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(action, nonce, proof))
    loop.close()


if __name__ == '__main__':
    main()
