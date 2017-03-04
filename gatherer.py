import sys, os, time
import spotipy
import spotipy.util as util
import urllib2

# export SPOTIPY_CLIENT_ID='4703020e6c6643448a29e593df0ad64c'
# export SPOTIPY_CLIENT_SECRET='74e38f246ccf4ab2b384f4377bd0ef28'
# export SPOTIPY_REDIRECT_URI=''

class Data: pass

def retrieve_song(genre,n=50):
    retrieved_songs=[]
    uniq=[]
    c=0
    T=time.time()
    while len(retrieved_songs)<n:
        c+=1
        if c%10 == 0:
            print 'iteration#', c, len(retrieved_songs)
        results = sp.recommendations(seed_artists=None, seed_genres=[genre], seed_tracks=None, limit=100, country=None)#, **kwargs)
        for r in results['tracks']:
            data = Data()
            data.album = r['album']['name']
            if r['album']['images']:
                data.image = r['album']['images'][0]
            else:
                data.image = 'Not Found'
            data.id = r['id']
            data.track_name = r['name']
            data.mp3 = r['preview_url']
            arr=[]
            for arti in r['artists']:
                arr+=[arti['name']]
            data.artist_name = arr

            if data.mp3==None or data.mp3==[]:
                # print 'No mp3'
                pass
            else:
                if data.id in uniq:
                    # print 'duplicated'
                    pass
                else:
                    uniq+=[data.id]
                    retrieved_songs.append(data)
    print 'Retrieved %d in %.2f seconds'  %(len(retrieved_songs), time.time()-T)
    return retrieved_songs[:n]

def downloadMP3(songs, genre):
    T2 = time.time()
    filepath = 'mp3/'+genre+'/'
    print 'Downloading mp3'
    for d in songs:
        try:
            dlmp3 = urllib2.urlopen(d.mp3)
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            with open(filepath+d.id+'.mp3', 'wb') as dl: #track[0].strip().split()[0]
                dl.write(dlmp3.read())
        except:
            print 'Timed out:',d.id ,'url', d.mp3

    T3 = time.time()
    print 'Downloaded in %.2f' %T3-T2

def writeCSV(songs, genre):
    filepath = 'metadata/'
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    with open(filepath+genre +'.csv', 'w') as f:
        f.write("FileIndex,id,trackName,album,artistName,image,link\n")
        for i,d in enumerate(songs):
            f.write(str(i+1)+',')
            f.write(d.id+',')
            f.write(d.track_name.replace(',', '->').encode('utf8')+',')
            f.write(d.album.replace(',', '->').encode('utf8')+',')
            f.write('{'+'-'.join(d.artist_name).encode('utf8')+'},')
            f.write(d.image['url']+',')
            f.write(d.mp3+',')
            f.write('\n')


if __name__ == "__main__":
    scope = 'user-library-read'
    username = 'moin'
    token = util.prompt_for_user_token(username, scope, client_id = '52ad70b443924859a4d52c63500c769c',
            client_secret = '33a02bc3e5c74789b11c3696bc1af671', redirect_uri = 'http://www.uci.edu/')

    if token:
        # print token
        sp = spotipy.Spotify(auth=token)
        # print sp.track('2Gy3tEwecEcO45QDNtiAti')
        # result1 = sp.recommendation_genre_seeds()
        # genre = result1['genres'][0]
        n = 500 # number of song to retrieve
        genres=['jazz', 'pop', 'country', 'folk', 'hip-hop', 'r-n-b', 'rock', 'metal', 'house', 'salsa', 'classical', 'dubstep', 'techno', 'trance', 'electronic'] #, opera', 'tango' #rap instrumental
        for g in genres:
            print 'Genre:',g 
            retrieved_songs = retrieve_song(g, n)
            downloadMP3(retrieved_songs, g)
            writeCSV(retrieved_songs, g)
    else:
        print "Can't get token for", username

# usful to find genres when searching on artist type....
# for k in ['genres', 'uri']:
# 	print k, results['artists']['items'][0][k]

# trying to find genres from album # all of them are empty []
# print results['tracks']['items'][0]['album']['uri']
# results2 = client.album(results['tracks']['items'][0]['album']['uri'])
# print results2
