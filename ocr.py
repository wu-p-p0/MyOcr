import config  # load config for ocr
import easyocr


class OCR:
    def __init__(self):
        self.reader = easyocr.Reader(lang_list=config.lang_list, gpu=config.use_GPU,
                                     user_network_directory=config.model_storage_directory)

    def read(self, image) -> list:
        return self.reader.readtext(batch_size=config.batch_size, rotation_info=config.rotation_info,
                                    paragraph=config.paragraph, detail=config.detail, image=image)
