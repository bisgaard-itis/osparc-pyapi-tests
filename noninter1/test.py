import json
import os
from pathlib import Path

print("Konichiwa. O genki desu ka?")

input_path = Path(os.environ["INPUT_FOLDER"])
output_path = Path(os.environ["OUTPUT_FOLDER"])

test_data_path = input_path / "input.data"

test_data = json.loads(test_data_path.read_text())

output_paths = {}
for output_i in range(1, 6):
    output_paths[output_i] = output_path / f"output_{output_i}"

    output_paths[output_i].mkdir(parents=True, exist_ok=True)

output_data_path = output_paths[1] / "output.data"

output_data_path.write_text(json.dumps(test_data))

print(f"Wrote output files to: {output_path.resolve()}")

print("Genki desu")
