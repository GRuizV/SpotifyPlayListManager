/* eslint-disable no-restricted-syntax */


// CONSTANTS AND ENVIRONMENT VARIABLES SETTING
require('dotenv').config();
const fetch = require('node-fetch');
const fs = require('fs');
const CryptoJS = require('crypto-js');

const UserController = require('../controllers/userController');

const CLIENT_ID = process.env.SPOTIFY_API_CLIENT_ID;
const CLIENT_SECRET = process.env.SPOTIFY_API_CLIENT_SECRET;

const PLAYLIST_NAME = 'Discover Daily';
const PLAYLIST_DESCRIPTION =
  "If you would like to support Discoverify, consider visiting patreon.com/discoverify (COMPLETELY OPTIONAL). Daily music, curated for you based on your listening history. If you don't want to get this daily playlist anymore, you can unsubscribe at https://discoverifymusic.com";

function SpotifyAPIException(deleteUser) {
  this.deleteUser = deleteUser;
}




// MAIN CLASS
class SpotifyHelper {


  /* 
  This function validates, with a refreshed token the communication with the Spotify server
  to make authenticated requests on behalf of the user.  
  */
  static async getNewAccessToken(refreshToken) {

    const details = {
      grant_type: 'refresh_token',
      refresh_token: refreshToken,
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET,
    };



    let formBody = [];
    // eslint-disable-next-line guard-for-in
    for (const property in details) {
      const encodedKey = encodeURIComponent(property);
      const encodedValue = encodeURIComponent(details[property]);
      formBody.push(`${encodedKey}=${encodedValue}`);
    }
    formBody = formBody.join('&');



    const result = await fetch(`https://accounts.spotify.com/api/token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formBody,
    });



    const resultJSON = await result.json();

    if (resultJSON.error === 'invalid_grant') {
      throw new SpotifyAPIException(true);
    }

    return resultJSON.access_token;
  }

  // FUNCTION REVIEWED




  /*
  This function is similar to the last one, and they differ in the moment is used.
  This one, is used once, when initially the user authorize the app for making the requests
  and the the before this is used periodically, since the tokens expires within a time period,
  so to avoid keep asking the user for re-authorization, the function above gets a new one. 
  */
  static async getRefreshToken(code, redirectUri) {

    const details = {
      grant_type: 'authorization_code',
      code,
      redirect_uri: redirectUri,
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET,
    };

    let formBody = [];
    // eslint-disable-next-line guard-for-in
    for (const property in details) {
      const encodedKey = encodeURIComponent(property);
      const encodedValue = encodeURIComponent(details[property]);
      formBody.push(`${encodedKey}=${encodedValue}`);
    }
    formBody = formBody.join('&');

    const response = await fetch('https://accounts.spotify.com/api/token', {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formBody,
    });

    return response.json();
  }

  // FUNCTION REVIEWED





  /*
  This function fetches the top 20 tracks (or artists) from the user sessions, and handles errors
  */
  static async getTop(type, range, accessToken) {

    try {
      const result = await fetch(
        `https://api.spotify.com/v1/me/top/${type}?limit=20&time_range=${range}`,
        {
          Accepts: 'application/json',
          method: 'GET',
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );

      const resultJSON = await result.json();

      return resultJSON.items.map((x) => x.id);

    } catch (e) {
      const result = await fetch(
        `https://api.spotify.com/v1/me/top/${type}?limit=20&time_range=${range}`,
        {
          Accepts: 'application/json',
          method: 'GET',
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );

      const resultJSON = await result.json();

      return resultJSON.items.map((x) => x.id);
    }
  }

  // FUNCTION REVIEWED






  /*
  This function collect for different time ranges (All time, medium term and short term) listener habits,
  both in tracks and artists
  */
  // eslint-disable-next-line camelcase
  static async getAllTop(playlistOptions, access_token) {

    const allTimeArtists = playlistOptions.seeds.includes('AA')
      ? await this.getTop('artists', 'long_term', access_token)
      : null;

    const allTimeTracks = playlistOptions.seeds.includes('AT')
      ? await this.getTop('tracks', 'long_term', access_token)
      : null;

      
    const mediumTermArtists = playlistOptions.seeds.includes('MA')
      ? await this.getTop('artists', 'medium_term', access_token)
      : null;

    const mediumTermTracks = playlistOptions.seeds.includes('MT')
      ? await this.getTop('tracks', 'medium_term', access_token)
      : null;


    const shortTermArtists = playlistOptions.seeds.includes('SA')
      ? await this.getTop('artists', 'short_term', access_token)
      : null;

    const shortTermTracks = playlistOptions.seeds.includes('ST')
      ? await this.getTop('tracks', 'short_term', access_token)
      : null;



    return {
      allTime: { artists: allTimeArtists, tracks: allTimeTracks },
      mediumTerm: { artists: mediumTermArtists, tracks: mediumTermTracks },
      shortTerm: { artists: shortTermArtists, tracks: shortTermTracks },
    };
  }

  // FUNCTION REVIEWED






  /*
  From a parameter (playlistOptions) passed, the function will pick randomly tracks and artists
  presumably as seed to generate later the final playlist.
  */
  static getSeeds(playlistOptions, top) {

    const artists = [];
    const tracks = [];

    for (let i = 0; i < playlistOptions.seeds.length; i += 1) {

      switch (playlistOptions.seeds[i]) {

        case 'AT':

          if (top.allTime.tracks.length > 0) {
            const index = Math.floor(Math.random() * top.allTime.tracks.length);
            tracks.push(top.allTime.tracks[index]);
            top.allTime.tracks.splice(index, 1);
          }
          break;


        case 'MT':

          if (top.mediumTerm.tracks.length > 0) {
            const index = Math.floor(
              Math.random() * top.mediumTerm.tracks.length
            );
            tracks.push(top.mediumTerm.tracks[index]);
            top.mediumTerm.tracks.splice(index, 1);
          }
          break;


        case 'ST':

          if (top.shortTerm.tracks.length > 0) {
            const index = Math.floor(
              Math.random() * top.shortTerm.tracks.length
            );
            tracks.push(top.shortTerm.tracks[index]);
            top.shortTerm.tracks.splice(index, 1);
          }
          break;


        case 'AA':

          if (top.allTime.artists.length > 0) {
            const index = Math.floor(
              Math.random() * top.allTime.artists.length
            );
            artists.push(top.allTime.artists[index]);
            top.allTime.artists.splice(index, 1);
          }
          break;


        case 'MA':

          if (top.mediumTerm.artists.length > 0) {
            const index = Math.floor(
              Math.random() * top.mediumTerm.artists.length
            );
            artists.push(top.mediumTerm.artists[index]);
            top.mediumTerm.artists.splice(index, 1);
          }
          break;


        case 'SA':

          if (top.shortTerm.artists.length > 0) {
            const index = Math.floor(
              Math.random() * top.shortTerm.artists.length
            );
            artists.push(top.shortTerm.artists[index]);
            top.shortTerm.artists.splice(index, 1);
          }
          break;


        default:

          throw new Error(
            `Unexpected seed value found: ${playlistOptions.seeds[i]}`
          );
      }
    }

    return { artists, tracks };
  }

  // FUNCTION REVIEWED







 /*
  This function makes a request to spotify for checking if the tracks passed are within the
  users liked tracks.
  */
  static async getLiked(trackIds, accessToken) {
    const result = await fetch(
      `https://api.spotify.com/v1/me/tracks/contains?ids=${trackIds.join(',')}`,
      {
        Accepts: 'application/json',
        method: 'GET',
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );

    return result.json();
  }
 // FUNCTION REVIEWED






 /*
  What this function does is:
  1. It constructs a base URL for Spotify API recommendations with a limit of 50.
  2. It appends seed_artists and seed_tracks to the URL if they are provided in the seeds parameter.
  3. It constructs two URLs: minMaxUrl and targetUrl, based on the user's playlistOptions.
    - minMaxUrl includes the minimum and maximum values for each parameter (acousticness, danceability, energy, etc.).
    - targetUrl calculates the target value as the average of the minimum and maximum values for each parameter.
  4. It returns a dictionary containing minMaxUrl and targetUrl.
  */
  static getRecommendationUrls(user, seeds) {


    let baseUrl = 'https://api.spotify.com/v1/recommendations?limit=50';

    if (seeds.artists.length > 0) {
      baseUrl += `&seed_artists=${seeds.artists.join(',')}`;
    }

    if (seeds.tracks.length > 0) {
      baseUrl += `&seed_tracks=${seeds.tracks.join(',')}`;
    }


    let minMaxUrl = baseUrl;

    minMaxUrl += `&min_acousticness=${
      user.playlistOptions.acousticness[0] / 100
    }&max_acousticness=${user.playlistOptions.acousticness[1] / 100}`;
    minMaxUrl += `&min_danceability=${
      user.playlistOptions.danceability[0] / 100
    }&max_danceability=${user.playlistOptions.danceability[1] / 100}`;
    minMaxUrl += `&min_energy=${
      user.playlistOptions.energy[0] / 100
    }&max_energy=${user.playlistOptions.energy[1] / 100}`;
    minMaxUrl += `&min_instrumentalness=${
      user.playlistOptions.instrumentalness[0] / 100
    }&max_instrumentalness=${user.playlistOptions.instrumentalness[1] / 100}`;
    minMaxUrl += `&min_popularity=${user.playlistOptions.popularity[0]}&max_popularity=${user.playlistOptions.popularity[1]}`;
    minMaxUrl += `&min_valence=${
      user.playlistOptions.valence[0] / 100
    }&max_valence=${user.playlistOptions.valence[1] / 100}`;




    let targetUrl = baseUrl;

    targetUrl += `&target_acousticness=${
      (user.playlistOptions.acousticness[0] +
        user.playlistOptions.acousticness[1]) /
      200
    }`;
    targetUrl += `&target_danceability=${
      (user.playlistOptions.danceability[0] +
        user.playlistOptions.danceability[1]) /
      200
    }`;
    targetUrl += `&target_energy=${
      (user.playlistOptions.energy[0] + user.playlistOptions.energy[1]) / 200
    }`;
    targetUrl += `&target_instrumentalness=${
      (user.playlistOptions.instrumentalness[0] +
        user.playlistOptions.instrumentalness[1]) /
      200
    }`;
    targetUrl += `&target_popularity=${Math.round(
      (user.playlistOptions.popularity[0] +
        user.playlistOptions.popularity[1]) /
        2
    )}`;
    targetUrl += `&target_valence=${
      (user.playlistOptions.valence[0] + user.playlistOptions.valence[1]) / 200
    }`;

    return { minMaxUrl, targetUrl };
  }
 // FUNCTION REVIEWED






 /*
  What this function does is:

  1. Initialization: It initializes constants and variables, including the playlist size and the usr variable, which is either the provided user or, if user.playlistOptions is falsy, 
  it fetches the playlist options from the database using UserController.restorePlaylistOptions(userId).
  2. Building Recommendation URLs: It calls the getRecommendationUrls function to construct two URLs for fetching recommendations based on the user's preferences and seeds.
  3. Fetching Recommendations: It fetches recommendations from Spotify using fetch(minMaxUrl, ...) and handles the response, including a retry mechanism in case of an error.
  4. Processing Recommendations: It extracts track IDs and URIs from the recommendation response and filters out tracks that are already liked or in the user's playlist.
  5. Fetching Additional Recommendations: If the number of tracks for the playlist is still below the desired size, it fetches additional recommendations using the targetUrl.
  6. Finalizing Playlist: It combines the tracks from the initial and additional recommendations, ensuring that the playlist size does not exceed the limit and that liked tracks 
  and tracks already in the playlist are included appropriately.
  7. Returning Playlist: It returns an array of URIs for the tracks to be added to the playlist.
  
  This function essentially generates a playlist of tracks based on the user's preferences and Spotify's recommendations, 
  ensuring that the playlist contains diverse and appealing tracks while avoiding duplicates and tracks the user has already liked or added to their playlist.
  */
  static async getTracks(user, userId, tracksInPlaylist, seeds, accessToken) {

    const PLAYLIST_SIZE = 30;
    let usr = user;

    if (!user.playlistOptions) {
      usr = await UserController.restorePlaylistOptions(userId);
    }

    const { minMaxUrl, targetUrl } = this.getRecommendationUrls(usr, seeds);

    let recommendations = await fetch(minMaxUrl, {
      Accepts: 'application/json',
      method: 'GET',
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });


    let responseJSON;
    try {
      responseJSON = await recommendations.json();
    } catch (e) {
      // eslint-disable-next-line no-use-before-define
      console.log(responseJSON);
      console.log(e);

      await new Promise((r) => setTimeout(r, 1000));

      recommendations = await fetch(minMaxUrl, {
        Accepts: 'application/json',
        method: 'GET',
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });

      responseJSON = await recommendations.json();
    }


    const tracks = responseJSON.tracks || [];


    const trackIds = [];
    const uris = [];

    for (let i = 0; i < tracks.length; i += 1) {
      trackIds.push(tracks[i].id);
      uris.push(tracks[i].uri);
    }



    const liked =
      tracks.length === 0 ? [] : await this.getLiked(trackIds, accessToken);

    const likedTracks = new Set();
    const alreadyInPlaylist = new Set();
    const playlistUris = new Set();


    for (let i = 0; i < liked.length; i += 1) {

      if (!liked[i]) {
        playlistUris.add(uris[i]);
      } else {
        likedTracks.add(uris[i]);
      }

      if (tracksInPlaylist.has(trackIds[i])) {
        alreadyInPlaylist.add(uris[i]);
      }

      if (playlistUris.size >= PLAYLIST_SIZE) break;
    }


    if (playlistUris.size < PLAYLIST_SIZE) {

      const targetRecommendations = await fetch(targetUrl, {
        Accepts: 'application/json',
        method: 'GET',
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });

      const targetResponseJSON = await targetRecommendations.json();
      const targetTracks = targetResponseJSON.tracks || [];

      if (targetTracks.length === 0) {
        return [];
      }

      const targetTrackIds = [];
      const targetUris = [];


      for (let i = 0; i < targetTracks.length; i += 1) {
        targetTrackIds.push(targetTracks[i].id);
        targetUris.push(targetTracks[i].uri);
      }



      const targetLiked = await this.getLiked(targetTrackIds, accessToken);

      for (let i = 0; i < targetLiked.length; i += 1) {

        if (!targetLiked[i]) {
          playlistUris.add(targetUris[i]);
        } else {
          likedTracks.add(targetUris[i]);
        }

        if (tracksInPlaylist.has(targetTrackIds[i])) {
          alreadyInPlaylist.add(targetUris[i]);
        }

        if (playlistUris.size >= PLAYLIST_SIZE) break;
      }
    }



    for (const track of alreadyInPlaylist) {
      if (playlistUris.size >= PLAYLIST_SIZE) break;

      if (!likedTracks.has(track)) {
        playlistUris.add(track);
      }
    }


    for (const track of likedTracks) {
      if (playlistUris.size >= PLAYLIST_SIZE) break;

      playlistUris.add(track);
    }

    return Array.from(playlistUris);
  }
  //FUNCTION REVIEWED







  /*
  What this function does is literally update the playlist with the tracks passed 
  and prompts the HTTP response
  */
  static async updatePlaylistTracks(playlistId, tracks, accessToken) {

    await fetch(`https://api.spotify.com/v1/playlists/${playlistId}/tracks`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${accessToken}`,
      },
      body: JSON.stringify({
        uris: tracks,
      }),
    });
  }
  // FUNCTION REVIEWED





  /*
  What this function does is retrieve a playlist from the Spotify API using its ID. 
  It then checks if the owner of the playlist is the same as the provided user ID. 
  If they match, it returns the playlist JSON object; otherwise, it returns null. 
  The function also handles any errors that may occur during the API request, logging the error and returning null.
  */
  static async getPlaylist(userId, playlistId, accessToken) {

    if (!playlistId) return null;

    let resultJSON;

    try {

      const result = await fetch(
        `https://api.spotify.com/v1/playlists/${playlistId}`,
        {
          Accepts: 'application/json',
          method: 'GET',
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );

      resultJSON = await result.json();

      return resultJSON.owner.id === userId ? resultJSON : null;

    } catch (e) {
      console.log(resultJSON);
      console.log(e);


      const result = await fetch(
        `https://api.spotify.com/v1/playlists/${playlistId}`,
        {
          Accepts: 'application/json',
          method: 'GET',
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );

      resultJSON = await result.json();

      return resultJSON.owner.id === userId ? resultJSON : null;
    }
  }
  // FUNCTION REVIEWED








  /*
  What this function does is create straighforward the 'Discoverify' playlist
  */
  static async createPlaylist(user, userId, accessToken) {

    const response = await fetch(
      `https://api.spotify.com/v1/users/${userId}/playlists`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify({
          name: PLAYLIST_NAME,
          public: false,
          description: PLAYLIST_DESCRIPTION,
        }),
      }
    );

    const responseJSON = await response.json();

    user.playlistId = responseJSON.id;

    return responseJSON;
  }
  // FUNCTION REVIEWED






  /*
  What this function does is to retrive the data from the user autheticated in the app
  */
  static async getMe(accessToken) {
    const response = await fetch('https://api.spotify.com/v1/me', {
      Accepts: 'application/json',
      method: 'GET',
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    return response.json();
  }
 // FUNCTION REVIEWED







  /*
  What this function does is to retrive the user's playlists up to 50 of them.
  */
  static async getUserPlaylists(accessToken) {
    const response = await fetch(
      'https://api.spotify.com/v1/me/playlists?limit=50',
      {
        Accepts: 'application/json',
        method: 'GET',
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );

    return response.json();
  }
 // FUNCTION REVIEWED





 /*
  This function appears to simplify others, so it only sets the headers for requesting something to the spotify endpoints.
  */
  static async getGenericFetch(uri, accessToken) {
    const response = await fetch(uri, {
      Accepts: 'application/json',
      method: 'GET',
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    return response.json();
  }
 // FUNCTION REVIEWED








  /*
  This function validates against the user playlist if a specific playlist exist with a playlist ID
  */
  static async doesMyPlaylistExists(playlistId, accessToken) {

    let playlists = await this.getUserPlaylists(accessToken);

    if (!playlists || !playlists.items) {
      return false;
    }

    let { next } = playlists;

    do {
      for (let i = 0; i < playlists.items.length; i += 1) {
        if (playlists.items[i].id === playlistId) {
          return true;
        }
      }

      if (next) {
        playlists = await this.getGenericFetch(next, accessToken);
        next = playlists.next;
      }
    } while (next);

    return false;
  }
 // FUNCTION REVIEWED




  /*
  This function updates the cover of the playlist
  */
  static async addPlaylistCover(playlistId, encodedImage, accessToken) {

    await fetch(`https://api.spotify.com/v1/playlists/${playlistId}/images`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'image/jpeg',
        Authorization: `Bearer ${accessToken}`,
      },
      body: fs.createReadStream(encodedImage),
    });
  }
  // FUNCTION REVIEWED





  '******* CORE FUNCTION *******'
  /*
  This function does this:
    
    1. Decrypts the user's userId using AES decryption.
    2. Retrieves a new access token using the user's refreshToken.
    3. Retrieves the seed options for the playlist based on the user's playlist options and their Spotify listening history.
    4. Checks if the user's playlist already exists and if the Spotify playlist with the given playlistId exists.
    5. If the user's playlist or the Spotify playlist does not exist, it creates a new playlist for the user.
    6. Retrieves the existing tracks in the playlist to avoid adding duplicates.
    7. Gets new tracks based on the user's playlist options and listening history.
    8. Updates the playlist with the new tracks.
    9. Updates the user's lastUpdated field and saves the user object.
    10. Optionally, adds a new playlist cover image if playlistCover is provided.
    11. Handles errors, such as deleting the user if necessary.
  */
  static async updatePlaylist(user, playlistCover) {

    console.log(`Starting job for user: ${user.userId}`);

    const userId = CryptoJS.AES.decrypt(
      user.userId,
      CryptoJS.enc.Base64.parse(CLIENT_SECRET),
      {
        mode: CryptoJS.mode.ECB,
      }
    ).toString(CryptoJS.enc.Utf8);

    try {
      const accessToken = await this.getNewAccessToken(user.refreshToken);

      const seeds = this.getAllTop(
        user.playlistOptions,
        accessToken
      ).then((allTop) => this.getSeeds(user.playlistOptions, allTop));

      let playlist = this.getPlaylist(userId, user.playlistId, accessToken);

      const doesMyPlaylistExist = this.doesMyPlaylistExists(
        user.playlistId,
        accessToken
      );

      if (!(await playlist) || !(await doesMyPlaylistExist)) {
        playlist = await this.createPlaylist(user, userId, accessToken);
        console.log('Had to create new playlist');
      }

      const playlistId = (await playlist).id;
      const tracksAlreadyInPlaylist = new Set(
        (await playlist).tracks.items.map((x) => x.track.id)
      );

      const tracks = await this.getTracks(
        user,
        userId,
        tracksAlreadyInPlaylist,
        await seeds,
        accessToken
      );

      console.log(`${tracks.length} tracks found`);

      this.updatePlaylistTracks(playlistId, tracks, accessToken);

      user.lastUpdated = new Date();
      user.save();

      if (playlistCover) {
        await this.addPlaylistCover(playlistId, playlistCover, accessToken);
      }

      console.log(`Playlist updated for user: ${user.userId}`);
    } catch (e) {
      console.log(e);

      if (e.deleteUser) {
        console.log(`Deleting User: ${userId}`);
        // await UserController.deleteUser(userId);
        return;
      }
    }

    console.log(' ');
  }
 // FUNCTION REVIEWED







  /*
  This function does the Discovery playlist update for a number of users
  */
  static async updatePlaylists(users) {

    console.log(`running ${users.length} jobs | ${new Date()}`);
    // const playlistCover = 'images/playlistCover.jpeg';
    // await Promise.all(users.map(user => this.updatePlaylist(user, null)));

    const failures = [];

    for (let i = 0; i < users.length; i += 1) {

      try {
        console.log(`${i + 1}/${users.length}`);
        await this.updatePlaylist(users[i], null);

      } catch (e) {
        console.log(e);
        failures.push(users[i]);
      }
    }

    console.log();
    console.log(`running ${failures.length} failure jobs | ${new Date()}`);

    for (let i = 0; i < failures.length; i += 1) {
      try {
        console.log(`${i + 1}/${failures.length}`);
        await this.updatePlaylist(failures[i], null);
      } catch (e) {
        console.log(e);
      }
    }

    console.log(`${users.length} jobs complete | ${new Date()}`);
  }
 // FUNCTION REVIEWED






  /*
  This function runs the same process of the updatePlaylist function but does not actually updates it,
  it only throw statuses for each one.
  */
  static async updatePlaylistsNoUpdate() {

    const users = await UserController.getAllUsers();

    console.log(`running ${users.length} jobs | ${new Date()}`);
    // const playlistCover = 'images/playlistCover.jpeg';
    // await Promise.all(users.map(user => this.updatePlaylist(user, null)));

    for (let i = 0; i < users.length; i += 1) {
      try {
        const user = users[i];
        console.log(`Running no update for user: ${user.userId}`);

        const userId = CryptoJS.AES.decrypt(
          user.userId,
          CryptoJS.enc.Base64.parse(CLIENT_SECRET),
          {
            mode: CryptoJS.mode.ECB,
          }
        ).toString(CryptoJS.enc.Utf8);

        const accessToken = await this.getNewAccessToken(user.refreshToken);

        const seeds = this.getAllTop(
          user.playlistOptions,
          accessToken
        ).then((allTop) => this.getSeeds(user.playlistOptions, allTop));

        const playlist = this.getPlaylist(userId, user.playlistId, accessToken);

        const doesMyPlaylistExist = this.doesMyPlaylistExists(
          user.playlistId,
          accessToken
        );

        if (!(await playlist) || !(await doesMyPlaylistExist)) {
          console.log('HAD TO CREATE NEW PLAYLIST');
        }

        const playlistId = (await playlist).id;
        const tracksAlreadyInPlaylist = new Set(
          (await playlist).tracks.items.map((x) => x.track.id)
        );

        const tracks = await this.getTracks(
          user,
          userId,
          tracksAlreadyInPlaylist,
          await seeds,
          accessToken
        );

        console.log(`${tracks.length} tracks found`);
        console.log('Playlist ID', playlistId);
        console.log('PLAYLIST EXISTS', await doesMyPlaylistExist);

        console.log(' ');

      } catch (e) {
        console.log(e);
      }
    }

    console.log(`${users.length} jobs complete | ${new Date()}`);
  }
  // FUNCTION REVIEWED

}






module.exports = SpotifyHelper;
