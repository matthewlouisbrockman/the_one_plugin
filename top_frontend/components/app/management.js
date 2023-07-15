import { useEffect, useState } from "react";
import { CreateJobForm } from "./ui/create_job_form";
import { JobSelectionDropdown } from "./ui/job_selection_dropdown";
export const Management = () => {
  const [jobs, setJobs] = useState([]);
  const [currentJobId, setCurrentJobId] = useState(null);
  const [jobTasks, setJobTasks] = useState([]);
  const [creatingJob, setCreatingJob] = useState(false);

  const getJobs = async () => {
    const res = await fetch("/api/theoneplugin/jobs");
    const data = await res.json();
    console.log("res: ", data);
    if (data?.jobs) {
      setJobs(data.jobs);
      setCurrentJobId(data.jobs[0]?.job_id);
    }
  };

  const handleSaveJob = async ({ jobId, jobName, jobDescription }) => {
    if (!jobName || !jobDescription) {
      setCreatingJob(false);
      return;
    }
    const res = await fetch("/api/theoneplugin/jobs", {
      method: "POST",
      body: JSON.stringify({
        job_id: jobId,
        job_name: jobName,
        job_description: jobDescription,
      }),
    });
    const data = await res.json();
    console.log("res: ", data);
    if (data?.job) {
      setJobs([...jobs, data.job]);
      setCurrentJobId(data.job.job_id);
    }
  };

  useEffect(() => {
    getJobs();
  }, []);

  return (
    <div className="flex flex-col w-full h-full bg-black text-white">
      <button
        className="bg-white text-black rounded px-3 py-1 w-[300px]"
        onClick={() => setCreatingJob(true)}
      >
        Create Job
      </button>
      {creatingJob && <CreateJobForm onClose={handleSaveJob} />}
      <JobSelectionDropdown
        jobs={jobs}
        currentJob={currentJobId}
        setCurrentJob={setCurrentJobId}
      />
      {!!currentJobId && (
        <JobDisplay
          jobId={currentJobId}
          job={jobs.find((job) => job.job_id === parseInt(currentJobId))}
          setJob={(job) => {
            const newJobs = jobs.map((j) => {
              if (j.job_id === job.job_id) {
                return job;
              }
              return j;
            });
            setJobs(newJobs);
          }}
          handleSaveJob={(name, description) => {
            handleSaveJob({
              jobId: currentJobId,
              jobName: name,
              jobDescription: description,
            });
          }}
        />
      )}
    </div>
  );
};

const JobDisplay = ({ job, handleSaveJob, jobId }) => {
  console.log("job: ", job);
  const [jobName, setJobName] = useState(job?.job_name || "");
  const [jobDescription, setJobDescription] = useState(
    job?.job_description || ""
  );
  useEffect(() => {
    setJobName(job?.job_name || "");
    setJobDescription(job?.job_description || "");
  }, [jobId]);

  return (
    <div className="flex flex-col bg-white text-black p-4">
      <div className="flex flex-row">
        <div>Job Name</div>
        <input
          type="text"
          className="border-2 border-black rounded"
          value={jobName}
          onChange={(e) => setJobName(e.target.value)}
        />
      </div>
      <div className="flex flex-row">
        <div>Job Description</div>
        <textarea
          type="text"
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          className="border-2 border-black rounded w-[500px]"
        />
      </div>
      <div className="flex flex-row">
        <button
          className="rounded px-3 py-1"
          onClick={() => {
            handleSaveJob(jobName, jobDescription);
          }}
        >
          Save
        </button>
      </div>
    </div>
  );
};
