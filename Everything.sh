#!/bin/bash

#SBATCH --job-name=everything
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=32000
#SBATCH --output=auto/Everything.out
#SBATCH --error=auto/Everything.err
#SBATCH --cpus-per-task=1
#SBATCH --time=1-0:00:00
#SBATCH --mail-user=FILL_IN
#SBATCH --mail-type=END,FAIL
#SBATCH --account=FILL_IN

get_job_id() {
    echo "$1" | awk '{print $NF}'
}

# Submit download job
download_job=$(sbatch <<DOWNLOAD
#!/bin/bash
#SBATCH -t 1-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=128000
#SBATCH --cpus-per-task=1
#SBATCH --partition=batch
#SBATCH --job-name=Download
#SBATCH --output=auto/DandF.out
#SBATCH --error=auto/DandF.err
#SBATCH --mail-user=FILL_IN
#SBATCH --mail-type=FAIL
#SBATCH --account=FILL_IN
Download.sh
DOWNLOAD
)

# Extract the job ID from the submission output
download_job_id=$(get_job_id "$download_job")


# Submit Update job after Main job
update_job=$(sbatch --dependency=afterok:$download_job_id <<UPDATE
#!/bin/bash
#SBATCH -t 0-01:00:00
#SBATCH --partition=batch
#SBATCH --job-name=Update
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=32000
#SBATCH --output=auto/UpdateMaster.out
#SBATCH --error=auto/UpdateMaster.err
#SBATCH --mail-user=FILL_IN
#SBATCH --mail-type=FAIL
#SBATCH --account=FILL_IN
UpdateMasterLists.sh
UPDATE
)

update_job_id=$(get_job_id "$update_job")

# Submit Format job after Update job
format_job=$(sbatch --dependency=afterok:$update_job_id <<FORMAT
#!/bin/bash
#SBATCH -t 1-00:00:00
#SBATCH --partition=batch
#SBATCH --job-name=Format
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=32000
#SBATCH --output=auto/Format.out
#SBATCH --error=auto/Format.err
#SBATCH --account=FILL_IN
#SBATCH --mail-user=FILL_IN
#SBATCH --mail-type=FAIL
FormatFiles.sh
FORMAT
)

format_job_id=$(get_job_id "$format_job")

# Submit Gpt job after Format job
gpt_job=$(sbatch --dependency=afterok:$format_job_id <<GPT
#!/bin/bash
#SBATCH -t 0-01:00:00
#SBATCH --partition=batch
#SBATCH --job-name=Gpt
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=32000
#SBATCH --output=auto/Gpt.out
#SBATCH --error=auto/Gpt.err
#SBATCH --account=FILL_IN
#SBATCH --mail-user=FILL_IN
#SBATCH --mail-type=FAIL
Gpt.sh
GPT
)

gpt_job_id=$(get_job_id "$gpt_job")

# Submit Upload job after GPT job
upload_job=$(sbatch --dependency=afterok:$gpt_job_id <<UPLOAD
#!/bin/bash
#SBATCH -t 0-01:00:00
#SBATCH --partition=batch
#SBATCH --job-name=Upload
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=32000
#SBATCH --output=auto/Upload.out
#SBATCH --error=auto/Upload.err
#SBATCH --account=FILL_IN
#SBATCH --mail-user=FILL_IN
#SBATCH --mail-type=FAIL,END
/Upload.sh
UPLOAD
)
