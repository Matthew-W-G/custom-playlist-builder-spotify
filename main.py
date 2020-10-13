import spotipy
from spotipy import oauth2
from spotipy.oauth2 import SpotifyOAuth
import json
import requests
from authorization import *
import spotipy.util as util
import statistics




if __name__ == '__main__':
    print("IN MAIN")


if sp_oauth.is_token_expired(token_info):
    token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    token = token_info['access_token']
    sp = spotipy.Spotify(auth=token)

print("ACCESS TOKEN : " + token_info['access_token'])

sp = spotipy.Spotify(auth=token_info['access_token'])


print('CATEGORY', sp.category_playlists('summer'))

print('TEST TRACKS', sp.track('59qrUpoplZxbIZxk6X0Bm3'))
print('TEST TRACKS', sp.track('2Z8WuEywRWYTKe1NybPQEW'))
print('TEST TRACKS', sp.track('7pYfyrMNPn3wtoCyqcTVoI'))
print('TEST TRACKS', sp.track('7oGZAicScQt96OAW4AruYy'))


print(sp.track('0MOiv7WTXCqvm89lVCf9C8')['artists'][0]['id'])

playlist_results_track_ids = []

def get_my_tracks():
    """
    Gathers user's saved tracks and returns their ids in the form of an array

    : return: array of saved track ids
    """
    saved_tracks_counter = 0
    offset_adjust = 0
    while True:
        count = len(sp.current_user_saved_tracks(limit=40, offset=offset_adjust)['items'])
        if(count == 0):
            break
        else:
            saved_tracks_counter = saved_tracks_counter + count
            offset_adjust = offset_adjust + 40

    print(saved_tracks_counter)

    favorite_tracks_ids = []


    #adding my most played songs to favorite list
    for x in range(50):
        favorite_tracks_ids.append(sp.current_user_top_tracks(limit=1, offset=x)['items'][0]['id'])

    #adding my saved songs to favorite list
    for x in range(saved_tracks_counter):
        favorite_tracks_ids.append(sp.current_user_saved_tracks(limit=1, offset=x)['items'][0]['track']['id'])


    return favorite_tracks_ids

#my_tracks holds ids of saved tracks
my_tracks = get_my_tracks()




def get_playlist_tracks(search_query, my_tracks):
    """
    Compiles a list of tracks related to the search query inputted

    : param search_query: input for topic of songs
    : return: array of saved track ids
    """
    search_query = 'playlist:' + search_query
    playlist_query_results = sp.search(q=search_query, type='playlist')

    playlists_length = len(playlist_query_results['playlists']['items'])

    playlist_results_ids = []

    for i in range(playlists_length):
        playlist_results_ids.append(playlist_query_results['playlists']['items'][i]['id'])

    print('INDEX 0 HEREEEEE', playlist_results_ids[0])
    print(sp.playlist(playlist_results_ids[0]))

    print(sp.playlist(playlist_results_ids[0])['tracks']['items'][0]['track']['id'])

    print('PLAYLIST LENGTH', playlists_length)

    playlist_results_track_ids = []
    for x in range(len(playlist_results_ids)):
        for y in range(len(sp.playlist(playlist_results_ids[x])['tracks']['items'])):
            playlist_results_track_ids.append(sp.playlist(playlist_results_ids[x])['tracks']['items'][y]['track']['id'])

    print(playlist_results_track_ids)


    print("SAVED SONGS: ", my_tracks)
    print("PLAYLIST SONGS: ", playlist_results_track_ids)


    new_playlist_ids = []




    matching_ids = []

    """
    for x in range(len(my_tracks)):
        for y in range(len(playlist_results_track_ids)):
            if my_tracks[x] == playlist_results_track_ids[y]:
                matching_ids.append(my_tracks[x])
    """
    matching_ids = list(set(my_tracks) & set(playlist_results_track_ids))

    print("MATCHING SONGS: ", matching_ids)


    #new_playlist_ids holds ids of songs added to the new playlist

    number_of_matches = len(matching_ids)

    if number_of_matches >= 20:
        number_of_matches = 20

    for i in range(number_of_matches):
        if(len(matching_ids) > 0):
            mode = max(set(matching_ids), key = matching_ids.count)
        new_playlist_ids.append(mode)
        #filters out all the ids that matched the most recent mode
        matching_ids = list(filter(lambda x: x != mode, matching_ids))

    print("NEW PLAYLIST", new_playlist_ids)

    for x in range(number_of_matches):
        print(sp.track(new_playlist_ids[x])['name'])

    return playlist_results_track_ids, new_playlist_ids



def recommend_by_artist(playlist_results_track_ids):
    most_prevalent_tracks = []
    my_top_artists_ids = []
    new_playlist_recommendations = []


    while( len(playlist_results_track_ids) > 0):
        mode = max(set(playlist_results_track_ids), key=playlist_results_track_ids.count)
        most_prevalent_tracks.append(mode)
        playlist_results_track_ids = list(filter(lambda x: x != mode, playlist_results_track_ids))

    for x in range(50):
        my_top_artists_ids.append(sp.current_user_top_artists(limit=1, offset=x)['items'][0]['id'])

    print('here')


    most_prevalent_tracks_artists = []

    #most_prevalent_tracks = most_prevalent_tracks[0:200]

    for x in range(len(most_prevalent_tracks)):
            most_prevalent_tracks_artists.append(sp.track(most_prevalent_tracks[x])['artists'][0]['id'])
        for i in range(25):
            if(len(new_playlist_recommendations) < 10):
                if(sp.track(most_prevalent_tracks[x])['artists'][0]['id'] == my_top_artists_ids[i]):
                    new_playlist_recommendations.append(most_prevalent_tracks[x])
                    print('new', new_playlist_recommendations)


    most_prevalent_tracks

    print('new recs: ', new_playlist_recommendations)


    return new_playlist_recommendations



topic = 'Inspirational'
playlist_results_track_ids, new_playlist_ids = get_playlist_tracks(topic, my_tracks)

new_playlist_ids = recommend_by_artist(playlist_results_track_ids) + new_playlist_ids


custom_playlist = sp.user_playlist_create('giantsdude27','My ' + topic + ' Playlist', False, 'This is a custom playlist with ' + topic + '-related songs, tailored to my interests')

print(custom_playlist)
custom_playlist_id = custom_playlist['id']

print("ID: ", custom_playlist_id )

sp.user_playlist_add_tracks('giantsdude27', custom_playlist_id, new_playlist_ids)

for x in range(len(new_playlist_ids)):
    print(sp.track(new_playlist_ids[x])['name'], 'AUDIO', sp.audio_features(new_playlist_ids[x]))
