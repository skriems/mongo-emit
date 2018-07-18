import ast
import argparse
import logging
import sys

from .helpers import utc_timestamp

LOG = logging.getLogger(__name__)


def cli_args():
    """ parse cli arguments """

    parser = argparse.ArgumentParser('mongo-emit')

    parser.add_argument(
        '--target',
        help="'<db>' or '<db>.<collection>' to be watched")

    parser.add_argument(
        '--pipeline',
        help="aggreate pipeline (list) wrapped in 'single quotes'!")

    parser.add_argument(
        '--resume-token',
        help='specify a specific resume_token')

    parser.add_argument(
        '--starttime',
        help='start at <iso8601_datetime_string>')

    parser.add_argument(
        '--full-document', action='store_true',
        help='fullDocument field on _update_ events')

    args = parser.parse_args()

    # VALIDATION
    if args.pipeline:
        try:
            args.pipeline = ast.literal_eval(args.pipeline)
        except ValueError:
            LOG.error(' pipeline must be a list\n')
            parser.print_help()
            sys.exit(1)

    if args.resume_token:
        try:
            args.resume_token = ast.literal_eval(args.resume_token)
        except ValueError:
            LOG.error(' resume_token must be a dict\n')
            parser.print_help()
            sys.exit(1)

    # the following options get grouped into an `options` attribute and will be
    # removed from the Namespace obj
    #
    # That way Namespace.__dict__ has the needed shape for getting passed to
    # `update_from_dict`
    options = getattr(args, 'options', {})

    if args.full_document:
        options.update(full_document='updateLookup')
    if args.resume_token:
        options.update(resume_after=args.resume_token)
    if args.starttime:
        timestamp = utc_timestamp(args.starttime)

        options.update(start_at_operation_time=timestamp)

    if options:
        setattr(args, 'options', options)

    # cleanup the Namespace
    delattr(args, 'resume_token')
    delattr(args, 'starttime')
    delattr(args, 'full_document')
    return args
