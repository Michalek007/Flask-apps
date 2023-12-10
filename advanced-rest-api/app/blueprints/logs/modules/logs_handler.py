from datetime import datetime

from configuration import Config
from utils.files_management import FilesManagement


class LogsHandler:
    """ Implements methods responsible for manipulating logs data.
        Attributes:
            LOGS_FILES: dict with log files names
            file: FilesManagement instance
    """

    LOGS_FILES = {
        'client': Config.CLIENT_LOGS_FILE,
        'service': Config.SERVICE_LOGS_FILE
    }

    def __init__(self, file_name: str):
        self.file = FilesManagement(file_name)

    @classmethod
    def get_log_handler(cls, name: str):
        """ LogsHandler constructor.
            Args:
                name: logs name
            Returns:
                LogsHandler object or ``None`` if file was not found or name was incorrect
        """
        if name not in cls.LOGS_FILES.keys():
            return None
        try:
            return cls(cls.LOGS_FILES.get(name))
        except FileNotFoundError:
            return None

    def get(self):
        """ Returns logs data. """
        return self.file.get_data()

    def delete(self, timestamp):
        """ Deletes logs earlier than given timestamp. """
        data = self.file.get_data()

        formatted_data = []
        for item in data:
            line = item.split('ERROR:')
            line = list(map(lambda value: value.strip(), line))
            formatted_data.append(line)

        deleted_index_list = []
        flag = 0
        for i in range(len(formatted_data)):
            try:
                item = formatted_data[i]
                item_index = i
                if len(item) == 1 and flag == 0:
                    item_before = formatted_data[item_index - 1]
                    item_before_timestamp = datetime.strptime(item_before[0], '%Y-%m-%d %H:%M:%S,%f')
                    if item_before_timestamp < timestamp:
                        flag = 1
                if len(item) > 1:
                    item_timestamp = datetime.strptime(item[0], '%Y-%m-%d %H:%M:%S,%f')
                    if item_timestamp < timestamp:
                        deleted_index_list.append(item_index)
                if flag:
                    deleted_index_list.append(item_index)
                    item_after = formatted_data[item_index + 1]
                    if len(item_after) > 1:
                        flag = 0
            except (IndexError, ValueError):
                continue

        for i in range(len(deleted_index_list)):
            data.pop(deleted_index_list[i] - i)
        self.file.save_data()
