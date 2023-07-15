export const JobSelectionDropdown = ({ jobs, currentJob, setCurrentJob }) => {
  return (
    <div className="flex flex-row">
      {!!jobs?.length && (
        <select
          value={jobs.find((job) => job.job_id === currentJob)?.job_id}
          onChange={(e) => {
            console.log("target value: ", e.target.value);
            setCurrentJob(parseInt(e.target.value));
          }}
          defaultValue={jobs[0]?.job_id}
        >
          {jobs.map((job) => (
            <option key={job.job_id} value={job.job_id}>
              {job.job_name}
            </option>
          ))}
        </select>
      )}
    </div>
  );
};
