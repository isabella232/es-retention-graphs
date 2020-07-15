#!/usr/bin/env python3
from os import path
from optparse import OptionParser

from query import ESQueryPeers
from graph import PDGraphPeers

HELP_DESCRIPTION = 'This generates a CSV with buckets of peer_ids for every day.'
HELP_EXAMPLE = 'Example: ./unique_count.py -i "logstash-2019.11.*" -f "peer_id"'


def parse_opts():
    parser = OptionParser(description=HELP_DESCRIPTION, epilog=HELP_EXAMPLE)
    parser.add_option('-H', '--host', dest='es_host', default='localhost',
                      help='ElasticSearch host.')
    parser.add_option('-P', '--port', dest='es_port', default=9200,
                      help='ElasticSearch port.')
    parser.add_option('-i', '--index-pattern', default='logstash-*',
                      help='Patter for matching indices.')
    parser.add_option('-f', '--field', type='str', default='peer_id',
                      help='Name of the field to count.')
    parser.add_option('-F', '--fleet', type='str', default='eth.prod',
                      help='Name of the fleet to query.')
    parser.add_option('-m', '--max-size', type='int', default=100000,
                      help='Max number of counts to find.')
    parser.add_option('-d', '--image-dpi', type='int', default=200,
                      help='DPI of generated PNG images.')
    parser.add_option('-o', '--output-dir', default='./',
                      help='Dir into which images are generated.')
    (opts, args) = parser.parse_args()

    if not opts.field:
        parser.error('No field name specified!')

    return (opts, args)


def main():
    (opts, args) = parse_opts()

    esq = ESQueryPeers(opts.es_host, opts.es_port)

    data = []
    for index in esq.get_indices(opts.index_pattern):
        print('Index: {}'.format(index))
        data.extend(esq.get_peers(index, opts.field, opts.fleet, opts.max_size))

    pdg = PDGraphPeers(data)

    plot = pdg.days_per_peers()
    plot.figure.savefig(path.join(opts.output_dir, "days_per_peers.png"),
                        dpi=opts.image_dpi)

    matrix = pdg.weekly_cohorts()
    matrix.figure.savefig(path.join(opts.output_dir, "weekly_cohorts.png"),
                          dpi=opts.image_dpi)


if __name__ == '__main__':
    main()
