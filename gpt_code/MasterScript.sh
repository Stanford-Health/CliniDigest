#!/bin/bash

# fill in sbatch info

get_job_id() {
    echo "$1" | awk '{print $NF}'
}

# TODO: add full path before DownloadCode.sh
# ex: /labs/mpsnyder/arjo/clinical_trials_code/DownloadCode.sh
# Submit Download job
main_job=$(sbatch <<DOWNLOAD
#!/bin/bash
# fill in sbatch info
clinical_trials_code/DownloadCode.sh
MAIN
)

# Extract the job ID from the submission output
main_job_id=$(get_job_id "$main_job")

# TODO: add full path before WebsiteCode.sh
# ex: /labs/mpsnyder/arjo/clinical_trials_code/WebsiteCode.sh
# Submit Website job after Main job
website_job=$(sbatch --dependency=afterok:$main_job_id <<WEBSITE
#!/bin/bash
# fill in sbatch info
clinical_trials_code/WebsiteCode.sh
WEBSITE
)

# TODO: add full path before Filter.sh
# ex: /labs/mpsnyder/arjo/gpt_code/Filter.sh
# Submit Filter job after Main job
filter_job=$(sbatch --dependency=afterok:$main_job_id <<FILTER
#!/bin/bash
# fill in sbatch info
gpt_code/Filter.sh
FILTER
)

filter_job_id=$(get_job_id "$filter_job")

# TODO: add full path before UpdateMasterLists.sh
# ex: /labs/mpsnyder/arjo/gpt_code/UpdateMasterLists.sh
# Submit Update job after Filter job
update_job=$(sbatch --dependency=afterok:$filter_job_id <<UPDATE
#!/bin/bash
# fill in sbatch info
gpt_code/UpdateMasterLists.sh
UPDATE
)

update_job_id=$(get_job_id "$update_job")

# TODO: add full path before FormatFiles.sh
# ex: /labs/mpsnyder/arjo/gpt_code/FormatFiles.sh
# Submit Format job after Update job
format_job=$(sbatch --dependency=afterok:$update_job_id <<FORMAT
#!/bin/bash
# fill in sbatch info
gpt_code/FormatFiles.sh
FORMAT
)

format_job_id=$(get_job_id "$format_job")

# TODO: add full path before Gpt.sh
# ex: /labs/mpsnyder/arjo/gpt_code/Gpt.sh
# Submit Gpt job after Format job
gpt_job=$(sbatch --dependency=afterok:$format_job_id <<GPT
#!/bin/bash
# fill in sbatch info
gpt_code/Gpt.sh
GPT
)

gpt_job_id=$(get_job_id "$gpt_job")

# TODO: add full path before Upload.sh
# ex: /labs/mpsnyder/arjo/gpt_code/Upload.sh
# Submit Upload job after Format job
upload_job=$(sbatch --dependency=afterok:$gpt_job_id <<UPLOAD
#!/bin/bash
# fill in sbatch info
gpt_code/Upload.sh
UPLOAD
)
