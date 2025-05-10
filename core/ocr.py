from config import ocr_config
import easyocr


class OCR:
    def __init__(self):
        self.reader = easyocr.Reader(lang_list=ocr_config.lang_list, gpu=ocr_config.use_GPU,
                                     user_network_directory=ocr_config.model_storage_directory)

    def read(self, image) -> list:
        return self.reader.readtext(batch_size=ocr_config.batch_size, rotation_info=ocr_config.rotation_info,
                                    paragraph=ocr_config.paragraph, detail=ocr_config.detail, image=image)
