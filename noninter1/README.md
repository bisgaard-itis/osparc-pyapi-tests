How to use
==========

* Put your api key/secret in an osparc_conf.json file, according to:
[osparc_conf.json.dummy](osparc_conf.json.dummy)

* Look at 
[run.sh](run.sh)
and adapt to your system.

* Create a study template according to this figure (make sure the file picker and probe have exactly the same name as in the figure):
[study_template.png](study_template.png)

* Put the UUID of the template you created in the run_study.py script

* Execute
```
./run.sh
```

* You should see something like:
```
{'items': [{'content_schema': None,
            'key': '5858836e-7368-5f50-99ca-d82d1c31a242',
            'kind': 'output'}],
 'total': 1}
Status: [PENDING]
Status: [STARTED]
Status: [STARTED]
Status: [STARTED]
...
Status: [STARTED]
Status: [STARTED]
Status: [SUCCESS]
{'job_id': 'f95fb2ce-f5a3-11ee-9635-02420a140047',
 'progress': 100,
 'started_at': datetime.datetime(2024, 4, 8, 12, 31, 52, 355923, tzinfo=tzutc()),
 'state': 'SUCCESS',
 'stopped_at': datetime.datetime(2024, 4, 8, 12, 32, 22, 881941, tzinfo=tzutc()),
 'submitted_at': datetime.datetime(2024, 4, 8, 12, 31, 52, 235699, tzinfo=tzutc())}
{'OutputFile1': {'checksum': None,
 'content_type': 'application/zip',
 'e_tag': 'db4952ec22a6d16b7addcd45eb03bda4',
 'filename': 'output_data.zip',
 'id': '409f0972-eceb-38ef-a921-7b28b4780f7a'}}
{"f1": 3}
```


