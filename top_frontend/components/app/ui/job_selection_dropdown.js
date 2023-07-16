export const JobSelectionDropdown = ({ jobs, currentJob, setCurrentJob }) => {
  return (
    <div className="flex flex-row">
      {!!jobs?.length && (
        <select
          value={currentJob} // Use currentJob directly as the value
          onChange={(e) => {
            setCurrentJob(parseInt(e.target.value));
          }}
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
