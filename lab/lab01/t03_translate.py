import os
from os import environ
from google.cloud import translate
from google.oauth2 import service_account


dirname = os.path.dirname(__file__)
key_file_path = os.path.abspath(os.path.join(
    dirname, '..', '..', 'service_account_key.json'))
credentials = service_account.Credentials.from_service_account_file(
    key_file_path)
# Reference
# https://codelabs.developers.google.com/codelabs/cloud-translation-python3#0


def get_parent() -> str:
    parent = f"projects/{credentials.project_id}"
    return parent


def detect_language(text: str) -> str:
    client = translate.TranslationServiceClient.from_service_account_file(
        key_file_path)
    response = client.detect_language(parent=get_parent(), content=text)

    max_confidence_language = max(
        response.languages, key=lambda language: language.confidence)
    return max_confidence_language.language_code


def translate_to(text: str, target_language_code: str) -> str:
    client = translate.TranslationServiceClient.from_service_account_file(
        key_file_path)
    response = client.translate_text(
        contents=[text],
        target_language_code=target_language_code,
        parent=get_parent(),
    )

    translated_texts = [
        translation.translated_text for translation in response.translations]
    return ' '.join(translated_texts)


"""
print(detect_language("雲端系統及數據中心管理高級文憑課程編號 IT114115"))
print(detect_language("Higher Diploma in Cloud and Data Centre Administration Programme code IT114115"))
print(detect_language("ワンピース"))
print(translate_to("雲端系統及數據中心管理高級文憑課程編號 IT114115", "en"))
print(translate_to("Higher Diploma in Cloud and Data Centre Administration Programme code IT114115","ja"))
print(translate_to("ワンピース","en"))
"""