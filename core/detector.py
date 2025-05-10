import re
import csv
from typing import List

from config import detector_config


class KeywordDetector:
    """关键词检测器，用于检测文本中是否包含敏感关键词"""

    def __init__(self, keywords_file: str = detector_config.keywords_file):
        """
        初始化关键词检测器

        参数:
            keywords_file: 关键词CSV文件路径
        """
        self.keywords = self._load_keywords(keywords_file)
        self.pattern = self._build_pattern()

    def _load_keywords(self, keywords_file: str) -> List[str]:
        """从CSV文件加载关键词列表"""
        try:
            with open(keywords_file, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                return [keyword.strip() for keyword in next(reader) if keyword.strip()]
        except Exception as e:
            print(f"加载关键词文件失败: {e}")
            return []

    def _build_pattern(self) -> re.Pattern:
        """构建正则表达式匹配模式"""
        if not self.keywords:
            return None
        escaped_keywords = [re.escape(k) for k in self.keywords]
        return re.compile(r'\b(' + '|'.join(escaped_keywords) + r')\b', re.IGNORECASE)

    def contains_keywords(self, text: str) -> bool:
        """
        检测文本是否包含任何关键词

        参数:
            text: 待检测的文本

        返回:
            bool: 包含关键词返回True，否则返回False
        """
        if not self.pattern:
            return False
        return bool(self.pattern.search(text))
