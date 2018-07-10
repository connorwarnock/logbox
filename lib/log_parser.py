import dateutil.parser


class LogParser:
    KEYS=[('drone_id', 'Integer'),
          ('drone_generation', 'Integer'),
          ('start_time', 'DateTime'),
          ('end_time', 'DateTime'),
          ('lat', 'Float'),
          ('lon', 'Float'),
          ('building_layout_map', 'String')]

    """
    @param log_path: path to local file or s3 object
    """
    def __init__(self, log_path):
        self.log_path = log_path

    """
    Parses log file and returns list of log lines

    @return: list of log lines as dictionaries
    """
    def parse(self):
        parsed_lines = []
        with open(self.log_path) as f:
            for line in f.readlines():
                parsed_lines.append(self.__parse_line(line))
        return parsed_lines

    def __parse_line(self, line):
        values = line.rstrip('\n').split(' ')
        parsed_values = []
        for key_with_type, original_value in zip(self.KEYS, values):
            key = key_with_type[0]
            type = key_with_type[1]
            if type == 'Integer':
                value = int(original_value)
            elif type == 'DateTime':
                value = dateutil.parser.parse(original_value)
            elif type == 'Float':
                value = float(original_value)
            elif type == 'String':
                value = original_value
            else:
                raise Error('Type not supported', type)
            parsed_values.append((key, value))
        return dict(parsed_values)
