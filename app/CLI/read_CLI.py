import configparser as parse


def reading_cli(file):
    """
    Read the file ini and use the template to run the code.
    :param file: The file fetched for the template.
    :return: Return a dictionary of the template.
    """
    path_filters_log = {
        "input_dir": '',
        "output_dir": '',
        "log_file": '',
        "filters": '',
        "extension": '',
    }

    conf = parse.ConfigParser()
    conf.read(f'app/CLI/{file}')
    conf.sections()
    path_filters_log['input_dir'] = conf['DEFAULT']['input_dir']
    path_filters_log['output_dir'] = conf['DEFAULT']['output_dir']
    path_filters_log['log_file'] = conf['DEFAULT']['log_file']
    path_filters_log['extension'] = conf['DEFAULT']['extension']
    path_filters_log['filters'] = conf['filters']['content']

    return path_filters_log
