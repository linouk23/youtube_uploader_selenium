"""This module implements uploading videos on YouTube via Selenium using metadata JSON file
    to extract its title, description etc."""

import json
from time import sleep
from pathlib import Path
import logging
import platform
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional, DefaultDict

from selenium_firefox.firefox import Firefox, By, Keys
from .Constant import *

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def load_metadata(metadata_path: Optional[str] = None) -> DefaultDict[str, str]:
    if metadata_path is None:
        return defaultdict(str)
    with open(metadata_path, encoding='utf-8') as metadata_file:
        return defaultdict(str, json.load(metadata_file))


@dataclass
class YouTubeVideo:
    path: str
    thumbnail: str = ''
    title: str = ''
    description: str = ''
    tags: list = field(default_factory=lambda: [])
    category: str = ''
    language: str = ''

    def __post_init__(self):
        if not Path(self.path).is_file():
            logger.error(f'Video file does not exist or was not found at "{self.path}"')
            return
        # Could do more user feedback regarding errors here
        self.tags = ','.join(self.tags) if isinstance(self.tags, list) else self.tags
        if not self.title: 
            self.title = Path(self.path).stem
            logger.warning(f'The video title was set to {self.title}')

    @classmethod
    def from_file(cls, video_path: str, metadata_path: Optional[str]) -> 'YouTubeVideo':
        metadata_dict = load_metadata(metadata_path)

        return cls(
            path=video_path,
            thumbnail=metadata_dict.get(Constant.VIDEO_THUMBNAIL),
            title=metadata_dict.get(Constant.VIDEO_TITLE),
            description=metadata_dict.get(Constant.VIDEO_DESCRIPTION),
            tags=metadata_dict.get(Constant.VIDEO_TAGS),
            category=metadata_dict.get(Constant.VIDEO_CATEGORY),
            language=metadata_dict.get(Constant.VIDEO_LANGUAGE),
        )


class YouTubeUploader:
    """A class for uploading videos on YouTube via Selenium using metadata JSON file
    to extract its title, description etc"""

    def __init__(self, youtube_video: YouTubeVideo) -> None:
        self.video = youtube_video
        current_working_dir = str(Path.cwd())
        self.browser = Firefox(current_working_dir, current_working_dir)
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        self.is_mac = not any(os_name in platform.platform() for os_name in ["Windows", "Linux"])

    def upload(self):
        try:
            self.__login()
            return self.__upload()
        except Exception as e:
            print(e)
            self.__quit()
            raise

    def __login(self):
        
        self.browser.get(Constant.YOUTUBE_URL)
        sleep(Constant.USER_WAITING_TIME)

        if not self.browser.has_cookies_for_current_website():  # TODO: actively check if we're logged in
            logger.info('Please sign in and then press enter')
            input()
            self.browser.get(Constant.YOUTUBE_URL)
            sleep(Constant.USER_WAITING_TIME)
            self.browser.save_cookies()

        self.browser.load_cookies()
        sleep(Constant.USER_WAITING_TIME)
        self.browser.refresh()

    def __write_in_field(self, field, string, select_all=False):
        self.browser.driver.execute_script("arguments[0].click();", field)
        sleep(Constant.USER_WAITING_TIME)
        if select_all:
            if self.is_mac:
                field.send_keys(Keys.COMMAND + 'a')
            else:
                field.send_keys(Keys.CONTROL + 'a')
            sleep(Constant.USER_WAITING_TIME)
        field.send_keys(string)

    def __upload(self) -> (bool, Optional[str]):
        self.browser.get(Constant.YOUTUBE_URL)
        sleep(Constant.USER_WAITING_TIME)
        self.browser.get(Constant.YOUTUBE_UPLOAD_URL)
        sleep(Constant.USER_WAITING_TIME)

        # Video Upload
        absolute_video_path = str(Path.cwd() / self.video.path)
        self.browser.find(By.XPATH, Constant.INPUT_FILE_VIDEO).send_keys(absolute_video_path)
        logger.debug(f'Attached video {self.video.path}')

        # Thumbnail Selection
        if self.video.thumbnail:
            absolute_thumbnail_path = str(Path.cwd() / self.video.thumbnail)
            self.browser.find(By.XPATH, Constant.INPUT_FILE_THUMBNAIL).send_keys(absolute_thumbnail_path)
            change_display = "document.getElementById('file-loader').style = 'display: block! important'"
            self.browser.driver.execute_script(change_display)
            logger.debug(f'Attached thumbnail {self.video.thumbnail}')

        # Video Title
        title_field = self.browser.find(By.ID, Constant.TEXTBOX, timeout=15)
        self.__write_in_field(title_field, self.video.title, select_all=True)
        logger.debug(f'The video title was set to "{self.video.title}"')

        # Video Description
        if self.video.description:
            video_description = self.video.description.replace("\n", Keys.ENTER);
            description_field = self.browser.find_all(By.ID, Constant.TEXTBOX)[1]
            self.__write_in_field(description_field, video_description, select_all=True)
            logger.debug('Description filled.')

        # Kids Selection
        kids_section = self.browser.find(
            By.NAME, Constant.NOT_MADE_FOR_KIDS_LABEL)
        self.browser.find(By.ID, Constant.RADIO_LABEL, kids_section).click()
        logger.debug('Selected \"{}\"'.format(Constant.NOT_MADE_FOR_KIDS_LABEL))

        # Advanced options
        self.browser.find(By.XPATH, Constant.MORE_BUTTON).click()
        logger.debug('Clicked MORE OPTIONS')

        if self.video.tags:
            tags_container = self.browser.find(By.XPATH, Constant.TAGS_INPUT)
            tags_container.send_keys(self.video.tags)
            logger.debug(f'The tags were set to "{self.video.tags}"')

        if self.video.language:
            self.browser.find(By.XPATH, Constant.LANGUAGE_DROPDOWN).click()
            self.browser.find(By.XPATH, Constant.LANGUAGE_SELECTION.format(LANGUAGE=self.video.language)).click()
            logger.debug(f'Set Video Language to {self.video.language}')

        if self.video.category:
            self.browser.find(By.XPATH, Constant.CATEGORY_DROPDOWN).click()
            self.browser.find(
                By.XPATH, 
                Constant.CATEGORY_SELECTION.format(
                    CATEGORY_SELECTION=self.video.category
                )
            ).click()
            logger.debug(f'Set Category to {self.video.category}')

        self.browser.find(By.ID, Constant.NEXT_BUTTON).click()
        logger.debug('Clicked {} one'.format(Constant.NEXT_BUTTON))

        # Thanks to romka777
        self.browser.find(By.ID, Constant.NEXT_BUTTON).click()
        logger.debug('Clicked {} two'.format(Constant.NEXT_BUTTON))

        self.browser.find(By.ID, Constant.NEXT_BUTTON).click()
        logger.debug('Clicked {} three'.format(Constant.NEXT_BUTTON))
        public_main_button = self.browser.find(By.NAME, Constant.PUBLIC_BUTTON)
        self.browser.find(By.ID, Constant.RADIO_LABEL,
                          public_main_button).click()
        logger.debug('Made the video {}'.format(Constant.PUBLIC_BUTTON))

        video_id = self.__get_video_id()

        status_container = self.browser.find(By.XPATH,
                                             Constant.STATUS_CONTAINER)
        while True:
            in_process = status_container.text.find(Constant.UPLOADED) != -1
            if in_process:
                sleep(Constant.USER_WAITING_TIME)
            else:
                break

        done_button = self.browser.find(By.ID, Constant.DONE_BUTTON)

        # Catch such error as
        # "File is a duplicate of a video you have already uploaded"
        if done_button.get_attribute('aria-disabled') == 'true':
            error_message = self.browser.find(By.XPATH, Constant.ERROR_CONTAINER).text
            logger.error(error_message)
            return False, None

        done_button.click()
        logger.debug(f'Published the video with video_id = {video_id}')
        sleep(Constant.USER_WAITING_TIME)
        self.browser.get(Constant.YOUTUBE_URL)
        self.__quit()
        return True, video_id

    def __get_video_id(self) -> Optional[str]:
        video_id = None
        try:
            video_url_container = self.browser.find(
                By.XPATH, Constant.VIDEO_URL_CONTAINER)
            video_url_element = self.browser.find(By.XPATH, Constant.VIDEO_URL_ELEMENT,
                                                  element=video_url_container)
            video_id = video_url_element.get_attribute(
                Constant.HREF).split('/')[-1]
        except:
            logger.warning(Constant.VIDEO_NOT_FOUND_ERROR)
            pass
        return video_id

    def __quit(self):
        self.browser.driver.quit()