# Description

This Python script generates graphs visualizing peer retention in Status app.

# Details

The script queries an ElasticSearch endpoint for `logstash-*` indices and aggregates counts of instances of log messages with set `peer_id` field.

This data is then analyzed using [Pandas](https://pandas.pydata.org/) and graphed using [Seaborn](https://seaborn.pydata.org/) in the form of 

This was built from a combination of a [CSV generating script](https://github.com/status-im/infra-utils/blob/d1e0426cc28a1b20a182f341c55c4e295912fe35/elasticsearch/unique_count.py) and a [cohort analysis](https://colab.research.google.com/drive/1Osl3EXbKR2_iwAhOHmAiCum9F6IquRX2) done by [@jakubgs](https://github.com/jakubgs) and [@bgits](https://github.com/bgits).

# Example

![](examples/weekly_cohorts.png)
