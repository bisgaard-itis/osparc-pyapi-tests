"""Test osparc client API"""

import time
import shutil
import zipfile

import osparc
import osparc.api
import osparc_client
from pathlib import Path

osparc_cfg = osparc.Configuration(
    host="10.43.103.149.nip.io:8006",
    username="test_T1QyAxKBUX",
    password="0dsHA6zdYDNEtwNKsXZHBQq8eHuPbd",
)

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
    template_id = "02621c5a-bbba-11ee-ba85-02420a000022"
    # job_id = "32ccb81c-bc34-11ee-ba85-02420a000022"

    print(studies_api.list_study_ports(study_id=template_id))

    test_py_file = osparc.api.FilesApi(api_client).upload_file(
        file=Path("test.py")
    )

    test_data_file = osparc.api.FilesApi(api_client).upload_file(
        file=Path("input.data")
    )

    new_job = studies_api.create_study_job(
        study_id=template_id,
        job_inputs={
            "values": {
                "PythonCode1": test_py_file,
                "DataFile1": test_data_file,
            }
        },
    )

    print(studies_api.start_study_job(study_id=template_id, job_id=new_job.id))

    job_status = studies_api.inspect_study_job(
        study_id=template_id, job_id=new_job.id
    )

    while job_status.state != "SUCCESS" and job_status != "FAILED":
        job_status = studies_api.inspect_study_job(
            study_id=template_id, job_id=new_job.id
        )
        print(job_status.state)

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
    shutil.move(output_file, output_filename)

    output_file = Path(output_filename)

    with zipfile.ZipFile(output_file, "r") as zip_ref:
        zip_ref.extractall()

    outdata_file = Path("output_1/output.data")
    print(outdata_file.read_text())
