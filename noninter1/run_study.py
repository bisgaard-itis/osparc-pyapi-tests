"""Test osparc client API"""

import json

# import os
import shutil
import sys
import time
import zipfile
from pathlib import Path

import numpy
import osparc
import osparc_client

# import pdb_attach
import urllib3

MAX_N_OF_ATTEMPTS = 5
RETRY_MEAN_START_INTERVAL = 2

exitcode_map = {0: 0, 1: 1, 2: 2, 504: 14, 502: 12}


def main():
    # pdb_port = int(numpy.random.uniform(10000, 50000))
    # pdb_attach.listen(pdb_port)
    # print(f"PDB listening on port: {pdb_port}")
    # print(f"My PID is: {os.getpid()}")

    osparc_conf = json.loads(Path("osparc_conf.json").read_text())
    template_id = osparc_conf["template_id"]
    del osparc_conf["template_id"]
    # osparc_cfg = osparc.Configuration(
    #     retry_status_codes={429, 502, 503, 504, 404, 506}, **osparc_conf
    # )
    osparc_cfg = osparc.Configuration(**osparc_conf)

    try:
        run_test(template_id, osparc_cfg)
        exit_value = 0
    except (
        urllib3.exceptions.MaxRetryError,
        osparc_client.exceptions.ApiException,
        Exception,
    ) as error:
        print(f"Error received: [{error}]")
        if "504" in str(error):
            exit_value = exitcode_map[504]
        elif "(502)" in str(error):
            exit_value = exitcode_map[502]
        elif "Job failed" in str(error):
            exit_value = exitcode_map[2]
        else:
            exit_value = exitcode_map[1]
    finally:
        sys.exit(exit_value)


def run_test(template_id, osparc_cfg):
    with osparc.ApiClient(
        osparc_cfg,
    ) as api_client:
        studies_api = osparc_client.StudiesApi(api_client)

        print(studies_api.list_study_ports(study_id=template_id))

        test_json_file = osparc.FilesApi(api_client).upload_file(
            file=Path("input.json")
        )
        print("Uploaded input json file ")

        n_of_attempts = 0
        time.sleep(
            numpy.random.exponential(n_of_attempts * RETRY_MEAN_START_INTERVAL)
        )

        while True:
            try:
                n_of_attempts += 1
                print("Creating job")
                new_job = studies_api.create_study_job(
                    study_id=template_id,
                    job_inputs={
                        "values": {
                            "InputFile1": test_json_file,
                        }
                    },
                )
                print("Job created successfully")
                break
            except osparc_client.exceptions.ApiException:
                if n_of_attempts >= MAX_N_OF_ATTEMPTS:
                    raise Exception(
                        f"Tried {n_of_attempts} times to create job but failed"
                    )
                else:
                    print("Received API exception, retrying")
                    time.sleep(
                        numpy.random.exponential(
                            n_of_attempts * RETRY_MEAN_START_INTERVAL
                        )
                    )

        print(f"New job created: {new_job}")

        studies_api.start_study_job(study_id=template_id, job_id=new_job.id)

        print("New job has started")

        job_status = studies_api.inspect_study_job(
            study_id=template_id, job_id=new_job.id
        )

        print(f"New job, status: {job_status.state}")

        while job_status.state != "SUCCESS" and job_status.state != "FAILED":
            job_status = studies_api.inspect_study_job(
                study_id=template_id, job_id=new_job.id
            )
            print(f"Status: [{job_status.state}]")

            time.sleep(1)

        if job_status.state == "FAILED":
            raise Exception("Job failed")

        print(
            studies_api.inspect_study_job(
                study_id=template_id, job_id=new_job.id
            )
        )

        output_file = None
        n_of_attempts = 0
        while output_file is None:
            n_of_attempts += 1
            job_results = studies_api.get_study_job_outputs(
                study_id=template_id, job_id=new_job.id
            ).results

            print(job_results)
            output_file = job_results["OutputFile1"]
            if n_of_attempts >= MAX_N_OF_ATTEMPTS:
                raise Exception(
                    f"Tried {n_of_attempts} times to get job output file "
                    "but failed"
                )
            time.sleep(2)

        output_filename = job_results["OutputFile1"].filename
        output_file = Path(
            osparc.FilesApi(api_client).download_file(
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


if __name__ == "__main__":
    main()
