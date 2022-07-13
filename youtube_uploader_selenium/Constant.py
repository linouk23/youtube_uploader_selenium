class Constant:
    """A class for storing constants for YoutubeUploader class"""
    YOUTUBE_URL = 'https://www.youtube.com'
    YOUTUBE_STUDIO_URL = 'https://studio.youtube.com'
    YOUTUBE_UPLOAD_URL = 'https://www.youtube.com/upload'
    USER_WAITING_TIME = 1
    VIDEO_TITLE = 'title'
    VIDEO_DESCRIPTION = 'description'
    VIDEO_TAGS = 'tags'
    DESCRIPTION_CONTAINER = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/' \
                            'ytcp-uploads-details/div/ytcp-uploads-basics/ytcp-mention-textbox[2]'
    TEXTBOX_ID = 'textbox'
    TEXT_INPUT = 'text-input'
    RADIO_LABEL = 'radioLabel'
    STATUS_CONTAINER = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/' \
                       'div/div[1]/ytcp-video-upload-progress/span'
    NOT_MADE_FOR_KIDS_LABEL = 'VIDEO_MADE_FOR_KIDS_NOT_MFK'

    # Thanks to romka777
    ADVANCED_BUTTON_ID = 'toggle-button'
    TAGS_INPUT_CONTAINER_ID = 'chip-bar'

    TAGS_INPUT = 'text-input'
    NEXT_BUTTON = 'next-button'
    PUBLIC_BUTTON = 'PUBLIC'
    VIDEO_URL_CONTAINER = "//span[@class='video-url-fadeable style-scope ytcp-video-info']"
    VIDEO_URL_ELEMENT = "//a[@class='style-scope ytcp-video-info']"
    HREF = 'href'
    UPLOADED = 'Uploading'
    ERROR_CONTAINER = '//*[@id="error-message"]'
    VIDEO_NOT_FOUND_ERROR = 'Could not find video_id'
    DONE_BUTTON = 'done-button'
    INPUT_FILE_VIDEO = "//input[@type='file']"
    INPUT_FILE_THUMBNAIL = "//input[@id='file-loader']"

    # Playlist
    VIDEO_PLAYLIST = 'playlist'
    PL_DROPDOWN_CLASS = 'ytcp-video-metadata-playlists'
    PL_SEARCH_INPUT_ID = 'search-input'
    PL_ITEMS_CONTAINER_ID = 'items'
    PL_ITEM_CONTAINER = '//span[text()="{}"]'
    PL_NEW_BUTTON_CLASS = 'new-playlist-button'
    PL_CREATE_PLAYLIST_CONTAINER_ID = 'create-playlist-form'
    PL_CREATE_BUTTON_CLASS = 'create-playlist-button'

