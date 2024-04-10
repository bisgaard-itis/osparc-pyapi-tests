"""Test osparc client API"""

import json
import shutil
import time
import zipfile
from pathlib import Path

import osparc
import osparc.api
import osparc_client

osparc_conf = json.loads(Path("osparc_conf.json").read_text())
osparc_cfg = osparc.Configuration(**osparc_conf)

with osparc.ApiClient(osparc_cfg) as api_client:
    studies_api = osparc_client.StudiesApi(api_client)

    # template_id = "61b1bb42-ba03-11ee-986b-02420a00001c" # dummy
    # template_id = "1d99c612-bac5-11ee-986b-02420a00001c"  # dummypython
    # template_id = "ba57796c-bab2-11ee-986b-02420a00001c"
    # template_id = (
    #    "851bad86-bb84-11ee-abfc-02420a00001c"  # pythonrunnerservicetest
    # )
    # template_id = (
    #    "f580a480-bb9a-11ee-b73f-02420a000006"  # PythonRunnerStudyService
    # )
    # template_id = "02621c5a-bbba-11ee-ba85-02420a000022"
    # template_id = "a13d566e-c05b-11ee-95bf-02420a000008"
    # job_id = "32ccb81c-bc34-11ee-ba85-02420a000022"
    template_id = "5b01fb90-f59f-11ee-9635-02420a140047"

    print(studies_api.list_study_ports(study_id=template_id))

    test_py_file = osparc.api.FilesApi(api_client).upload_file(
        file=Path("test.py")
    )

    test_data_file = osparc.api.FilesApi(api_client).upload_file(
        file=Path("input.data")
    )
    test_json_file = osparc.api.FilesApi(api_client).upload_file(
        file=Path("input.json")
    )

    new_job = studies_api.create_study_job(
        study_id=template_id,
        job_inputs={
            "values": {
                # "InputNumber1": 0.5,
                # "InputInteger1": 6,
                "InputFile1": test_json_file,
            }
        },
    )

    studies_api.start_study_job(study_id=template_id, job_id=new_job.id)

    job_status = studies_api.inspect_study_job(
        study_id=template_id, job_id=new_job.id
    )

    while job_status.state != "SUCCESS" and job_status.state != "FAILED":
        job_status = studies_api.inspect_study_job(
            study_id=template_id, job_id=new_job.id
        )
        print(f"Status: [{job_status.state}]")

        time.sleep(1)

    print(
        studies_api.inspect_study_job(study_id=template_id, job_id=new_job.id)
    )

    job_results = studies_api.get_study_job_outputs(
        study_id=template_id, job_id=new_job.id
    ).results

    print(job_results)

    output_filename = job_results["OutputFile1"].filename
    output_file = Path(
        osparc.api.FilesApi(api_client).download_file(
            job_results["OutputFile1"].id
        )
    )

    studies_api.delete_study_job(study_id=template_id, job_id=new_job.id)
    shutil.move(output_file, output_filename)

    output_file = Path(output_filename)

    # print(output_file.resolve())

    with zipfile.ZipFile(output_file, "r") as zip_ref:
        zip_ref.extractall()

    outdata_file = Path("output.json")
    print(outdata_file.read_text())
