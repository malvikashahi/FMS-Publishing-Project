# main.py

from publisher import publish

publish(
    excel_file="input_files/HoldingData.xlsx",
    ppt_template="templates/TestCase1.pptx",
    mapping_file="configuration_files/mapping.json",
    output_file="output_files/output.pptx"
)