"""This module implements uploading videos on YouTube via Selenium using metadata JSON file
	to extract its title, description etc."""

from typing import DefaultDict, Optional
from selenium_firefox.firefox import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from collections import defaultdict
import json
import time
from .Constant import *
from pathlib import Path
import logging
import platform

logging.basicConfig()


def load_metadata(metadata_json_path: Optional[str] = None) -> DefaultDict[str, str]:
	if metadata_json_path is None:
		return defaultdict(str)
	with open(metadata_json_path, encoding='utf-8') as metadata_json_file:
		return defaultdict(str, json.load(metadata_json_file))


class YouTubeUploader:
	"""A class for uploading videos on YouTube via Selenium using metadata JSON file
	to extract its title, description etc"""

	def __init__(self, video_path: str, metadata_json_path: Optional[str] = None, thumbnail_path: Optional[str] = None) -> None:
		self.video_path = video_path
		self.thumbnail_path = thumbnail_path
		self.metadata_dict = load_metadata(metadata_json_path)
		current_working_dir = str(Path.cwd())
		self.browser = Firefox(profile_path = current_working_dir, pickle_cookies = True, full_screen = False)
		self.logger = logging.getLogger(__name__)
		self.logger.setLevel(logging.DEBUG)
		self.__validate_inputs()

		self.is_mac = False
		if not any(os_name in platform.platform() for os_name in ["Windows", "Linux"]):
			self.is_mac = True

		self.logger.debug("Use profile path: {}".format(self.browser.source_profile_path))

	def __validate_inputs(self):
		if not self.metadata_dict[Constant.VIDEO_TITLE]:
			self.logger.warning(
				"The video title was not found in a metadata file")
			self.metadata_dict[Constant.VIDEO_TITLE] = Path(
				self.video_path).stem
			self.logger.warning("The video title was set to {}".format(
				Path(self.video_path).stem))
		if not self.metadata_dict[Constant.VIDEO_DESCRIPTION]:
			self.logger.warning(
				"The video description was not found in a metadata file")

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
		time.sleep(Constant.USER_WAITING_TIME)

		if self.browser.has_cookies_for_current_website():
			self.browser.load_cookies()
			self.logger.debug("Loaded cookies from {}".format(self.browser.cookies_folder_path))
			time.sleep(Constant.USER_WAITING_TIME)
			self.browser.refresh()
		else:
			self.logger.info('Please sign in and then press enter')
			input()
			self.browser.get(Constant.YOUTUBE_URL)
			time.sleep(Constant.USER_WAITING_TIME)
			self.browser.save_cookies()
			self.logger.debug("Saved cookies to {}".format(self.browser.cookies_folder_path))

	def __clear_field(self, field):
		field.click()
		time.sleep(Constant.USER_WAITING_TIME)
		if self.is_mac:
			field.send_keys(Keys.COMMAND + 'a')
		else:
			field.send_keys(Keys.CONTROL + 'a')
		time.sleep(Constant.USER_WAITING_TIME)
		field.send_keys(Keys.BACKSPACE)

	def __write_in_field(self, field, string, select_all=False):
		if select_all:
			self.__clear_field(field)
		else:
			field.click()
			time.sleep(Constant.USER_WAITING_TIME)

		field.send_keys(string)


	def __upload(self) -> (bool, Optional[str]):
		edit_mode = self.metadata_dict[Constant.VIDEO_EDIT]
		if edit_mode:
			self.browser.get(edit_mode)
			time.sleep(Constant.USER_WAITING_TIME)
		else:
			self.browser.get(Constant.YOUTUBE_URL)
			time.sleep(Constant.USER_WAITING_TIME)
			self.browser.get(Constant.YOUTUBE_UPLOAD_URL)
			time.sleep(Constant.USER_WAITING_TIME)
			absolute_video_path = str(Path.cwd() / self.video_path)
			self.browser.find(By.XPATH, Constant.INPUT_FILE_VIDEO).send_keys(
				absolute_video_path)
			self.logger.debug('Attached video {}'.format(self.video_path))
			time.sleep(Constant.USER_WAITING_TIME * 3)

		if self.thumbnail_path is not None:
			absolute_thumbnail_path = str(Path.cwd() / self.thumbnail_path)
			self.browser.find(By.XPATH, Constant.INPUT_FILE_THUMBNAIL).send_keys(
				absolute_thumbnail_path)
			change_display = "document.getElementById('file-loader').style = 'display: block! important'"
			self.browser.driver.execute_script(change_display)
			self.logger.debug(
				'Attached thumbnail {}'.format(self.thumbnail_path))

		title_field, description_field = self.browser.find_all(By.ID, Constant.TEXTBOX_ID, timeout=15)

		self.__write_in_field(
			title_field, self.metadata_dict[Constant.VIDEO_TITLE], select_all=True)
		self.logger.debug('The video title was set to \"{}\"'.format(
			self.metadata_dict[Constant.VIDEO_TITLE]))

		video_description = self.metadata_dict[Constant.VIDEO_DESCRIPTION]
		video_description = video_description.replace("\n", Keys.ENTER);
		if video_description:
			self.__write_in_field(description_field, video_description, select_all=True)
			self.logger.debug('Description filled.')

		kids_section = self.browser.find(By.NAME, Constant.NOT_MADE_FOR_KIDS_LABEL)
		kids_section.location_once_scrolled_into_view
		time.sleep(Constant.USER_WAITING_TIME)

		self.browser.find(By.ID, Constant.RADIO_LABEL, kids_section).click()
		self.logger.debug('Selected \"{}\"'.format(Constant.NOT_MADE_FOR_KIDS_LABEL))


		# Playlist
		playlist = self.metadata_dict[Constant.VIDEO_PLAYLIST]
		if playlist:
			self.browser.find(By.CLASS_NAME, Constant.PL_DROPDOWN_CLASS).click()
			time.sleep(Constant.USER_WAITING_TIME)
			search_field = self.browser.find(By.ID, Constant.PL_SEARCH_INPUT_ID)
			self.__write_in_field(search_field, playlist)
			time.sleep(Constant.USER_WAITING_TIME * 2)
			playlist_items_container = self.browser.find(By.ID, Constant.PL_ITEMS_CONTAINER_ID)
			# Try to find playlist
			self.logger.debug('Playlist xpath: "{}".'.format(Constant.PL_ITEM_CONTAINER.format(playlist)))
			playlist_item = self.browser.find(By.XPATH, Constant.PL_ITEM_CONTAINER.format(playlist), playlist_items_container)
			if playlist_item: 
				self.logger.debug('Playlist found.')
				playlist_item.click()
				time.sleep(Constant.USER_WAITING_TIME)
			else:
				self.logger.debug('Playlist not found. Creating')
				self.__clear_field(search_field)
				time.sleep(Constant.USER_WAITING_TIME)

				new_playlist_button = self.browser.find(By.CLASS_NAME, Constant.PL_NEW_BUTTON_CLASS)
				new_playlist_button.click()

				create_playlist_container = self.browser.find(By.ID, Constant.PL_CREATE_PLAYLIST_CONTAINER_ID)
				playlist_title_textbox = self.browser.find(By.XPATH, "//textarea", create_playlist_container)
				self.__write_in_field(playlist_title_textbox, playlist)

				time.sleep(Constant.USER_WAITING_TIME)
				create_playlist_button = self.browser.find(By.CLASS_NAME, Constant.PL_CREATE_BUTTON_CLASS)
				create_playlist_button.click()
				time.sleep(Constant.USER_WAITING_TIME)
			
			done_button = self.browser.find(By.CLASS_NAME, Constant.PL_DONE_BUTTON_CLASS)
			done_button.click()


		# Advanced options
		self.browser.find(By.ID, Constant.ADVANCED_BUTTON_ID).click()
		self.logger.debug('Clicked MORE OPTIONS')
		time.sleep(Constant.USER_WAITING_TIME)

		# Tags
		tags = self.metadata_dict[Constant.VIDEO_TAGS]
		if tags: 
			tags_container = self.browser.find(By.ID, Constant.TAGS_CONTAINER_ID)
			tags_field = self.browser.find(By.ID, Constant.TAGS_INPUT, tags_container)
			self.__write_in_field(tags_field, ','.join(tags))
			self.logger.debug('The tags were set to \"{}\"'.format(tags))


		self.browser.find(By.ID, Constant.NEXT_BUTTON).click()
		self.logger.debug('Clicked {} one'.format(Constant.NEXT_BUTTON))

		self.browser.find(By.ID, Constant.NEXT_BUTTON).click()
		self.logger.debug('Clicked {} two'.format(Constant.NEXT_BUTTON))

		self.browser.find(By.ID, Constant.NEXT_BUTTON).click()
		self.logger.debug('Clicked {} three'.format(Constant.NEXT_BUTTON))
		public_main_button = self.browser.find(By.NAME, Constant.PUBLIC_BUTTON)
		self.browser.find(By.ID, Constant.RADIO_LABEL,
						  public_main_button).click()
		self.logger.debug('Made the video {}'.format(Constant.PUBLIC_BUTTON))

		video_id = self.__get_video_id()

		status_container = self.browser.find(By.XPATH, Constant.STATUS_CONTAINER)
		while True:
			progress = status_container.get_attribute('value')
			if int(progress) < 100:
				self.logger.debug('Upload video progress: {}%'.format(progress))
				time.sleep(Constant.USER_WAITING_TIME * 5)
			else:
				time.sleep(Constant.USER_WAITING_TIME * 3)
				break

		done_button = self.browser.find(By.ID, Constant.DONE_BUTTON)

		# Catch such error as
		# "File is a duplicate of a video you have already uploaded"
		if done_button.get_attribute('aria-disabled') == 'true':
			error_message = self.browser.find(By.XPATH,
											  Constant.ERROR_CONTAINER).text
			self.logger.error(error_message)
			return False, None

		done_button.click()
		self.logger.debug(
			"Published the video with video_id = {}".format(video_id))
		time.sleep(Constant.USER_WAITING_TIME)
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
			self.logger.warning(Constant.VIDEO_NOT_FOUND_ERROR)
			pass
		return video_id

	def __quit(self):
		self.browser.driver.quit()
