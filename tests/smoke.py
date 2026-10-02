"""Run against a local PHP server: python3 tests/smoke.py [base URL]."""
import http.cookiejar, json, re, sys, time, urllib.request, urllib.error
base=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8018/'
def game_count():
    return json.load(urllib.request.urlopen(base+'stats.php'))['gamesPlayed']
initial_count=game_count()
def client():
    opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    page=opener.open(base).read().decode()
    token=re.search(r'name="csrf-token" content="([^"]+)"',page)[1]
    def call(action='state',data=None,expected=200,csrf=token):
        req=urllib.request.Request(base+'api.php?action='+action,data=None if data is None else json.dumps(data).encode(),headers={'Content-Type':'application/json','X-CSRF-Token':csrf})
        try: response=opener.open(req)
        except urllib.error.HTTPError as error: response=error
        assert response.code==expected,(response.code,response.read().decode())
        return json.load(response)
    return call
call=client(); initial=call(); assert initial['phase']=='setup' and len(initial['catalog'])==5
other=client(); assert other()['code']!=initial['code']
settings={'teams':['Mistrzowie','Tygrysy'],'categories':['przyslowia'],'duration':15}
call('new',settings,403,csrf='bad')
call('new',{**settings,'duration':14},400)
call('new',{**settings,'teams':['A','A']},400)
ready=call('new',settings); assert ready['phase']=='ready' and 'word' not in ready
assert game_count()==initial_count
running=call('start',{}); assert running['remaining']>14 and running['word']
assert game_count()==initial_count+1
call('start',{},400)
assert game_count()==initial_count+1
first=running['revision']; scored=call('next',{'revision':first})
assert scored['phase']=='finished' and scored['outcome']=='guessed'
assert scored['roundPoints']==1 and scored['teams'][0]['score']==1 and 'word' not in scored
call('next',{'revision':first},409)
reload=call(); assert reload['teams'][0]['score']==1 and reload['phase']=='finished'
second=call('advance',{}); assert second['turn']==1 and second['phase']=='ready'
second_running=call('start',{}); assert second_running['word']!=running['word']
call('setup',{},400); call('advance',{},400)
time.sleep(15.1)
finished=call('next',{'revision':second_running['revision']},409)
finished=call(); assert finished['phase']=='finished' and finished['outcome']=='timeout'
assert finished['teams'][1]['score']==0 and 'word' not in finished
assert game_count()==initial_count+1
cycle=call('advance',{}); assert cycle['turn']==0 and cycle['round']==2 and cycle['teams'][0]['score']==1
call('setup',{}); reset=call('new',settings); assert all(t['score']==0 for t in reset['teams'])
call('start',{}); assert game_count()==initial_count+2
assert other()['phase']=='setup'
print('PASS: categories, validation, CSRF, isolated rooms, single phrase, scoring, duplicate request, reload, deadline, team rotation, reset, persistent game counter')
