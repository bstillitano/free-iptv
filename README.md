# free-iptv

Free, legal TV channels from Australia, the UK, the US and Malta, as M3U playlists with a TV guide.

Only official, free-to-watch streams are included: broadcaster streams (Seven, 9, 10, ABC, SBS via
[i.mjh.nz](https://i.mjh.nz)), free ad-supported services (Pluto TV, Samsung TV Plus, Tubi, Plex, Roku),
and Smash Malta's public web player. No paid channels, restreams or raw-IP feeds.

## Playlists

| Playlist | Channels | Link |
|---|---|---|
| Everything (AU, UK, US, Malta) | 1,071 | `https://raw.githubusercontent.com/bstillitano/free-iptv/main/playlists/free-tv.m3u` |
| Australia + UK + Malta | 356 | `https://raw.githubusercontent.com/bstillitano/free-iptv/main/playlists/au-uk-mt.m3u` |
| US (part 1) | 358 | `https://raw.githubusercontent.com/bstillitano/free-iptv/main/playlists/us-1.m3u` |
| US (part 2) | 357 | `https://raw.githubusercontent.com/bstillitano/free-iptv/main/playlists/us-2.m3u` |

The split playlists stay under Plex's ~480-channel limit per tuner. Otherwise, use **Everything**.

## TV guide (EPG)

```
https://raw.githubusercontent.com/bstillitano/free-iptv/main/epg/epg.xml.gz
```

The playlists already reference this guide, so most apps load it automatically. It's rebuilt
twice a day by a GitHub Action from Matt Huisman's guides, keeping only channels in these playlists.
Not every channel has guide data.

## Using it

Paste a playlist link into an IPTV app: TiviMate (Android TV / Fire TV), IPTVX or UHF (Apple devices),
IPTV Smarters, or VLC (no guide). If the guide doesn't appear, add the EPG link in the app's settings.

The Australian free-to-air channels (Seven, 9, 10, ABC, SBS) only play from inside Australia.
Streams come and go, so some channels will stop working over time.
