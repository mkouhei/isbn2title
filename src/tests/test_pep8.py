#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
if sys.version_info > (2, 6) and sys.version_info < (3, 0):
    import pep8

    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.dirname(CURRENT_DIR)

    def test_pep8():
        arglist = [
            '--statistics',
            '--filename=*.py',
            '--show-source',
            '--benchmark',
            '--repeat',
            '--show-pep8',
            #'--qq',
            #'-v',
            BASE_DIR,
            ]

        options, args = pep8.process_options(arglist)
        runner = pep8.input_file

        for path in args:
            if os.path.isdir(path):
                pep8.input_dir(path, runner=runner)
            elif not pep8.excluded(path):
                options.counters['files'] += 1
                runner(path)

        pep8.print_statistics()
        errors = pep8.get_count('E')
        warnings = pep8.get_count('W')
        message = 'pep8: %d errors / %d warnings' % (errors, warnings)
        print(message)
        assert errors + warnings == 0, message
