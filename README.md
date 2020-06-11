## About
Python script to upload videos on YouTube using Selenium
that allows to upload more than 6<sup>1</sup> videos per day 
which is the maximum [[1]](https://github.com/tokland/youtube-upload/issues/268) for all other tools that use the [YouTube Data API v3](https://developers.google.com/youtube/v3).

###### <sup>1</sup>: Since the projects that enable the YouTube Data API have a default quota allocation of `10,000` units per day [[2]](https://developers.google.com/youtube/v3/getting-started#calculating-quota-usage) and a video upload has a cost of approximately `1,600` units [[3]](https://developers.google.com/youtube/v3/getting-started#quota): `10,000 / 1,600 = 6.25`.

Instead, this script is only restricted by a daily upload limit for a channel on YouTube:
> 100 videos is the limit in the first 24 hours, then drops to 50 every 24 hours after that. [[4]](https://support.google.com/youtube/thread/1187675?hl=en)

## Installation

```bash
git clone https://github.com/linouk23/youtube-uploader-selenium
cd youtube-uploader-selenium
```

## Usage
At a minimum, just specify a video:

```bash
python3 upload.py --video rockets.flv
```

If it is the first time you've run the script, a browser window should popup and prompt you to provide YouTube credentials (and then simply press <it>Enter</it> after a successful login).
A token will be created and stored in a file in the local directory for subsequent use.

Video title, description and other metadata can specified via a JSON file using the `--meta` flag:
```bash
python3 upload.py --video rockets.flv --meta metadata.json
```

An example JSON file would be:
```json
{
  "title": "Best Of James Harden | 2019-20 NBA Season",
  "description": "Check out the best of James Harden's 2019-20 season so far!",
  "tags": ["nba", "rockets", "harden"],
}
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Feedback
If you find a bug / want a new feature to be added, please [open an issue](https://github.com/tokland/youtube-upload/issues).

## FAQ
TODO: add popular questions

## License
[MIT](https://choosealicense.com/licenses/mit/)